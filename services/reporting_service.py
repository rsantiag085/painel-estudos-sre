"""Agregações de progresso independentes de semanas fixas."""

from collections import Counter, defaultdict

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from data.curriculum import PHASES
from models import Activity, ActivityProgress, Course, StudySlot


TRACKED_STATUSES = (
    "done",
    "in_progress",
    "deferred",
    "blocked",
    "skipped",
    "cancelled",
    "pending",
)


def _group_payload(group_id, label, rows):
    counts = Counter(progress.status for activity, progress in rows)
    total = len(rows)
    done = counts["done"]
    minutes = sum(
        activity.duration_minutes
        for activity, progress in rows
        if progress.status == "done"
    )
    return {
        "id": str(group_id),
        "label": label,
        "total": total,
        **{status: counts[status] for status in TRACKED_STATUSES},
        "pct": round(done / total * 100) if total else 0,
        "minutes_completed": minutes,
    }


def progress_by_course(session: Session) -> list[dict]:
    courses = session.scalars(select(Course).order_by(Course.phase, Course.id)).all()
    rows = session.execute(
        select(Activity, ActivityProgress)
        .join(ActivityProgress, ActivityProgress.activity_id == Activity.id)
        .order_by(Activity.sequence)
    ).all()
    grouped = defaultdict(list)
    for activity, progress in rows:
        grouped[activity.course_id].append((activity, progress))
    return [
        _group_payload(course.id, course.name, grouped[course.id])
        for course in courses
    ]


def progress_by_phase(session: Session) -> list[dict]:
    rows = session.execute(
        select(Activity, ActivityProgress, Course.phase)
        .join(ActivityProgress, ActivityProgress.activity_id == Activity.id)
        .join(Course, Course.id == Activity.course_id)
        .order_by(Activity.sequence)
    ).all()
    grouped = defaultdict(list)
    for activity, progress, phase in rows:
        grouped[phase].append((activity, progress))
    return [
        _group_payload(phase, PHASES[phase]["label"], grouped[phase])
        for phase in sorted(PHASES)
    ]


def progress_summary(session: Session) -> dict:
    rows = session.execute(
        select(Activity, ActivityProgress)
        .join(ActivityProgress, ActivityProgress.activity_id == Activity.id)
    ).all()
    counts = Counter(progress.status for _, progress in rows)
    total = len(rows)
    minutes = sum(
        activity.duration_minutes
        for activity, progress in rows
        if progress.status == "done"
    )
    slots_completed = session.scalar(
        select(func.count()).select_from(StudySlot).where(
            StudySlot.status == "completed"
        )
    ) or 0
    slots_missed = session.scalar(
        select(func.count()).select_from(StudySlot).where(
            StudySlot.status == "missed"
        )
    ) or 0
    attempts = slots_completed + slots_missed
    return {
        "total": total,
        **{status: counts[status] for status in TRACKED_STATUSES},
        "pct": round(counts["done"] / total * 100) if total else 0,
        "minutes_completed": minutes,
        "hours_completed": round(minutes / 60, 1),
        "slots_completed": slots_completed,
        "slots_missed": slots_missed,
        "execution_rate_pct": round(slots_completed / attempts * 100)
        if attempts
        else 0,
    }


def full_stats(session: Session) -> dict:
    return {
        **progress_summary(session),
        "by_phase": progress_by_phase(session),
        "by_course": progress_by_course(session),
    }
