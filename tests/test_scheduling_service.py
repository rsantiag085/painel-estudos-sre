from datetime import date

import pytest
from sqlalchemy import select

from models import Activity, ActivityHistory, ActivityProgress, StudySlot
from services.curriculum_seed import seed_curriculum
from services.scale_service import generate_slots
from services.scheduling_service import (
    SchedulingConflict,
    allocate_activity,
    allocate_available_slots,
    allocate_next,
    complete_activity,
    defer_activity,
    is_slot_compatible,
    mark_in_progress,
    next_eligible_activity,
    set_inactive_status,
)


def prepare(session, start="2030-01-01", end="2030-01-05"):
    seed_curriculum(session)
    generate_slots(session, start, end)


def test_next_eligible_activity_is_ordered_by_sequence(session):
    prepare(session)

    first = next_eligible_activity(session)

    assert first.id == "linux-admin-001"
    assert first.sequence == 1


def test_activity_prerequisite_must_be_done(session):
    prepare(session)
    activity = session.get(Activity, "linux-admin-002")
    activity.prerequisites = ["linux-admin-001"]
    session.flush()

    with pytest.raises(SchedulingConflict, match="Pré-requisitos"):
        allocate_activity(session, activity.id, "2030-01-01-F1")

    session.get(ActivityProgress, "linux-admin-001").status = "done"
    session.flush()
    progress = allocate_activity(session, activity.id, "2030-01-01-F1")
    assert progress.current_slot_id == "2030-01-01-F1"


def test_course_prerequisite_must_be_completed(session):
    prepare(session)
    network_activity = "networks-devops-001"

    with pytest.raises(SchedulingConflict, match="Pré-requisitos"):
        allocate_activity(session, network_activity, "2030-01-01-F1")

    linux_ids = session.scalars(
        select(Activity.id).where(Activity.course_id == "linux-admin")
    ).all()
    for activity_id in linux_ids:
        session.get(ActivityProgress, activity_id).status = "done"
    session.flush()

    progress = allocate_activity(session, network_activity, "2030-01-01-F1")
    assert progress.current_slot_id == "2030-01-01-F1"


def test_allocate_next_uses_first_compatible_activity(session):
    prepare(session)

    progress = allocate_next(session, "2030-01-01-F1")

    # A atividade 001 é prática; F1 recebe a próxima atividade teórica elegível.
    assert progress.activity_id == "linux-admin-002"
    assert progress.current_slot_id == "2030-01-01-F1"
    assert session.get(StudySlot, "2030-01-01-F1").status == "scheduled"


def test_duplicate_allocation_is_rejected_and_history_is_not_duplicated(session):
    prepare(session)
    allocate_activity(session, "linux-admin-001", "2030-01-01-F3")

    # Repetir exatamente a mesma associação é idempotente.
    allocate_activity(session, "linux-admin-001", "2030-01-01-F3")
    assert session.query(ActivityHistory).filter_by(event_type="scheduled").count() == 1

    with pytest.raises(SchedulingConflict, match="já possui slot"):
        allocate_activity(session, "linux-admin-001", "2030-01-01-F4")
    with pytest.raises(SchedulingConflict, match="não está disponível"):
        allocate_next(session, "2030-01-01-F3")


def test_in_progress_keeps_its_slot_while_other_slots_are_allocated(session):
    prepare(session)
    allocate_activity(session, "linux-admin-001", "2030-01-01-F3")
    progress = mark_in_progress(session, "linux-admin-001")

    allocate_available_slots(session, date(2030, 1, 1), date(2030, 1, 2))

    assert progress.status == "in_progress"
    assert progress.current_slot_id == "2030-01-01-F3"
    assert session.get(StudySlot, "2030-01-01-F3").status == "scheduled"


def test_completed_activity_stays_associated_and_never_returns_to_queue(session):
    prepare(session)
    allocate_activity(session, "linux-admin-001", "2030-01-01-F3")

    progress = complete_activity(session, "linux-admin-001", note="feito")

    assert progress.status == "done"
    assert progress.current_slot_id == "2030-01-01-F3"
    assert progress.completed_at is not None
    assert progress.current_slot.status == "completed"
    assert next_eligible_activity(session).id != progress.activity_id
    with pytest.raises(SchedulingConflict, match="concluída"):
        defer_activity(session, progress.activity_id)


def test_not_done_becomes_deferred_and_moves_to_next_compatible_slot(session):
    prepare(session)
    allocate_activity(session, "linux-admin-001", "2030-01-01-F3")

    progress = defer_activity(session, "linux-admin-001", note="imprevisto")

    assert progress.status == "deferred"
    assert progress.defer_count == 1
    assert progress.current_slot_id == "2030-01-01-F4"
    assert session.get(StudySlot, "2030-01-01-F3").status == "missed"
    assert session.get(StudySlot, "2030-01-01-F4").status == "scheduled"
    deferred_event = session.scalars(
        select(ActivityHistory).where(ActivityHistory.event_type == "deferred")
    ).one()
    assert deferred_event.study_slot_id == "2030-01-01-F3"
    assert deferred_event.note == "imprevisto"


def test_repeated_defer_appends_history_without_moving_old_records(session):
    prepare(session)
    allocate_activity(session, "linux-admin-001", "2030-01-01-F3")
    defer_activity(session, "linux-admin-001", note="primeiro")
    first_event = session.scalars(
        select(ActivityHistory).where(ActivityHistory.event_type == "deferred")
    ).one()
    first_snapshot = (first_event.id, first_event.study_slot_id, first_event.note)

    progress = defer_activity(session, "linux-admin-001", note="segundo")
    events = session.scalars(
        select(ActivityHistory)
        .where(ActivityHistory.event_type == "deferred")
        .order_by(ActivityHistory.id)
    ).all()

    assert len(events) == 2
    assert (events[0].id, events[0].study_slot_id, events[0].note) == first_snapshot
    assert events[1].study_slot_id == "2030-01-01-F4"
    # F2 aceita exercício/prática e é o primeiro slot compatível da folga.
    assert progress.current_slot_id == "2030-01-03-F2"
    assert progress.defer_count == 2


def test_defer_expands_schedule_when_materialized_window_is_full(session):
    prepare(session, end="2030-01-15")
    allocate_activity(session, "linux-admin-001", "2030-01-01-F3")
    activity = session.get(Activity, "linux-admin-001")

    future_slots = session.scalars(
        select(StudySlot).where(
            StudySlot.study_date >= date(2030, 1, 1),
            StudySlot.id != "2030-01-01-F3",
        )
    ).all()
    for slot in future_slots:
        if is_slot_compatible(activity, slot):
            slot.status = "scheduled"
    session.flush()

    progress = defer_activity(session, activity.id)

    assert progress.current_slot_id == "2030-01-17-F2"
    assert session.get(StudySlot, "2030-01-17-F2").status == "scheduled"


@pytest.mark.parametrize("status", ["blocked", "skipped", "cancelled"])
def test_inactive_statuses_are_allowed_release_slot_and_leave_queue(session, status):
    prepare(session)
    allocate_activity(session, "linux-admin-001", "2030-01-01-F3")

    progress = set_inactive_status(
        session, "linux-admin-001", status, note="decisão"
    )

    assert progress.status == status
    assert progress.current_slot_id is None
    assert session.get(StudySlot, "2030-01-01-F3").status == "available"
    assert next_eligible_activity(session).id != "linux-admin-001"
    event = session.scalars(
        select(ActivityHistory).where(ActivityHistory.event_type == status)
    ).one()
    assert event.study_slot_id == "2030-01-01-F3"


def test_flexible_slot_compatibility_for_aws_and_reading(session):
    prepare(session)
    activity = session.get(Activity, "linux-admin-001")
    f4 = session.get(StudySlot, "2030-01-01-F4")
    t2 = session.get(StudySlot, "2030-01-02-T2")
    f1 = session.get(StudySlot, "2030-01-01-F1")

    activity.preferred_slot = "AWS"
    assert is_slot_compatible(activity, f4)
    assert is_slot_compatible(activity, t2)
    assert not is_slot_compatible(activity, f1)

    activity.preferred_slot = "READING"
    assert is_slot_compatible(activity, f4)
    assert is_slot_compatible(activity, t2)
