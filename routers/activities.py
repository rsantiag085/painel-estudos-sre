from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Activity, ActivityHistory, ActivityProgress, Course, StudySlot
from routers.serializers import activity_view
from schemas import ActivityCommandRequest, ActivityHistoryResponse, ActivityView
from services.scheduling_service import (
    SchedulingConflict,
    SchedulingError,
    complete_activity,
    defer_activity,
    mark_in_progress,
    next_eligible_activity,
    reopen_activity,
    set_inactive_status,
    update_activity_note,
)

router = APIRouter(prefix="/api/activities", tags=["activities"])


def _map_scheduling_error(error: SchedulingError):
    status_code = 409 if isinstance(error, SchedulingConflict) else 404
    raise HTTPException(status_code=status_code, detail=str(error)) from error


def _command(db: Session, operation, activity_id: str, note: str):
    try:
        progress = operation(db, activity_id, note=note)
        db.commit()
        activity = db.get(Activity, activity_id)
        progress = db.get(ActivityProgress, activity_id)
        return activity_view(activity, progress)
    except SchedulingError as error:
        db.rollback()
        _map_scheduling_error(error)


@router.get("", response_model=list[ActivityView])
async def list_activities(
    course_id: str | None = None,
    phase: int | None = Query(default=None, ge=1, le=5),
    status: str | None = None,
    tag: str | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    statement = (
        select(Activity, ActivityProgress)
        .join(ActivityProgress, ActivityProgress.activity_id == Activity.id)
        .join(Course, Course.id == Activity.course_id)
        .order_by(Activity.sequence, Activity.id)
    )
    if course_id is not None:
        statement = statement.where(Activity.course_id == course_id)
    if phase is not None:
        statement = statement.where(Course.phase == phase)
    if status is not None:
        statement = statement.where(ActivityProgress.status == status)
    rows = db.execute(statement).all()
    if tag is not None:
        rows = [(a, p) for a, p in rows if tag in (a.tags or [])]
    return [activity_view(a, p) for a, p in rows[offset : offset + limit]]


@router.get("/next", response_model=ActivityView | None)
async def get_next_activity(
    slot_id: str | None = None,
    db: Session = Depends(get_db),
):
    slot = None
    if slot_id is not None:
        slot = db.get(StudySlot, slot_id)
        if slot is None:
            raise HTTPException(status_code=404, detail="Slot não encontrado")
    activity = next_eligible_activity(db, slot)
    if activity is None:
        return None
    return activity_view(activity, db.get(ActivityProgress, activity.id))


@router.get("/{activity_id}/history", response_model=list[ActivityHistoryResponse])
async def get_activity_history(activity_id: str, db: Session = Depends(get_db)):
    if db.get(Activity, activity_id) is None:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return db.scalars(
        select(ActivityHistory)
        .where(ActivityHistory.activity_id == activity_id)
        .order_by(ActivityHistory.created_at, ActivityHistory.id)
    ).all()


@router.get("/{activity_id}", response_model=ActivityView)
async def get_activity(activity_id: str, db: Session = Depends(get_db)):
    activity = db.get(Activity, activity_id)
    progress = db.get(ActivityProgress, activity_id)
    if activity is None or progress is None:
        raise HTTPException(status_code=404, detail="Atividade não encontrada")
    return activity_view(activity, progress)


@router.post("/{activity_id}/start", response_model=ActivityView)
async def start_activity(
    activity_id: str,
    payload: ActivityCommandRequest,
    db: Session = Depends(get_db),
):
    return _command(db, mark_in_progress, activity_id, payload.note)


@router.post("/{activity_id}/complete", response_model=ActivityView)
async def finish_activity(
    activity_id: str,
    payload: ActivityCommandRequest,
    db: Session = Depends(get_db),
):
    return _command(db, complete_activity, activity_id, payload.note)


@router.post("/{activity_id}/defer", response_model=ActivityView)
async def postpone_activity(
    activity_id: str,
    payload: ActivityCommandRequest,
    db: Session = Depends(get_db),
):
    return _command(db, defer_activity, activity_id, payload.note)


def _inactive_command(status):
    def operation(db, activity_id, *, note=""):
        return set_inactive_status(db, activity_id, status, note=note)

    return operation


@router.post("/{activity_id}/block", response_model=ActivityView)
async def block_activity(activity_id: str, payload: ActivityCommandRequest, db=Depends(get_db)):
    return _command(db, _inactive_command("blocked"), activity_id, payload.note)


@router.post("/{activity_id}/skip", response_model=ActivityView)
async def skip_activity(activity_id: str, payload: ActivityCommandRequest, db=Depends(get_db)):
    return _command(db, _inactive_command("skipped"), activity_id, payload.note)


@router.post("/{activity_id}/cancel", response_model=ActivityView)
async def cancel_activity(activity_id: str, payload: ActivityCommandRequest, db=Depends(get_db)):
    return _command(db, _inactive_command("cancelled"), activity_id, payload.note)


@router.post("/{activity_id}/note", response_model=ActivityView)
async def save_activity_note(
    activity_id: str,
    payload: ActivityCommandRequest,
    db: Session = Depends(get_db),
):
    return _command(db, update_activity_note, activity_id, payload.note)


@router.post("/{activity_id}/reopen", response_model=ActivityView)
async def reopen_activity_endpoint(
    activity_id: str,
    payload: ActivityCommandRequest,
    db: Session = Depends(get_db),
):
    return _command(db, reopen_activity, activity_id, payload.note)
