"""
routers/progress.py — CRUD de progresso por lição
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import LessonProgress
from schemas import LessonProgressCreate, LessonProgressResponse

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("", response_model=list[LessonProgressResponse])
def list_progress(db: Session = Depends(get_db)):
    """Lista todo o progresso salvo."""
    rows = db.query(LessonProgress).all()
    return [
        LessonProgressResponse(
            lesson_id=r.lesson_id,
            status=r.status,
            note=r.note or "",
            updated_at=r.updated_at,
        )
        for r in rows
    ]


@router.post("/{lesson_id}", response_model=LessonProgressResponse)
def upsert_progress(
    lesson_id: str,
    payload: LessonProgressCreate,
    db: Session = Depends(get_db),
):
    """Salva ou atualiza o progresso de uma lição."""
    if payload.status not in ("pending", "done", "skipped", "work"):
        raise HTTPException(status_code=422, detail="status deve ser: pending | done | skipped | work")

    row = db.query(LessonProgress).filter(LessonProgress.lesson_id == lesson_id).first()
    if row:
        row.status = payload.status
        row.note = payload.note or ""
        row.updated_at = datetime.utcnow()
    else:
        row = LessonProgress(
            lesson_id=lesson_id,
            status=payload.status,
            note=payload.note or "",
        )
        db.add(row)

    db.commit()
    db.refresh(row)

    return LessonProgressResponse(
        lesson_id=row.lesson_id,
        status=row.status,
        note=row.note or "",
        updated_at=row.updated_at,
    )
