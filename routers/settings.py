"""Configuração inicial e preferências da instalação."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from database import get_db
from models import StudySlot
from schemas import UserSettingsRequest, UserSettingsResponse
from services.settings_service import get_settings, save_settings


router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("", response_model=UserSettingsResponse)
async def read_settings(db: Session = Depends(get_db)):
    return get_settings(db)


@router.put("", response_model=UserSettingsResponse)
async def update_settings(
    payload: UserSettingsRequest,
    db: Session = Depends(get_db),
):
    current = get_settings(db)
    scale_changed = (
        payload.work_schedule != current["work_schedule"]
        or payload.anchor_date != current["anchor_date"]
        or payload.anchor_day_type != current["anchor_day_type"]
        or payload.start_date != current["start_date"]
        or payload.study_days != current["study_days"]
        or payload.daily_study_minutes != current["daily_study_minutes"]
    )
    if current["configured"] and scale_changed:
        future_slots = db.scalar(
            select(func.count())
            .select_from(StudySlot)
            .where(StudySlot.study_date >= current["start_date"])
        )
        if future_slots:
            raise HTTPException(
                status_code=409,
                detail="A escala possui agenda materializada. Limpe os slots futuros antes de alterá-la.",
            )
    result = save_settings(db, payload.model_dump())
    db.commit()
    return result
