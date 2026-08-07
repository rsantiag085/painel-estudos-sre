"""Estatísticas, progresso e backup sem dependência de WEEKS."""

from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import (
    Activity,
    ActivityHistory,
    ActivityProgress,
    AppSetting,
    Course,
    LessonProgress,
    Milestone,
    StudySlot,
    WeekNote,
)
from schemas import DynamicStatsResponse, ProgressGroup, ProgressSummaryResponse
from services.reporting_service import (
    full_stats,
    progress_by_course,
    progress_by_phase,
    progress_summary,
)

router = APIRouter(prefix="/api", tags=["progress"])


@router.get("/stats", response_model=DynamicStatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    return full_stats(db)


@router.get("/progress/summary", response_model=ProgressSummaryResponse)
async def get_progress_summary(db: Session = Depends(get_db)):
    return progress_summary(db)


@router.get("/progress/phases", response_model=list[ProgressGroup])
async def get_progress_phases(db: Session = Depends(get_db)):
    return progress_by_phase(db)


@router.get("/progress/courses", response_model=list[ProgressGroup])
async def get_progress_courses(db: Session = Depends(get_db)):
    return progress_by_course(db)


@router.get("/progress")
async def legacy_progress_adapter(db: Session = Depends(get_db)):
    """Compatibilidade somente leitura; IDs agora são permanentes."""
    rows = db.scalars(
        select(ActivityProgress).order_by(ActivityProgress.activity_id)
    ).all()
    return [
        {
            "lesson_id": row.activity_id,
            "status": row.status,
            "note": row.note or "",
            "updated_at": row.updated_at,
        }
        for row in rows
    ]


@router.get("/export")
async def export_data(db: Session = Depends(get_db)):
    """Exporta dados novos e mantém as chaves do backup legado."""
    legacy_progress = db.scalars(select(LessonProgress)).all()
    notes = db.scalars(select(WeekNote)).all()
    milestones = db.scalars(select(Milestone)).all()
    courses = db.scalars(select(Course).order_by(Course.id)).all()
    activities = db.scalars(select(Activity).order_by(Activity.sequence)).all()
    progress = db.scalars(select(ActivityProgress).order_by(ActivityProgress.activity_id)).all()
    slots = db.scalars(select(StudySlot).order_by(StudySlot.study_date, StudySlot.slot_code)).all()
    history = db.scalars(select(ActivityHistory).order_by(ActivityHistory.id)).all()
    settings = db.scalars(select(AppSetting).order_by(AppSetting.key)).all()

    return {
        "schema_version": "3.0",
        "exported_at": datetime.now(UTC).isoformat(),
        # Chaves legadas preservadas.
        "progress": [
            {
                "lesson_id": row.lesson_id,
                "status": row.status,
                "note": row.note,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None,
            }
            for row in legacy_progress
        ],
        "week_notes": [
            {
                "week_num": row.week_num,
                "note": row.note,
                "updated_at": row.updated_at.isoformat() if row.updated_at else None,
            }
            for row in notes
        ],
        "milestones": [
            {
                "id": row.id,
                "phase_num": row.phase_num,
                "label": row.label,
                "done": row.done,
            }
            for row in milestones
        ],
        "dynamic": {
            "courses": [
                {
                    "id": row.id,
                    "name": row.name,
                    "provider": row.provider,
                    "url": row.url,
                    "video_hours": row.video_hours,
                    "priority": row.priority,
                    "execution": row.execution,
                    "phase": row.phase,
                    "status": row.status,
                    "prerequisites": row.prerequisites or [],
                    "notes": row.notes,
                }
                for row in courses
            ],
            "activities": [
                {
                    "id": row.id,
                    "course_id": row.course_id,
                    "sequence": row.sequence,
                    "name": row.name,
                    "duration_minutes": row.duration_minutes,
                    "activity_type": row.activity_type,
                    "preferred_day_type": row.preferred_day_type,
                    "preferred_slot": row.preferred_slot,
                    "prerequisites": row.prerequisites or [],
                    "tags": row.tags or [],
                    "required": row.required,
                }
                for row in activities
            ],
            "activity_progress": [
                {
                    "activity_id": row.activity_id,
                    "status": row.status,
                    "note": row.note,
                    "current_slot_id": row.current_slot_id,
                    "defer_count": row.defer_count,
                    "started_at": row.started_at.isoformat() if row.started_at else None,
                    "completed_at": row.completed_at.isoformat() if row.completed_at else None,
                    "updated_at": row.updated_at.isoformat() if row.updated_at else None,
                }
                for row in progress
            ],
            "study_slots": [
                {
                    "id": row.id,
                    "study_date": row.study_date.isoformat(),
                    "day_type": row.day_type,
                    "slot_code": row.slot_code,
                    "start_time": row.start_time,
                    "duration_minutes": row.duration_minutes,
                    "slot_type": row.slot_type,
                    "status": row.status,
                }
                for row in slots
            ],
            "activity_history": [
                {
                    "id": row.id,
                    "activity_id": row.activity_id,
                    "study_slot_id": row.study_slot_id,
                    "event_type": row.event_type,
                    "from_status": row.from_status,
                    "to_status": row.to_status,
                    "note": row.note,
                    "created_at": row.created_at.isoformat(),
                }
                for row in history
            ],
            "app_settings": [
                {"key": row.key, "value": row.value, "updated_at": row.updated_at.isoformat()}
                for row in settings
            ],
        },
    }


@router.post("/import")
async def import_legacy_data(data: dict, db: Session = Depends(get_db)):
    """Mantém restauração v2; dados dinâmicos nunca são apagados por ela."""
    if "progress" in data:
        db.query(LessonProgress).delete()
        for item in data["progress"]:
            db.add(LessonProgress(
                lesson_id=item["lesson_id"],
                status=item["status"],
                note=item.get("note", ""),
            ))
    if "week_notes" in data:
        db.query(WeekNote).delete()
        for item in data["week_notes"]:
            db.add(WeekNote(
                week_num=item["week_num"],
                note=item.get("note", ""),
            ))
    if "milestones" in data:
        db.query(Milestone).update({Milestone.done: False})
        done_labels = {m["label"] for m in data["milestones"] if m.get("done")}
        if done_labels:
            db.query(Milestone).filter(Milestone.label.in_(done_labels)).update(
                {Milestone.done: True}, synchronize_session=False
            )
    db.commit()
    return {
        "status": "success",
        "message": "Dados legados restaurados sem alterar o catálogo dinâmico.",
    }
