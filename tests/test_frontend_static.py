from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_has_all_dynamic_sections():
    html = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    for view in (
        "today", "queue", "courses", "roadmap", "projects", "achievements",
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


def test_course_cards_render_safe_external_source_links():
    javascript = (ROOT / "static" / "app.js").read_text(encoding="utf-8")

    assert "courseSourceAction(course)" in javascript
    assert "isSafeExternalUrl(course.url)" in javascript
    assert "^https?:\\/\\/" in javascript
    assert 'target="_blank"' in javascript
    assert 'rel="noopener noreferrer"' in javascript
    assert "Abrir curso" in javascript
    assert "Link não cadastrado" in javascript
    assert 'aria-disabled="true"' in javascript
    assert 'href=""' not in javascript


def test_achievement_badges_remain_available_in_dynamic_frontend():
    html = (ROOT / "templates" / "index.html").read_text(encoding="utf-8")
    javascript = (ROOT / "static" / "app.js").read_text(encoding="utf-8")

    assert 'data-view="achievements"' in html
    assert "function computeBadges()" in javascript
    assert "function renderAchievements()" in javascript
    assert "function showBadgeCelebration(badge)" in javascript
    assert "course.activities_done" in javascript
    assert "State.stats?.by_phase" in javascript
    assert "SRE Master" in javascript
    assert "Badge conquistado!" in javascript
