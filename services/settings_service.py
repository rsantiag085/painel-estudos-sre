"""Configuração da instalação para uso por diferentes estudantes."""

import os
from datetime import date

from sqlalchemy.orm import Session

from models import AppSetting


KEYS = {
    "configured": "profile.configured",
    "display_name": "profile.display_name",
    "start_date": "schedule.start_date",
    "anchor_date": "schedule.anchor_date",
    "anchor_day_type": "schedule.anchor_day_type",
}


def _value(session: Session, key: str, default: str) -> str:
    row = session.get(AppSetting, key)
    return row.value if row is not None else default


def get_settings(session: Session) -> dict:
    anchor_default = os.getenv("SCALE_ANCHOR_DATE", "2030-01-01")
    anchor_date = date.fromisoformat(_value(session, KEYS["anchor_date"], anchor_default))
    return {
        "configured": _value(session, KEYS["configured"], "false") == "true",
        "display_name": _value(session, KEYS["display_name"], "Estudante"),
        "start_date": date.fromisoformat(
            _value(session, KEYS["start_date"], anchor_date.isoformat())
        ),
        "anchor_date": anchor_date,
        "anchor_day_type": _value(session, KEYS["anchor_day_type"], "FOLGA"),
    }


def save_settings(session: Session, payload: dict) -> dict:
    values = {
        KEYS["configured"]: "true",
        KEYS["display_name"]: payload["display_name"].strip(),
        KEYS["start_date"]: payload["start_date"].isoformat(),
        KEYS["anchor_date"]: payload["anchor_date"].isoformat(),
        KEYS["anchor_day_type"]: payload["anchor_day_type"],
    }
    for key, value in values.items():
        row = session.get(AppSetting, key)
        if row is None:
            session.add(AppSetting(key=key, value=value))
        else:
            row.value = value
    session.flush()
    return get_settings(session)
