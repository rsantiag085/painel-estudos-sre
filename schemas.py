"""
schemas.py — Pydantic schemas para request/response
"""
from datetime import date, datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


ActivityStatus = Literal[
    "pending",
    "in_progress",
    "done",
    "deferred",
    "blocked",
    "skipped",
    "cancelled",
]
DayType = Literal["FOLGA", "TRABALHO", "COMERCIAL"]
SlotStatus = Literal["available", "scheduled", "completed", "missed", "cancelled"]


class ORMResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


# ── Catálogo dinâmico ───────────────────────────────────────────────────────


class CourseBase(BaseModel):
    id: str
    name: str
    provider: str = ""
    url: str = ""
    video_hours: float = Field(default=0.0, ge=0)
    priority: Literal["very_high", "high", "medium", "low"]
    execution: Literal["full", "selective", "optional"]
    phase: int = Field(ge=1, le=5)
    status: Literal["available", "in_progress", "planned", "future"]
    prerequisites: list[str] = Field(default_factory=list)
    notes: str = ""


class CourseCreate(CourseBase):
    pass


class CourseResponse(CourseBase, ORMResponse):
    created_at: datetime
    updated_at: datetime


class ActivityBase(BaseModel):
    id: str
    course_id: str
    sequence: int = Field(gt=0)
    name: str
    duration_minutes: int = Field(default=30, gt=0, multiple_of=30)
    activity_type: Literal[
        "lesson", "lab", "project", "review", "reading", "quiz", "exam"
    ]
    preferred_day_type: Literal["FOLGA", "TRABALHO", "ANY"] = "ANY"
    preferred_slot: Literal[
        "THEORY", "PRACTICE", "REVIEW", "AWS", "READING", "ANY"
    ] = "ANY"
    prerequisites: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    required: bool = True


class ActivityCreate(ActivityBase):
    pass


class ActivityResponse(ActivityBase, ORMResponse):
    created_at: datetime
    updated_at: datetime


class StudySlotBase(BaseModel):
    id: str
    study_date: date
    day_type: DayType
    slot_code: str
    start_time: str
    duration_minutes: int = Field(default=30, gt=0)
    slot_type: str
    status: SlotStatus = "available"


class StudySlotCreate(StudySlotBase):
    pass


class StudySlotResponse(StudySlotBase, ORMResponse):
    created_at: datetime
    updated_at: datetime


class ActivityProgressBase(BaseModel):
    activity_id: str
    status: ActivityStatus = "pending"
    note: str = ""
    current_slot_id: Optional[str] = None
    defer_count: int = Field(default=0, ge=0)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class ActivityProgressCreate(ActivityProgressBase):
    pass


class ActivityProgressResponse(ActivityProgressBase, ORMResponse):
    created_at: datetime
    updated_at: datetime


class ActivityHistoryCreate(BaseModel):
    activity_id: str
    study_slot_id: Optional[str] = None
    event_type: str
    from_status: Optional[ActivityStatus] = None
    to_status: Optional[ActivityStatus] = None
    note: str = ""


class ActivityHistoryResponse(ActivityHistoryCreate, ORMResponse):
    id: int
    created_at: datetime


class AppSettingBase(BaseModel):
    key: str
    value: str


class AppSettingCreate(AppSettingBase):
    pass


class AppSettingResponse(AppSettingBase, ORMResponse):
    updated_at: datetime


class UserSettingsRequest(BaseModel):
    display_name: str = Field(min_length=1, max_length=80)
    start_date: date
    work_schedule: Literal["12x36", "commercial"] = "12x36"
    anchor_date: date
    anchor_day_type: Literal["FOLGA", "TRABALHO"]
    study_days: list[int] = Field(default_factory=lambda: [0, 1, 2, 3, 4])
    daily_study_minutes: int = Field(default=60, ge=30, le=480, multiple_of=30)

    @field_validator("study_days")
    @classmethod
    def validate_study_days(cls, value: list[int]) -> list[int]:
        days = sorted(set(value))
        if any(day < 0 or day > 6 for day in days):
            raise ValueError("study_days deve conter valores entre 0 e 6")
        return days

    @model_validator(mode="after")
    def validate_commercial_schedule(self):
        if self.work_schedule == "commercial" and not self.study_days:
            raise ValueError("Selecione pelo menos um dia de estudo")
        return self


class UserSettingsResponse(UserSettingsRequest):
    configured: bool


# ── API dinâmica ─────────────────────────────────────────────────────────────


class ActivityView(ActivityBase):
    status: ActivityStatus
    note: str = ""
    current_slot_id: Optional[str] = None
    defer_count: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class CourseView(CourseBase):
    activities_total: int
    activities_done: int
    progress_pct: int


class ScheduledActivity(BaseModel):
    id: str
    course_id: str
    name: str
    sequence: int
    activity_type: str
    status: ActivityStatus


class ScheduleSlotView(StudySlotBase):
    activity: Optional[ScheduledActivity] = None


class ScheduleDayResponse(BaseModel):
    date: date
    day_type: DayType
    slots: list[ScheduleSlotView]


class ScheduleRangeResponse(BaseModel):
    start_date: date
    end_date: date
    days: list[ScheduleDayResponse]


class ScheduleGenerateRequest(BaseModel):
    start_date: date
    end_date: Optional[date] = None
    allocate: bool = False


class ScheduleGenerateResponse(BaseModel):
    start_date: date
    end_date: date
    days_processed: int
    slots_created: int
    slots_existing: int
    slots_total: int
    activities_allocated: int


class AllocationRequest(BaseModel):
    activity_id: Optional[str] = None
    note: str = ""


class ActivityCommandRequest(BaseModel):
    note: str = ""


class ProgressGroup(BaseModel):
    id: str
    label: str
    total: int
    done: int
    in_progress: int
    deferred: int
    blocked: int
    skipped: int
    cancelled: int
    pending: int
    pct: int
    minutes_completed: int


class ProgressSummaryResponse(BaseModel):
    total: int
    done: int
    in_progress: int
    deferred: int
    blocked: int
    skipped: int
    cancelled: int
    pending: int
    pct: int
    minutes_completed: int
    hours_completed: float
    slots_completed: int
    slots_missed: int
    execution_rate_pct: int


class DynamicStatsResponse(ProgressSummaryResponse):
    by_phase: list[ProgressGroup]
    by_course: list[ProgressGroup]


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


# ── DeferredLesson ────────────────────────────────────────────────────────────

class DeferredLessonUpdate(BaseModel):
    status: str          # 'done' | 'skipped'
    note: Optional[str] = ""


class DeferredLessonResponse(BaseModel):
    id: int
    original_lesson_id: str
    lesson_name: str
    lesson_hours: float
    lesson_type: str
    lesson_tag: Optional[str]
    lesson_block: str
    target_date: str
    status: str
    note: str
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Stats ─────────────────────────────────────────────────────────────────────

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
