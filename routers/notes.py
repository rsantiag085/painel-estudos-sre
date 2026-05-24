"""
routers/notes.py — Notas por semana
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import WeekNote
from schemas import WeekNoteCreate, WeekNoteResponse

router = APIRouter(prefix="/api/week", tags=["notes"])


@router.get("/{week_num}/note", response_model=WeekNoteResponse)
def get_week_note(week_num: int, db: Session = Depends(get_db)):
    """Retorna a nota da semana."""
    row = db.query(WeekNote).filter(WeekNote.week_num == week_num).first()
    if not row:
        return WeekNoteResponse(week_num=week_num, note="")
    return WeekNoteResponse(
        week_num=row.week_num,
        note=row.note or "",
        updated_at=row.updated_at,
    )


@router.post("/{week_num}/note", response_model=WeekNoteResponse)
def save_week_note(
    week_num: int,
    payload: WeekNoteCreate,
    db: Session = Depends(get_db),
):
    """Salva ou atualiza a nota de uma semana."""
    row = db.query(WeekNote).filter(WeekNote.week_num == week_num).first()
    if row:
        row.note = payload.note
        row.updated_at = datetime.utcnow()
    else:
        row = WeekNote(week_num=week_num, note=payload.note)
        db.add(row)

    db.commit()
    db.refresh(row)

    return WeekNoteResponse(
        week_num=row.week_num,
        note=row.note or "",
        updated_at=row.updated_at,
    )
