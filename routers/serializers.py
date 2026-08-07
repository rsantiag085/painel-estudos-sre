"""Serialização compartilhada das entidades da API dinâmica."""

from models import Activity, ActivityProgress, Course, StudySlot


def activity_view(activity: Activity, progress: ActivityProgress) -> dict:
    return {
        "id": activity.id,
        "course_id": activity.course_id,
        "sequence": activity.sequence,
        "name": activity.name,
        "duration_minutes": activity.duration_minutes,
        "activity_type": activity.activity_type,
        "preferred_day_type": activity.preferred_day_type,
        "preferred_slot": activity.preferred_slot,
        "prerequisites": activity.prerequisites or [],
        "tags": activity.tags or [],
        "required": activity.required,
        "status": progress.status,
        "note": progress.note or "",
        "current_slot_id": progress.current_slot_id,
        "defer_count": progress.defer_count,
        "started_at": progress.started_at,
        "completed_at": progress.completed_at,
    }


def course_view(course: Course, statuses: list[str]) -> dict:
    total = len(statuses)
    done = statuses.count("done")
    return {
        "id": course.id,
        "name": course.name,
        "provider": course.provider,
        "url": course.url,
        "video_hours": course.video_hours,
        "priority": course.priority,
        "execution": course.execution,
        "phase": course.phase,
        "status": course.status,
        "prerequisites": course.prerequisites or [],
        "notes": course.notes or "",
        "activities_total": total,
        "activities_done": done,
        "progress_pct": round(done / total * 100) if total else 0,
    }


def slot_view(slot: StudySlot) -> dict:
    activity_payload = None
    if slot.progress is not None:
        activity = slot.progress.activity
        activity_payload = {
            "id": activity.id,
            "course_id": activity.course_id,
            "name": activity.name,
            "sequence": activity.sequence,
            "activity_type": activity.activity_type,
            "status": slot.progress.status,
        }
    return {
        "id": slot.id,
        "study_date": slot.study_date,
        "day_type": slot.day_type,
        "slot_code": slot.slot_code,
        "start_time": slot.start_time,
        "duration_minutes": slot.duration_minutes,
        "slot_type": slot.slot_type,
        "status": slot.status,
        "activity": activity_payload,
    }
