"""Cálculo da escala 12x36 e materialização idempotente de slots.

Não há alocação de atividades neste serviço. Ele apenas traduz a escala definida
em ``data.curriculum`` para linhas ``StudySlot``.
"""

from dataclasses import dataclass
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from data.curriculum import SCALE_ANCHOR, get_day_type, get_slots_for_day
from models import StudySlot


@dataclass(frozen=True)
class SlotGenerationResult:
    start_date: date
    end_date: date
    days_processed: int
    slots_created: int
    slots_existing: int

    @property
    def slots_total(self) -> int:
        return self.slots_created + self.slots_existing


def normalize_date(value: date | str) -> date:
    """Aceita ``date`` ou ISO ``YYYY-MM-DD`` e retorna um ``date``."""
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def day_type_for(value: date | str) -> str:
    """Retorna FOLGA/TRABALHO em relação à âncora configurada."""
    current_date = normalize_date(value)
    elapsed_days = (current_date - SCALE_ANCHOR).days
    return "FOLGA" if elapsed_days % 2 == 0 else "TRABALHO"


def slot_definitions_for(value: date | str) -> list[dict[str, object]]:
    """Retorna somente os quatro/dois slots obrigatórios do dia."""
    current_date = normalize_date(value)
    # Impede divergência silenciosa entre o serviço e a fonte do currículo.
    if day_type_for(current_date) != get_day_type(current_date):
        raise RuntimeError("Regra da escala divergiu de data.curriculum")
    return get_slots_for_day(current_date, include_optional=False)


def _dates_between(start_date: date, end_date: date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)


def generate_slots(
    session: Session,
    start_date: date | str,
    end_date: date | str | None = None,
) -> SlotGenerationResult:
    """Cria slots no intervalo inclusivo sem executar commit.

    Chamadas repetidas ou com intervalos sobrepostos reutilizam os IDs existentes.
    O chamador controla a transação, seguindo o mesmo padrão do seed do catálogo.
    """
    start = normalize_date(start_date)
    end = normalize_date(end_date) if end_date is not None else start
    if end < start:
        raise ValueError("end_date deve ser igual ou posterior a start_date")

    desired: list[dict[str, object]] = []
    for current_date in _dates_between(start, end):
        day_type = day_type_for(current_date)
        for definition in slot_definitions_for(current_date):
            slot_code = str(definition["code"])
            desired.append(
                {
                    "id": f"{current_date.isoformat()}-{slot_code}",
                    "study_date": current_date,
                    "day_type": day_type,
                    "slot_code": slot_code,
                    "start_time": str(definition["start_time"]),
                    "duration_minutes": int(definition["duration_minutes"]),
                    "slot_type": str(definition["slot_type"]),
                }
            )

    desired_ids = {item["id"] for item in desired}
    # Filtrar pela data evita atingir o limite de parâmetros do SQLite em
    # intervalos grandes. A interseção ignora eventuais slots opcionais.
    existing_ids = set(
        session.scalars(
            select(StudySlot.id).where(StudySlot.study_date.between(start, end))
        ).all()
    ) & desired_ids

    for item in desired:
        if item["id"] not in existing_ids:
            session.add(StudySlot(**item, status="available"))

    session.flush()

    return SlotGenerationResult(
        start_date=start,
        end_date=end,
        days_processed=(end - start).days + 1,
        slots_created=len(desired) - len(existing_ids),
        slots_existing=len(existing_ids),
    )
