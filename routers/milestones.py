"""
routers/milestones.py — Checkboxes de milestone por fase
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Milestone
from schemas import MilestoneUpdate, MilestoneResponse

router = APIRouter(prefix="/api/milestones", tags=["milestones"])


@router.get("", response_model=list[MilestoneResponse])
def list_milestones(db: Session = Depends(get_db)):
    """Lista todos os milestones agrupados por fase."""
    rows = db.query(Milestone).order_by(Milestone.phase_num, Milestone.id).all()
    return [
        MilestoneResponse(
            id=r.id,
            phase_num=r.phase_num,
            label=r.label,
            done=r.done,
            updated_at=r.updated_at,
        )
        for r in rows
    ]


@router.post("/{milestone_id}", response_model=MilestoneResponse)
def update_milestone(
    milestone_id: int,
    payload: MilestoneUpdate,
    db: Session = Depends(get_db),
):
    """Atualiza o status done/pending de um milestone."""
    row = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not row:
        raise HTTPException(status_code=404, detail="Milestone não encontrado")

    row.done = payload.done
    row.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(row)

    return MilestoneResponse(
        id=row.id,
        phase_num=row.phase_num,
        label=row.label,
        done=row.done,
        updated_at=row.updated_at,
    )
