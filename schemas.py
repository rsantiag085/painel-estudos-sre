"""
schemas.py — Pydantic schemas para request/response
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


# ── LessonProgress ──────────────────────────────────────────────────────────

class LessonProgressCreate(BaseModel):
    status: str = "pending"   # 'pending' | 'done' | 'skipped'
    note: Optional[str] = ""


class LessonProgressResponse(BaseModel):
    lesson_id: str
    status: str
    note: str
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── WeekNote ─────────────────────────────────────────────────────────────────

class WeekNoteCreate(BaseModel):
    note: str = ""


class WeekNoteResponse(BaseModel):
    week_num: int
    note: str
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Milestone ─────────────────────────────────────────────────────────────────

class MilestoneUpdate(BaseModel):
    done: bool


class MilestoneResponse(BaseModel):
    id: int
    phase_num: int
    label: str
    done: bool
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Stats ─────────────────────────────────────────────────────────────────────

class PhaseStats(BaseModel):
    phase: int
    label: str
    done: int
    total: int
    pct: int


class StatsResponse(BaseModel):
    done: int
    total: int
    skipped: int
    work_days: int
    hours_studied: float
    pct: int
    by_phase: list[PhaseStats]
    # v2.0 — Labs Zabbix extras (opcionais para compatibilidade)
    total_labs_zabbix: Optional[int] = 0
    labs_completed: Optional[int] = 0
    labs_pct: Optional[int] = 0
    days_remaining: Optional[int] = None
    expected_completion: Optional[str] = None
