"""Seed idempotente do catálogo definido em data.curriculum.

O currículo Python continua sendo a fonte de verdade. As tabelas ``courses`` e
``activities`` são snapshots consultáveis; estados mutáveis ficam separados em
``activity_progress``. Este serviço não remove registros que tenham desaparecido
do catálogo, evitando perda silenciosa durante uma atualização.
"""

from dataclasses import dataclass
from json import dumps

from sqlalchemy.orm import Session

from data.curriculum import ACTIVITIES, COURSES, validate_curriculum
from models import Activity, ActivityProgress, AppSetting, Course


@dataclass(frozen=True)
class SeedResult:
    courses_created: int = 0
    courses_updated: int = 0
    activities_created: int = 0
    activities_updated: int = 0
    progress_created: int = 0


COURSE_FIELDS = (
    "name",
    "provider",
    "url",
    "video_hours",
    "priority",
    "execution",
    "phase",
    "status",
    "prerequisites",
    "notes",
)

ACTIVITY_FIELDS = (
    "course_id",
    "sequence",
    "name",
    "duration_minutes",
    "activity_type",
    "preferred_day_type",
    "preferred_slot",
    "prerequisites",
    "tags",
    "required",
)


def _copy_mutable(value):
    return list(value) if isinstance(value, list) else value


def _update_changed(row, source: dict, fields: tuple[str, ...]) -> bool:
    changed = False
    for field in fields:
        value = _copy_mutable(source[field])
        if getattr(row, field) != value:
            setattr(row, field, value)
            changed = True
    return changed


def _set_setting(session: Session, key: str, value: str) -> None:
    setting = session.get(AppSetting, key)
    if setting is None:
        session.add(AppSetting(key=key, value=value))
    elif setting.value != value:
        setting.value = value


def seed_curriculum(session: Session) -> SeedResult:
    """Sincroniza catálogo e cria progresso inicial, sem executar commit.

    O chamador controla a transação. Assim, cursos, atividades, progresso e
    metadados do seed são confirmados ou revertidos como uma única unidade.
    """
    validation_errors = validate_curriculum()
    if validation_errors:
        raise ValueError("Currículo inválido: " + "; ".join(validation_errors))

    counts = {
        "courses_created": 0,
        "courses_updated": 0,
        "activities_created": 0,
        "activities_updated": 0,
        "progress_created": 0,
    }

    for source in COURSES:
        row = session.get(Course, source["id"])
        if row is None:
            row = Course(
                id=source["id"],
                **{
                    field: _copy_mutable(source[field])
                    for field in COURSE_FIELDS
                },
            )
            session.add(row)
            counts["courses_created"] += 1
        elif _update_changed(row, source, COURSE_FIELDS):
            counts["courses_updated"] += 1

    # Garante que os FKs de curso existam antes de inserir atividades.
    session.flush()

    for source in ACTIVITIES:
        row = session.get(Activity, source["id"])
        if row is None:
            row = Activity(
                id=source["id"],
                **{
                    field: _copy_mutable(source[field])
                    for field in ACTIVITY_FIELDS
                },
            )
            session.add(row)
            counts["activities_created"] += 1
        elif _update_changed(row, source, ACTIVITY_FIELDS):
            counts["activities_updated"] += 1

    session.flush()

    for source in ACTIVITIES:
        if session.get(ActivityProgress, source["id"]) is None:
            session.add(
                ActivityProgress(activity_id=source["id"], status="pending")
            )
            counts["progress_created"] += 1

    _set_setting(session, "curriculum.schema_version", "3.0")
    _set_setting(session, "curriculum.course_count", str(len(COURSES)))
    _set_setting(session, "curriculum.activity_count", str(len(ACTIVITIES)))
    _set_setting(
        session,
        "curriculum.source",
        dumps({"module": "data.curriculum", "weeks_used": False}),
    )
    session.flush()

    return SeedResult(**counts)
