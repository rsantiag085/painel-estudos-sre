from data.curriculum import ACTIVITIES, COURSES
from models import Activity, ActivityProgress, AppSetting, Course
from services.curriculum_seed import seed_curriculum


def test_seed_populates_catalog_progress_and_settings(session):
    result = seed_curriculum(session)

    assert result.courses_created == len(COURSES)
    assert result.activities_created == len(ACTIVITIES)
    assert result.progress_created == len(ACTIVITIES)
    assert session.query(Course).count() == len(COURSES)
    assert session.query(Activity).count() == len(ACTIVITIES)
    assert session.query(ActivityProgress).count() == len(ACTIVITIES)
    assert session.get(AppSetting, "curriculum.course_count").value == str(len(COURSES))
    assert session.get(AppSetting, "curriculum.activity_count").value == str(len(ACTIVITIES))


def test_seed_is_idempotent(session):
    seed_curriculum(session)
    session.flush()

    result = seed_curriculum(session)

    assert result.courses_created == 0
    assert result.courses_updated == 0
    assert result.activities_created == 0
    assert result.activities_updated == 0
    assert result.progress_created == 0
    assert session.query(Course).count() == len(COURSES)
    assert session.query(Activity).count() == len(ACTIVITIES)


def test_seed_updates_catalog_but_preserves_user_progress(session):
    seed_curriculum(session)
    progress = session.get(ActivityProgress, "linux-admin-001")
    progress.status = "done"
    progress.note = "estado do usuário"
    course = session.get(Course, "linux-admin")
    course.name = "nome desatualizado"
    session.flush()

    result = seed_curriculum(session)

    assert result.courses_updated == 1
    assert session.get(Course, "linux-admin").name == COURSES[0]["name"]
    preserved = session.get(ActivityProgress, "linux-admin-001")
    assert preserved.status == "done"
    assert preserved.note == "estado do usuário"
