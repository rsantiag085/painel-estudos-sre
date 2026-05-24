"""
routers/stats.py — Endpoint de estatísticas agregadas
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date as date_type

from database import get_db
from models import LessonProgress
from schemas import StatsResponse, PhaseStats
from data.curriculum import PHASES, WEEKS

router = APIRouter(prefix="/api", tags=["stats"])


@router.get("/stats", response_model=StatsResponse)
def get_stats(db: Session = Depends(get_db)):
    progress_map: dict[str, str] = {}
    rows = db.query(LessonProgress).all()
    for r in rows:
        progress_map[r.lesson_id] = r.status

    done = 0
    skipped = 0
    folga_days_studied = 0
    total = 0
    hours_studied = 0.0
    # v2.0 — Labs Zabbix tracking
    labs_total = 0
    labs_done = 0

    by_phase = []
    for phase_num, phase_data in PHASES.items():
        ph_done = 0
        ph_total = 0
        for week_num in phase_data["weeks"]:
            week = WEEKS.get(week_num)
            if not week:
                continue
            for date, date_data in week["dates"].items():
                for idx, lesson in enumerate(date_data["lessons"]):
                    lid = f"{date}-{idx}"
                    status = progress_map.get(lid, "pending")
                    total += 1
                    ph_total += 1
                    # Contar labs Zabbix
                    if lesson.get("tag") == "zabbix":
                        labs_total += 1
                        if status == "done":
                            labs_done += 1
                    if status == "done":
                        done += 1
                        ph_done += 1
                        hours_studied += lesson["h"]
                    elif status == "skipped":
                        skipped += 1

        pct = round(ph_done / ph_total * 100) if ph_total else 0
        by_phase.append(PhaseStats(
            phase=phase_num,
            label=phase_data["label"],
            done=ph_done,
            total=ph_total,
            pct=pct,
        ))

    global_pct = round(done / total * 100) if total else 0

    # v2.0 — Calcular dias restantes até 08/01/2027
    today = date_type.today()
    end_date = date_type(2027, 1, 8)
    days_remaining = max(0, (end_date - today).days)

    return StatsResponse(
        done=done,
        total=total,
        skipped=skipped,
        work_days=folga_days_studied,
        hours_studied=round(hours_studied, 1),
        pct=global_pct,
        by_phase=by_phase,
        # v2.0 extras
        total_labs_zabbix=labs_total,
        labs_completed=labs_done,
        labs_pct=round(labs_done / labs_total * 100) if labs_total else 0,
        days_remaining=days_remaining,
        expected_completion="2027-01-08",
    )



@router.get("/export")
def export_data(db: Session = Depends(get_db)):
    from models import WeekNote, Milestone
    from datetime import datetime

    progress_rows = db.query(LessonProgress).all()
    note_rows = db.query(WeekNote).all()
    milestone_rows = db.query(Milestone).all()

    return {
        "exported_at": datetime.utcnow().isoformat(),
        "progress": [
            {
                "lesson_id": r.lesson_id,
                "status": r.status,
                "note": r.note,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            }
            for r in progress_rows
        ],
        "week_notes": [
            {
                "week_num": r.week_num,
                "note": r.note,
                "updated_at": r.updated_at.isoformat() if r.updated_at else None,
            }
            for r in note_rows
        ],
        "milestones": [
            {
                "id": r.id,
                "phase_num": r.phase_num,
                "label": r.label,
                "done": r.done,
            }
            for r in milestone_rows
        ],
    }


@router.post("/import")
def import_data(data: dict, db: Session = Depends(get_db)):
    from models import LessonProgress, WeekNote, Milestone

    if "progress" in data:
        db.query(LessonProgress).delete()
        for p in data["progress"]:
            db.add(LessonProgress(
                lesson_id=p["lesson_id"],
                status=p["status"],
                note=p.get("note", "")
            ))

    if "week_notes" in data:
        db.query(WeekNote).delete()
        for n in data["week_notes"]:
            db.add(WeekNote(
                week_num=n["week_num"],
                note=n.get("note", "")
            ))

    if "milestones" in data:
        db.query(Milestone).update({Milestone.done: False})
        done_labels = {m["label"] for m in data["milestones"] if m.get("done")}
        if done_labels:
            db.query(Milestone).filter(Milestone.label.in_(done_labels)).update(
                {Milestone.done: True},
                synchronize_session=False
            )

    db.commit()
    return {"status": "success", "message": "Dados restaurados com sucesso!"}
