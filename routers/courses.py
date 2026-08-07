from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Activity, ActivityProgress, Course
from routers.serializers import course_view
from schemas import CourseView

router = APIRouter(prefix="/api/courses", tags=["courses"])


def _statuses_for_course(db: Session, course_id: str) -> list[str]:
    return db.scalars(
        select(ActivityProgress.status)
        .join(Activity, Activity.id == ActivityProgress.activity_id)
        .where(Activity.course_id == course_id)
    ).all()


@router.get("", response_model=list[CourseView])
async def list_courses(
    phase: int | None = Query(default=None, ge=1, le=5),
    status: str | None = None,
    db: Session = Depends(get_db),
):
    statement = select(Course).order_by(Course.phase, Course.id)
    if phase is not None:
        statement = statement.where(Course.phase == phase)
    if status is not None:
        statement = statement.where(Course.status == status)
    courses = db.scalars(statement).all()
    return [course_view(course, _statuses_for_course(db, course.id)) for course in courses]


@router.get("/{course_id}", response_model=CourseView)
async def get_course(course_id: str, db: Session = Depends(get_db)):
    course = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Curso não encontrado")
    return course_view(course, _statuses_for_course(db, course.id))
