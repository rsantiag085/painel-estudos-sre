def generate(client, start="2030-01-01", end="2030-01-03", allocate=False):
    return client.post(
        "/api/schedule/generate",
        json={"start_date": start, "end_date": end, "allocate": allocate},
    )


def test_courses_and_activities_catalog_api(api_client):
    courses = api_client.get("/api/courses")
    assert courses.status_code == 200
    assert len(courses.json()) == 23
    assert courses.json()[0]["activities_total"] > 0

    phase_one = api_client.get("/api/courses", params={"phase": 1})
    assert phase_one.status_code == 200
    assert all(course["phase"] == 1 for course in phase_one.json())

    course = api_client.get("/api/courses/linux-admin")
    assert course.status_code == 200
    assert course.json()["url"] == "https://www.udemy.com/course/adm-so-gnulinux/"
    assert course.json()["id"] == "linux-admin"

    catalog_course = api_client.get("/api/courses/networks-devops")
    assert catalog_course.status_code == 200
    assert catalog_course.json()["url"].startswith("https://www.udemy.com/course/")

    git_course = api_client.get("/api/courses/git-github")
    assert git_course.status_code == 200
    assert git_course.json()["url"] == (
        "https://www.youtube.com/watch?v=84FhNXNWoig"
        "&list=PLvlkVRRKOYFQyKmdrassLNxkzSMM6tcSL"
    )

    course_without_url = api_client.get("/api/courses/aws-restart")
    assert course_without_url.status_code == 200
    assert course_without_url.json()["url"] == ""

    activities = api_client.get(
        "/api/activities", params={"course_id": "linux-admin"}
    )
    assert activities.status_code == 200
    assert len(activities.json()) == 18
    assert activities.json()[0]["id"] == "linux-admin-001"
    assert activities.json()[0]["status"] == "pending"

    detail = api_client.get("/api/activities/linux-admin-001")
    assert detail.status_code == 200
    assert detail.json()["sequence"] == 1
    assert api_client.get("/api/activities/inexistente").status_code == 404


def test_next_activity_api_uses_sequence_and_slot_compatibility(api_client):
    assert api_client.get("/api/activities/next").json()["id"] == "linux-admin-001"
    generate(api_client)

    response = api_client.get(
        "/api/activities/next", params={"slot_id": "2030-01-01-F1"}
    )
    assert response.status_code == 200
    assert response.json()["id"] == "linux-admin-002"


def test_schedule_generation_is_idempotent_and_queryable(api_client):
    first = generate(api_client, end="2030-01-02")
    second = generate(api_client, end="2030-01-02")

    assert first.status_code == 200
    assert first.json()["slots_created"] == 6
    assert second.json()["slots_created"] == 0
    assert second.json()["slots_existing"] == 6

    today = api_client.get("/api/schedule/today", params={"date": "2030-01-01"})
    assert today.status_code == 200
    assert today.json()["day_type"] == "FOLGA"
    assert [slot["slot_code"] for slot in today.json()["slots"]] == [
        "F1", "F2", "F3", "F4"
    ]

    schedule_range = api_client.get(
        "/api/schedule/range",
        params={"start_date": "2030-01-01", "end_date": "2030-01-02"},
    )
    assert schedule_range.status_code == 200
    assert len(schedule_range.json()["days"]) == 2
    assert len(schedule_range.json()["days"][1]["slots"]) == 2


def test_schedule_today_canonical_route_without_date_parameter(api_client):
    response = api_client.get("/api/schedule/today")

    assert response.status_code == 200
    assert {"date", "day_type", "slots"}.issubset(response.json())
    assert isinstance(response.json()["slots"], list)
    assert api_client.get("/api/api/schedule/today").status_code == 404


def test_allocate_start_complete_and_history_api(api_client):
    generate(api_client)
    allocated = api_client.post(
        "/api/schedule/slots/2030-01-01-F3/allocate",
        json={"activity_id": "linux-admin-001", "note": "planejada"},
    )
    assert allocated.status_code == 200
    assert allocated.json()["current_slot_id"] == "2030-01-01-F3"

    started = api_client.post(
        "/api/activities/linux-admin-001/start", json={"note": "começando"}
    )
    assert started.status_code == 200
    assert started.json()["status"] == "in_progress"

    completed = api_client.post(
        "/api/activities/linux-admin-001/complete", json={"note": "feito"}
    )
    assert completed.status_code == 200
    assert completed.json()["status"] == "done"
    assert completed.json()["current_slot_id"] == "2030-01-01-F3"

    history = api_client.get("/api/activities/linux-admin-001/history")
    assert history.status_code == 200
    assert [event["event_type"] for event in history.json()] == [
        "scheduled", "started", "completed"
    ]
    assert api_client.post(
        "/api/activities/linux-admin-001/defer", json={"note": "não pode"}
    ).status_code == 409


def test_defer_api_records_history_and_reallocates(api_client):
    generate(api_client)
    api_client.post(
        "/api/schedule/slots/2030-01-01-F3/allocate",
        json={"activity_id": "linux-admin-001"},
    )

    deferred = api_client.post(
        "/api/activities/linux-admin-001/defer", json={"note": "imprevisto"}
    )

    assert deferred.status_code == 200
    assert deferred.json()["status"] == "deferred"
    assert deferred.json()["current_slot_id"] == "2030-01-01-F4"
    events = api_client.get(
        "/api/history", params={"activity_id": "linux-admin-001"}
    )
    assert events.status_code == 200
    assert any(event["event_type"] == "deferred" for event in events.json())


def test_block_skip_and_cancel_api(api_client):
    cases = [
        ("linux-admin-001", "block", "blocked"),
        ("linux-admin-002", "skip", "skipped"),
        ("linux-admin-003", "cancel", "cancelled"),
    ]
    for activity_id, command, expected in cases:
        response = api_client.post(
            f"/api/activities/{activity_id}/{command}", json={"note": expected}
        )
        assert response.status_code == 200
        assert response.json()["status"] == expected

    filtered = api_client.get("/api/activities", params={"status": "blocked"})
    assert [activity["id"] for activity in filtered.json()] == ["linux-admin-001"]


def test_add_note_without_changing_status(api_client):
    response = api_client.post(
        "/api/activities/linux-admin-001/note",
        json={"note": "revisar permissões"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "pending"
    assert response.json()["note"] == "revisar permissões"
    history = api_client.get("/api/activities/linux-admin-001/history").json()
    assert history[-1]["event_type"] == "note_updated"


def test_stats_and_progress_grouping_api(api_client):
    generate(api_client)
    api_client.post(
        "/api/schedule/slots/2030-01-01-F3/allocate",
        json={"activity_id": "linux-admin-001"},
    )
    api_client.post("/api/activities/linux-admin-001/complete", json={})

    summary = api_client.get("/api/progress/summary")
    assert summary.status_code == 200
    assert summary.json()["total"] == 300
    assert summary.json()["done"] == 1
    assert summary.json()["minutes_completed"] == 30
    assert summary.json()["execution_rate_pct"] == 100

    phases = api_client.get("/api/progress/phases")
    courses = api_client.get("/api/progress/courses")
    stats = api_client.get("/api/stats")
    assert phases.status_code == courses.status_code == stats.status_code == 200
    assert len(phases.json()) == 5
    linux = next(item for item in courses.json() if item["id"] == "linux-admin")
    assert linux["done"] == 1
    assert stats.json()["by_phase"][0]["done"] == 1
    assert stats.json()["by_course"]


def test_read_only_legacy_progress_and_extended_export(api_client):
    progress = api_client.get("/api/progress")
    assert progress.status_code == 200
    assert len(progress.json()) == 300
    assert progress.json()[0]["lesson_id"]

    exported = api_client.get("/api/export")
    assert exported.status_code == 200
    assert exported.json()["schema_version"] == "3.0"
    assert "progress" in exported.json()  # formato legado
    assert len(exported.json()["dynamic"]["activities"]) == 300
    assert len(exported.json()["dynamic"]["activity_progress"]) == 300

    assert api_client.get("/api/progress/week/1").status_code == 404
    assert api_client.get("/api/deferred").status_code == 404
