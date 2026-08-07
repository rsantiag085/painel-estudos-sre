from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_has_all_dynamic_sections():
    html = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    for view in (
        "today", "queue", "courses", "roadmap", "projects",
        "aws", "google", "history", "stats",
    ):
        assert f'data-view="{view}"' in html


def test_frontend_does_not_use_weeks_or_rigid_schedule_copy():
    content = "\n".join(
        [
            (ROOT / "templates" / "index.html").read_text(encoding="utf-8"),
            (ROOT / "static" / "app.js").read_text(encoding="utf-8"),
        ]
    ).lower()
    forbidden = (
        "weeks",
        "36 semanas",
        "janeiro de 2027",
        "dias restantes",
        "30 labs",
        "labs zabbix",
        "cronograma rígido",
    )
    for phrase in forbidden:
        assert phrase not in content


def test_frontend_uses_dynamic_api_and_required_actions():
    javascript = (ROOT / "static" / "app.js").read_text(encoding="utf-8")
    for path in (
        "/api/schedule/generate",
        "/api/schedule/today",
        "/api/activities/next",
        "/api/courses",
        "/api/stats",
        "/api/history",
    ):
        assert path in javascript
    for command in ("start", "complete", "defer", "block", "skip", "note"):
        assert command in javascript


def test_today_view_uses_canonical_schedule_route_without_duplicate_prefix():
    javascript = (ROOT / "static" / "app.js").read_text(encoding="utf-8")

    assert "api('/api/schedule/today')" in javascript
    assert "/api/api/" not in javascript
