"""
routers/progress.py — CRUD de progresso por lição
"""
from fastapi import APIRouter, Depends, HTTPException, Query
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


# ── v2.0 — Novos endpoints ────────────────────────────────────────────────────

@router.get("/week/{week_num}")
def get_week_progress(week_num: int, db: Session = Depends(get_db)):
    """Retorna progresso de todas as lições de uma semana específica."""
    from data.curriculum import WEEKS
    week_data = WEEKS.get(week_num)
    if not week_data:
        raise HTTPException(status_code=404, detail=f"Semana {week_num} não encontrada")

    progress_map = {
        r.lesson_id: {"status": r.status, "note": r.note}
        for r in db.query(LessonProgress).all()
    }

    lessons = []
    for date, date_data in sorted(week_data["dates"].items()):
        for idx, lesson in enumerate(date_data["lessons"]):
            lid = f"{date}-{idx}"
            p = progress_map.get(lid, {"status": "pending", "note": ""})
            lessons.append({
                "lesson_id": lid,
                "date": date,
                "day_type": date_data["type"],
                "name": lesson["name"],
                "hours": lesson["h"],
                "type": lesson.get("type", "aula"),
                "tag": lesson.get("tag"),
                "block": lesson.get("block", "manha"),
                "status": p["status"],
                "note": p["note"] or "",
            })

    done = sum(1 for l in lessons if l["status"] == "done")
    return {
        "week_num": week_num,
        "label": week_data.get("label", f"S{week_num:02d}"),
        "focus": week_data.get("focus", ""),
        "total": len(lessons),
        "done": done,
        "pct": round(done / len(lessons) * 100) if lessons else 0,
        "lessons": lessons,
    }


@router.get("/labs")
def get_zabbix_labs(db: Session = Depends(get_db)):
    """Retorna somente os Labs Zabbix com seu progresso."""
    from data.curriculum import WEEKS
    progress_map = {
        r.lesson_id: {"status": r.status, "note": r.note}
        for r in db.query(LessonProgress).all()
    }

    labs = []
    for week_num, week_data in sorted(WEEKS.items()):
        for date, date_data in sorted(week_data["dates"].items()):
            for idx, lesson in enumerate(date_data["lessons"]):
                if lesson.get("tag") == "zabbix":
                    lid = f"{date}-{idx}"
                    p = progress_map.get(lid, {"status": "pending", "note": ""})
                    labs.append({
                        "lesson_id": lid,
                        "week_num": week_num,
                        "label": week_data.get("label", f"S{week_num:02d}"),
                        "date": date,
                        "name": lesson["name"],
                        "hours": lesson["h"],
                        "status": p["status"],
                        "note": p["note"] or "",
                    })

    done = sum(1 for l in labs if l["status"] == "done")
    return {
        "total": len(labs),
        "done": done,
        "pct": round(done / len(labs) * 100) if labs else 0,
        "labs": labs,
    }


@router.get("/next")
def get_next_lessons(limit: int = Query(3, ge=1, le=20), db: Session = Depends(get_db)):
    """Retorna as próximas N lições pendentes."""
    from data.curriculum import WEEKS
    progress_map = {r.lesson_id: r.status for r in db.query(LessonProgress).all()}

    pending = []
    for week_num, week_data in sorted(WEEKS.items()):
        for date, date_data in sorted(week_data["dates"].items()):
            for idx, lesson in enumerate(date_data["lessons"]):
                lid = f"{date}-{idx}"
                if progress_map.get(lid, "pending") == "pending":
                    pending.append({
                        "lesson_id": lid,
                        "week_num": week_num,
                        "label": week_data.get("label", f"S{week_num:02d}"),
                        "date": date,
                        "name": lesson["name"],
                        "hours": lesson["h"],
                        "tag": lesson.get("tag"),
                        "type": lesson.get("type", "aula"),
                    })
                    if len(pending) >= limit:
                        return pending
    return pending
