"""
routers/deferred.py — Lições puladas realocadas para próximo dia de FOLGA.
"""
from datetime import date, timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import DeferredLesson
from schemas import DeferredLessonUpdate, DeferredLessonResponse
from data.curriculum import get_day_type

router = APIRouter(prefix="/api/deferred", tags=["deferred"])


def find_next_folga(from_date: str) -> str:
    """Retorna a string ISO da próxima FOLGA após from_date."""
    d = date.fromisoformat(from_date) + timedelta(days=1)
    for _ in range(365):
        if get_day_type(str(d)) == "FOLGA":
            return str(d)
        d += timedelta(days=1)
    raise ValueError(f"Nenhuma FOLGA encontrada após {from_date}")


@router.get("", response_model=list[DeferredLessonResponse])
def list_deferred(db: Session = Depends(get_db)):
    """Lista todas as lições diferidas pendentes, ordenadas por target_date."""
    rows = (
        db.query(DeferredLesson)
        .filter(DeferredLesson.status == "pending")
        .order_by(DeferredLesson.target_date, DeferredLesson.id)
        .all()
    )
    return rows


@router.get("/date/{target_date}", response_model=list[DeferredLessonResponse])
def list_deferred_by_date(target_date: str, db: Session = Depends(get_db)):
    """Lista lições diferidas pendentes para uma data específica."""
    rows = (
        db.query(DeferredLesson)
        .filter(
            DeferredLesson.target_date == target_date,
            DeferredLesson.status == "pending",
        )
        .order_by(DeferredLesson.id)
        .all()
    )
    return rows


@router.post("/{deferred_id}", response_model=DeferredLessonResponse)
def update_deferred(
    deferred_id: int,
    payload: DeferredLessonUpdate,
    db: Session = Depends(get_db),
):
    """
    Marca uma lição diferida como 'done' ou 'skipped'.
    Se 'skipped', cria automaticamente uma nova entrada para o próximo FOLGA.
    """
    if payload.status not in ("done", "skipped"):
        raise HTTPException(status_code=422, detail="status deve ser: done | skipped")

    row = db.query(DeferredLesson).filter(DeferredLesson.id == deferred_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Lição diferida não encontrada")

    row.status = payload.status
    row.note = payload.note or ""
    db.commit()

    if payload.status == "skipped":
        next_folga = find_next_folga(row.target_date)
        new_row = DeferredLesson(
            original_lesson_id=row.original_lesson_id,
            lesson_name=row.lesson_name,
            lesson_hours=row.lesson_hours,
            lesson_type=row.lesson_type,
            lesson_tag=row.lesson_tag,
            lesson_block=row.lesson_block,
            target_date=next_folga,
            status="pending",
        )
        db.add(new_row)
        db.commit()
        db.refresh(new_row)
        return new_row

    db.refresh(row)
    return row
