from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import ActivityHistory
from schemas import ActivityHistoryResponse

router = APIRouter(prefix="/api/history", tags=["history"])


@router.get("", response_model=list[ActivityHistoryResponse])
async def list_history(
    activity_id: str | None = None,
    event_type: str | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    statement = select(ActivityHistory).order_by(
        ActivityHistory.created_at.desc(), ActivityHistory.id.desc()
    )
    if activity_id is not None:
        statement = statement.where(ActivityHistory.activity_id == activity_id)
    if event_type is not None:
        statement = statement.where(ActivityHistory.event_type == event_type)
    return db.scalars(statement.offset(offset).limit(limit)).all()
