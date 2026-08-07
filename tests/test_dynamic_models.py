from datetime import date

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError

from models import ActivityHistory, StudySlot
from schemas import ActivityHistoryResponse, StudySlotResponse
from services.curriculum_seed import seed_curriculum


def test_new_and_legacy_tables_coexist(session):
    table_names = set(inspect(session.get_bind()).get_table_names())

    assert {
        "courses",
        "activities",
        "study_slots",
        "activity_progress",
        "activity_history",
        "app_settings",
    }.issubset(table_names)
    assert {
        "lesson_progress",
        "week_notes",
        "milestones",
        "deferred_lessons",
    }.issubset(table_names)


def test_slot_unique_per_date_and_code(session):
    session.add_all([
        StudySlot(
            id="2026-08-05-F1",
            study_date=date(2026, 8, 5),
            day_type="FOLGA",
            slot_code="F1",
            start_time="13:30",
            duration_minutes=30,
            slot_type="THEORY",
        ),
        StudySlot(
            id="outro-id",
            study_date=date(2026, 8, 5),
            day_type="FOLGA",
            slot_code="F1",
            start_time="14:00",
            duration_minutes=30,
            slot_type="THEORY",
        ),
    ])

    with pytest.raises(IntegrityError):
        session.flush()


def test_history_and_pydantic_responses_from_orm(session):
    seed_curriculum(session)
    slot = StudySlot(
        id="2026-08-05-F1",
        study_date=date(2026, 8, 5),
        day_type="FOLGA",
        slot_code="F1",
        start_time="13:30",
        duration_minutes=30,
        slot_type="THEORY",
    )
    session.add(slot)
    session.flush()
    event = ActivityHistory(
        activity_id="linux-admin-001",
        study_slot_id=slot.id,
        event_type="scheduled",
        from_status="pending",
        to_status="pending",
    )
    session.add(event)
    session.flush()

    slot_schema = StudySlotResponse.model_validate(slot)
    event_schema = ActivityHistoryResponse.model_validate(event)

    assert slot_schema.study_date == date(2026, 8, 5)
    assert event_schema.activity_id == "linux-admin-001"
    assert event_schema.study_slot_id == slot.id
