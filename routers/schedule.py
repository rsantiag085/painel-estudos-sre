from collections import defaultdict
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import StudySlot
from routers.serializers import activity_view, slot_view
from schemas import (
    ActivityView,
    AllocationRequest,
    ScheduleDayResponse,
    ScheduleGenerateRequest,
    ScheduleGenerateResponse,
    ScheduleRangeResponse,
)
from services.scale_service import day_type_for, generate_slots
from services.scheduling_service import (
    SchedulingConflict,
    SchedulingError,
    allocate_activity,
    allocate_available_slots,
    allocate_next,
)

router = APIRouter(prefix="/api/schedule", tags=["schedule"])


def _schedule_days(slots, start_date, end_date):
    grouped = defaultdict(list)
    for slot in slots:
        grouped[slot.study_date].append(slot_view(slot))
    days = []
    current = start_date
    from datetime import timedelta
    while current <= end_date:
        days.append({
            "date": current,
            "day_type": day_type_for(current),
            "slots": grouped[current],
        })
        current += timedelta(days=1)
    return days


def _slots_in_range(db, start_date, end_date):
    return db.scalars(
        select(StudySlot)
        .where(StudySlot.study_date.between(start_date, end_date))
        .order_by(StudySlot.study_date, StudySlot.start_time, StudySlot.slot_code)
    ).all()


@router.post("/generate", response_model=ScheduleGenerateResponse)
async def generate_schedule(payload: ScheduleGenerateRequest, db: Session = Depends(get_db)):
    end_date = payload.end_date or payload.start_date
    try:
        result = generate_slots(db, payload.start_date, end_date)
        allocations = (
            allocate_available_slots(db, payload.start_date, end_date)
            if payload.allocate
            else []
        )
        db.commit()
    except (ValueError, SchedulingError) as error:
        db.rollback()
        raise HTTPException(status_code=409, detail=str(error)) from error
    return {
        **result.__dict__,
        "slots_total": result.slots_total,
        "activities_allocated": len(allocations),
    }


@router.get("/today", response_model=ScheduleDayResponse)
async def get_today(
    on_date: date = Query(default_factory=date.today, alias="date"),
    db: Session = Depends(get_db),
):
    slots = _slots_in_range(db, on_date, on_date)
    return _schedule_days(slots, on_date, on_date)[0]


@router.get("/range", response_model=ScheduleRangeResponse)
async def get_schedule_range(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db),
):
    if end_date < start_date:
        raise HTTPException(status_code=422, detail="Intervalo de datas inválido")
    slots = _slots_in_range(db, start_date, end_date)
    return {
        "start_date": start_date,
        "end_date": end_date,
        "days": _schedule_days(slots, start_date, end_date),
    }


@router.post("/slots/{slot_id}/allocate", response_model=ActivityView | None)
async def allocate_slot(
    slot_id: str,
    payload: AllocationRequest,
    db: Session = Depends(get_db),
):
    try:
        progress = (
            allocate_activity(db, payload.activity_id, slot_id, note=payload.note)
            if payload.activity_id
            else allocate_next(db, slot_id, note=payload.note)
        )
        db.commit()
    except SchedulingConflict as error:
        db.rollback()
        raise HTTPException(status_code=409, detail=str(error)) from error
    except SchedulingError as error:
        db.rollback()
        raise HTTPException(status_code=404, detail=str(error)) from error
    if progress is None:
        return None
    return activity_view(progress.activity, progress)
