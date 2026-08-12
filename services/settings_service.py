"""Configuração da instalação para uso por diferentes estudantes."""

import json
import os
from datetime import date

from sqlalchemy.orm import Session

from models import AppSetting


KEYS = {
    "configured": "profile.configured",
    "display_name": "profile.display_name",
    "start_date": "schedule.start_date",
    "work_schedule": "schedule.work_schedule",
    "anchor_date": "schedule.anchor_date",
    "anchor_day_type": "schedule.anchor_day_type",
    "study_days": "schedule.study_days",
    "daily_study_minutes": "schedule.daily_study_minutes",
}


def _value(session: Session, key: str, default: str) -> str:
    row = session.get(AppSetting, key)
    return row.value if row is not None else default


def get_settings(session: Session) -> dict:
    anchor_default = os.getenv("SCALE_ANCHOR_DATE", "2030-01-01")
    anchor_date = date.fromisoformat(_value(session, KEYS["anchor_date"], anchor_default))
    raw_study_days = _value(session, KEYS["study_days"], "[0, 1, 2, 3, 4]")
    try:
        study_days = sorted({int(day) for day in json.loads(raw_study_days)})
    except (TypeError, ValueError, json.JSONDecodeError):
        study_days = [0, 1, 2, 3, 4]
    return {
        "configured": _value(session, KEYS["configured"], "false") == "true",
        "display_name": _value(session, KEYS["display_name"], "Estudante"),
        "start_date": date.fromisoformat(
            _value(session, KEYS["start_date"], anchor_date.isoformat())
        ),
        "work_schedule": _value(session, KEYS["work_schedule"], "12x36"),
        "anchor_date": anchor_date,
        "anchor_day_type": _value(session, KEYS["anchor_day_type"], "FOLGA"),
        "study_days": [day for day in study_days if 0 <= day <= 6],
        "daily_study_minutes": int(_value(session, KEYS["daily_study_minutes"], "60")),
    }


def save_settings(session: Session, payload: dict) -> dict:
    values = {
        KEYS["configured"]: "true",
        KEYS["display_name"]: payload["display_name"].strip(),
        KEYS["start_date"]: payload["start_date"].isoformat(),
        KEYS["work_schedule"]: payload["work_schedule"],
        KEYS["anchor_date"]: payload["anchor_date"].isoformat(),
        KEYS["anchor_day_type"]: payload["anchor_day_type"],
        KEYS["study_days"]: json.dumps(payload["study_days"]),
        KEYS["daily_study_minutes"]: str(payload["daily_study_minutes"]),
    }
    for key, value in values.items():
        row = session.get(AppSetting, key)
        if row is None:
            session.add(AppSetting(key=key, value=value))
        else:
            row.value = value
    session.flush()
    return get_settings(session)
