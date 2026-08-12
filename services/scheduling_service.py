"""Alocação e reagendamento de atividades nos slots da escala.

O serviço altera apenas estado atual e sempre acrescenta eventos ao histórico.
Não executa commit: a fronteira transacional pertence ao chamador.
"""

from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models import (
    Activity,
    ActivityHistory,
    ActivityProgress,
    Course,
    StudySlot,
    utcnow,
)
from services.scale_service import generate_slots


QUEUE_STATUSES = ("pending", "deferred")
INACTIVE_STATUSES = ("blocked", "skipped", "cancelled")

# Capacidades adicionais descritas na rotina de estudo. O tipo primário do slot
# continua em StudySlot.slot_type; esta matriz apenas expressa usos flexíveis.
SLOT_CAPABILITIES = {
    "F1": {"THEORY"},
    "F2": {"THEORY", "PRACTICE"},
    "F3": {"PRACTICE"},
    "F4": {"PRACTICE", "REVIEW", "AWS", "READING"},
    "T1": {"THEORY"},
    "T2": {"REVIEW", "AWS", "READING"},
}
COMMERCIAL_SLOT_CAPABILITIES = {"THEORY", "PRACTICE", "REVIEW", "AWS", "READING", "ANY"}


class SchedulingError(ValueError):
    """Erro de domínio do agendador."""


class SchedulingConflict(SchedulingError):
    """A operação conflita com uma associação ou estado existente."""


def is_slot_compatible(activity: Activity, slot: StudySlot) -> bool:
    """Verifica preferência de dia e capacidade do slot."""
    if slot.day_type != "COMERCIAL" and activity.preferred_day_type not in (
        "ANY",
        slot.day_type,
    ):
        return False
    if activity.preferred_slot == "ANY":
        return True
    capabilities = (
        COMMERCIAL_SLOT_CAPABILITIES
        if slot.day_type == "COMERCIAL"
        else SLOT_CAPABILITIES.get(slot.slot_code, {slot.slot_type})
    )
    return activity.preferred_slot in capabilities


def _activity_prerequisites_done(session: Session, activity: Activity) -> bool:
    for prerequisite_id in activity.prerequisites or []:
        prerequisite = session.get(ActivityProgress, prerequisite_id)
        if prerequisite is None or prerequisite.status != "done":
            return False
    return True


def _course_prerequisites_done(session: Session, activity: Activity) -> bool:
    course = session.get(Course, activity.course_id)
    if course is None:
        return False

    for course_id in course.prerequisites or []:
        required_ids = session.scalars(
            select(Activity.id).where(
                Activity.course_id == course_id,
                Activity.required.is_(True),
            )
        ).all()
        if not required_ids:
            return False
        statuses = session.scalars(
            select(ActivityProgress.status).where(
                ActivityProgress.activity_id.in_(required_ids)
            )
        ).all()
        if len(statuses) != len(required_ids) or any(
            status != "done" for status in statuses
        ):
            return False
    return True


def prerequisites_satisfied(session: Session, activity: Activity) -> bool:
    return _activity_prerequisites_done(
        session, activity
    ) and _course_prerequisites_done(session, activity)


def next_eligible_activity(
    session: Session,
    slot: StudySlot | None = None,
) -> Activity | None:
    """Retorna a primeira atividade livre e elegível pela sequência permanente."""
    candidates = session.scalars(
        select(Activity)
        .join(ActivityProgress, ActivityProgress.activity_id == Activity.id)
        .where(
            ActivityProgress.status.in_(QUEUE_STATUSES),
            ActivityProgress.current_slot_id.is_(None),
        )
        .order_by(Activity.sequence, Activity.id)
    ).all()

    for activity in candidates:
        if slot is not None and not is_slot_compatible(activity, slot):
            continue
        if prerequisites_satisfied(session, activity):
            return activity
    return None


def _history(
    session: Session,
    progress: ActivityProgress,
    event_type: str,
    *,
    slot_id: str | None = None,
    from_status: str | None = None,
    to_status: str | None = None,
    note: str = "",
) -> ActivityHistory:
    event = ActivityHistory(
        activity_id=progress.activity_id,
        study_slot_id=slot_id,
        event_type=event_type,
        from_status=from_status,
        to_status=to_status,
        note=note,
    )
    session.add(event)
    return event


def _assign(
    session: Session,
    activity: Activity,
    progress: ActivityProgress,
    slot: StudySlot,
    *,
    note: str = "",
) -> ActivityProgress:
    if progress.status not in QUEUE_STATUSES:
        raise SchedulingConflict(
            f"Atividade {activity.id} não está disponível para alocação"
        )
    if progress.current_slot_id is not None:
        if progress.current_slot_id == slot.id:
            return progress
        raise SchedulingConflict(f"Atividade {activity.id} já possui slot ativo")
    if slot.status != "available" or slot.progress is not None:
        raise SchedulingConflict(f"Slot {slot.id} não está disponível")
    if not is_slot_compatible(activity, slot):
        raise SchedulingConflict(f"Slot {slot.id} é incompatível com {activity.id}")
    if not prerequisites_satisfied(session, activity):
        raise SchedulingConflict(f"Pré-requisitos de {activity.id} não concluídos")

    progress.current_slot = slot
    slot.status = "scheduled"
    _history(
        session,
        progress,
        "scheduled",
        slot_id=slot.id,
        from_status=progress.status,
        to_status=progress.status,
        note=note,
    )
    session.flush()
    return progress


def allocate_activity(
    session: Session,
    activity_id: str,
    slot_id: str,
    *,
    note: str = "",
) -> ActivityProgress:
    activity = session.get(Activity, activity_id)
    progress = session.get(ActivityProgress, activity_id)
    slot = session.get(StudySlot, slot_id)
    if activity is None or progress is None:
        raise SchedulingError(f"Atividade {activity_id} não encontrada")
    if slot is None:
        raise SchedulingError(f"Slot {slot_id} não encontrado")
    return _assign(session, activity, progress, slot, note=note)


def allocate_next(
    session: Session,
    slot_id: str,
    *,
    note: str = "",
) -> ActivityProgress | None:
    slot = session.get(StudySlot, slot_id)
    if slot is None:
        raise SchedulingError(f"Slot {slot_id} não encontrado")
    if slot.status != "available" or slot.progress is not None:
        raise SchedulingConflict(f"Slot {slot.id} não está disponível")

    activity = next_eligible_activity(session, slot)
    if activity is None:
        return None
    progress = session.get(ActivityProgress, activity.id)
    return _assign(session, activity, progress, slot, note=note)


def allocate_available_slots(
    session: Session,
    start_date,
    end_date,
) -> list[ActivityProgress]:
    """Preenche slots vazios cronologicamente sem mover associações existentes."""
    slots = session.scalars(
        select(StudySlot)
        .where(
            StudySlot.study_date.between(start_date, end_date),
            StudySlot.status == "available",
        )
        .order_by(StudySlot.study_date, StudySlot.start_time, StudySlot.slot_code)
    ).all()
    allocations = []
    for slot in slots:
        progress = allocate_next(session, slot.id)
        if progress is not None:
            allocations.append(progress)
    return allocations


def mark_in_progress(
    session: Session, activity_id: str, *, note: str = ""
) -> ActivityProgress:
    progress = session.get(ActivityProgress, activity_id)
    if progress is None:
        raise SchedulingError(f"Atividade {activity_id} não encontrada")
    if progress.status == "in_progress":
        return progress
    if progress.status not in QUEUE_STATUSES or progress.current_slot is None:
        raise SchedulingConflict(f"Atividade {activity_id} não está alocada")

    old_status = progress.status
    progress.status = "in_progress"
    progress.started_at = progress.started_at or utcnow()
    _history(
        session,
        progress,
        "started",
        slot_id=progress.current_slot_id,
        from_status=old_status,
        to_status="in_progress",
        note=note,
    )
    session.flush()
    return progress


def complete_activity(
    session: Session, activity_id: str, *, note: str = ""
) -> ActivityProgress:
    progress = session.get(ActivityProgress, activity_id)
    if progress is None:
        raise SchedulingError(f"Atividade {activity_id} não encontrada")
    if progress.status == "done":
        return progress
    if progress.current_slot is None:
        raise SchedulingConflict(f"Atividade {activity_id} não está alocada")
    if progress.status in INACTIVE_STATUSES:
        raise SchedulingConflict(f"Atividade {activity_id} está {progress.status}")

    old_status = progress.status
    progress.status = "done"
    progress.completed_at = utcnow()
    progress.current_slot.status = "completed"
    _history(
        session,
        progress,
        "completed",
        slot_id=progress.current_slot_id,
        from_status=old_status,
        to_status="done",
        note=note,
    )
    session.flush()
    return progress


def _next_compatible_slot(
    session: Session,
    activity: Activity,
    previous_slot: StudySlot,
) -> StudySlot | None:
    slots = session.scalars(
        select(StudySlot)
        .where(
            StudySlot.status == "available",
            StudySlot.study_date >= previous_slot.study_date,
        )
        .order_by(StudySlot.study_date, StudySlot.start_time, StudySlot.slot_code)
    ).all()
    for slot in slots:
        is_later = slot.study_date > previous_slot.study_date or (
            slot.study_date == previous_slot.study_date
            and (slot.start_time, slot.slot_code)
            > (previous_slot.start_time, previous_slot.slot_code)
        )
        if is_later and slot.progress is None and is_slot_compatible(activity, slot):
            return slot
    return None


def defer_activity(
    session: Session, activity_id: str, *, note: str = ""
) -> ActivityProgress:
    """Marca não feito, registra história e realoca no próximo slot compatível."""
    activity = session.get(Activity, activity_id)
    progress = session.get(ActivityProgress, activity_id)
    if activity is None or progress is None:
        raise SchedulingError(f"Atividade {activity_id} não encontrada")
    if progress.status == "done":
        raise SchedulingConflict("Atividade concluída não pode ser adiada")
    if progress.current_slot is None:
        raise SchedulingConflict(f"Atividade {activity_id} não está alocada")

    previous_slot = progress.current_slot
    old_status = progress.status
    _history(
        session,
        progress,
        "deferred",
        slot_id=previous_slot.id,
        from_status=old_status,
        to_status="deferred",
        note=note,
    )
    previous_slot.status = "missed"
    progress.current_slot = None
    progress.status = "deferred"
    progress.defer_count += 1
    session.flush()

    # Materializa uma janela suficiente sem depender do frontend ou de WEEKS.
    generate_slots(
        session,
        previous_slot.study_date,
        previous_slot.study_date + timedelta(days=14),
    )
    next_slot = _next_compatible_slot(session, activity, previous_slot)
    if next_slot is None:
        # Se toda a janela materializada estiver ocupada, expande após a última
        # data conhecida. Como a escala alterna diariamente, dois dias contêm
        # pelo menos um FOLGA e um TRABALHO.
        last_date = session.scalar(select(func.max(StudySlot.study_date)))
        extension_start = (last_date or previous_slot.study_date) + timedelta(days=1)
        generate_slots(session, extension_start, extension_start + timedelta(days=1))
        next_slot = _next_compatible_slot(session, activity, previous_slot)
    if next_slot is None:
        raise SchedulingConflict("Nenhum próximo slot compatível encontrado")

    return _assign(
        session,
        activity,
        progress,
        next_slot,
        note="Realocada após atividade não feita",
    )


def set_inactive_status(
    session: Session,
    activity_id: str,
    status: str,
    *,
    note: str = "",
) -> ActivityProgress:
    """Aplica blocked/skipped/cancelled e libera um slot ainda não executado."""
    if status not in INACTIVE_STATUSES:
        raise SchedulingError("status deve ser blocked, skipped ou cancelled")
    progress = session.get(ActivityProgress, activity_id)
    if progress is None:
        raise SchedulingError(f"Atividade {activity_id} não encontrada")
    if progress.status == "done":
        raise SchedulingConflict("Atividade concluída não pode mudar para inativa")
    if progress.status == status:
        return progress

    old_status = progress.status
    slot_id = progress.current_slot_id
    if progress.current_slot is not None:
        progress.current_slot.status = "available"
        progress.current_slot = None
    progress.status = status
    if note:
        progress.note = note
    _history(
        session,
        progress,
        status,
        slot_id=slot_id,
        from_status=old_status,
        to_status=status,
        note=note,
    )
    session.flush()
    return progress


def update_activity_note(
    session: Session, activity_id: str, *, note: str = ""
) -> ActivityProgress:
    """Atualiza a nota sem modificar o estado ou a associação atual."""
    progress = session.get(ActivityProgress, activity_id)
    if progress is None:
        raise SchedulingError(f"Atividade {activity_id} não encontrada")
    progress.note = note
    _history(
        session,
        progress,
        "note_updated",
        slot_id=progress.current_slot_id,
        from_status=progress.status,
        to_status=progress.status,
        note=note,
    )
    session.flush()
    return progress
