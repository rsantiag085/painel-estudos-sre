from datetime import date

import pytest

from models import StudySlot
from services.scale_service import (
    day_type_for,
    generate_slots,
    slot_definitions_for,
)


@pytest.mark.parametrize(
    ("current_date", "expected"),
    [
        (date(2030, 1, 1), "FOLGA"),
        (date(2030, 1, 2), "TRABALHO"),
        (date(2030, 1, 3), "FOLGA"),
        (date(2029, 12, 31), "TRABALHO"),
        (date(2029, 12, 30), "FOLGA"),
        (date(2030, 1, 27), "FOLGA"),
        (date(2030, 1, 28), "TRABALHO"),
    ],
)
def test_day_type_uses_elapsed_days_in_both_directions(current_date, expected):
    assert day_type_for(current_date) == expected
    assert day_type_for(current_date.isoformat()) == expected


def test_alternation_crosses_year_boundary():
    first = date(2026, 12, 31)
    second = date(2027, 1, 1)
    third = date(2027, 1, 2)

    assert day_type_for(first) != day_type_for(second)
    assert day_type_for(first) == day_type_for(third)


def test_slot_definitions_have_exact_required_capacity():
    folga = slot_definitions_for("2030-01-01")
    trabalho = slot_definitions_for("2030-01-02")

    assert [slot["code"] for slot in folga] == ["F1", "F2", "F3", "F4"]
    assert [slot["code"] for slot in trabalho] == ["T1", "T2"]
    assert all(slot["duration_minutes"] == 30 for slot in folga + trabalho)


def test_generate_slots_for_inclusive_range(session):
    result = generate_slots(session, "2029-12-31", "2030-01-03")

    assert result.days_processed == 4
    assert result.slots_created == 12  # T(2) + F(4) + T(2) + F(4)
    assert result.slots_existing == 0
    assert session.query(StudySlot).count() == 12


def test_generation_is_idempotent_for_same_range(session):
    first = generate_slots(session, "2030-01-01", "2030-01-02")
    second = generate_slots(session, "2030-01-01", "2030-01-02")

    assert first.slots_created == 6
    assert second.slots_created == 0
    assert second.slots_existing == 6
    assert session.query(StudySlot).count() == 6


def test_generation_is_idempotent_for_overlapping_ranges(session):
    generate_slots(session, "2030-01-01", "2030-01-03")
    result = generate_slots(session, "2030-01-02", "2030-01-04")

    assert result.slots_existing == 6  # 06/08 (2) + 07/08 (4)
    assert result.slots_created == 2   # somente 08/08
    assert session.query(StudySlot).count() == 12


def test_generation_preserves_existing_slot_state(session):
    generate_slots(session, "2030-01-01")
    slot = session.get(StudySlot, "2030-01-01-F1")
    slot.status = "completed"
    session.flush()

    result = generate_slots(session, "2030-01-01")

    assert result.slots_created == 0
    assert session.get(StudySlot, slot.id).status == "completed"


def test_generation_rejects_reversed_range(session):
    with pytest.raises(ValueError, match="end_date"):
        generate_slots(session, "2030-01-02", "2030-01-01")
