"""
models.py — ORM models: LessonProgress, WeekNote, Milestone, DeferredLesson
"""
from datetime import UTC, datetime
from sqlalchemy import (
    JSON,
    Boolean,
    CheckConstraint,
    Column,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from database import Base


def utcnow():
    """Instante UTC para os modelos novos; legado permanece inalterado."""
    return datetime.now(UTC)


# -- Catálogo dinâmico -------------------------------------------------------


class Course(Base):
    """Snapshot persistido de um curso definido em data/curriculum.py."""

    __tablename__ = "courses"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    provider = Column(String, nullable=False, default="")
    url = Column(String, nullable=False, default="")
    video_hours = Column(Float, nullable=False, default=0.0)
    priority = Column(String, nullable=False)
    execution = Column(String, nullable=False)
    phase = Column(Integer, nullable=False, index=True)
    status = Column(String, nullable=False)
    prerequisites = Column(JSON, nullable=False, default=list)
    notes = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    activities = relationship("Activity", back_populates="course")

    __table_args__ = (
        CheckConstraint("video_hours >= 0", name="ck_courses_video_hours_nonnegative"),
        CheckConstraint("phase BETWEEN 1 AND 5", name="ck_courses_phase"),
    )


class Activity(Base):
    """Snapshot de uma atividade com ID permanente e sem data."""

    __tablename__ = "activities"

    id = Column(String, primary_key=True)
    course_id = Column(String, ForeignKey("courses.id"), nullable=False, index=True)
    sequence = Column(Integer, nullable=False, unique=True, index=True)
    name = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=30)
    activity_type = Column(String, nullable=False)
    preferred_day_type = Column(String, nullable=False, default="ANY")
    preferred_slot = Column(String, nullable=False, default="ANY")
    prerequisites = Column(JSON, nullable=False, default=list)
    tags = Column(JSON, nullable=False, default=list)
    required = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    course = relationship("Course", back_populates="activities")
    progress = relationship(
        "ActivityProgress", back_populates="activity", uselist=False
    )
    history = relationship("ActivityHistory", back_populates="activity")

    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0 AND duration_minutes % 30 = 0",
            name="ck_activities_duration_blocks",
        ),
    )


class StudySlot(Base):
    """Slot materializado da escala; ainda sem lógica de reagendamento."""

    __tablename__ = "study_slots"

    id = Column(String, primary_key=True)  # ex.: 2026-08-05-F1
    study_date = Column(Date, nullable=False, index=True)
    day_type = Column(String, nullable=False)
    slot_code = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False, default=30)
    slot_type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="available", index=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    progress = relationship(
        "ActivityProgress", back_populates="current_slot", uselist=False
    )
    history = relationship("ActivityHistory", back_populates="study_slot")

    __table_args__ = (
        UniqueConstraint("study_date", "slot_code", name="uq_study_slots_date_code"),
        CheckConstraint("duration_minutes = 30", name="ck_study_slots_duration"),
    )


class ActivityProgress(Base):
    """Estado mutável atual de uma atividade do catálogo."""

    __tablename__ = "activity_progress"

    activity_id = Column(
        String, ForeignKey("activities.id"), primary_key=True
    )
    status = Column(String, nullable=False, default="pending", index=True)
    note = Column(Text, nullable=False, default="")
    current_slot_id = Column(
        String, ForeignKey("study_slots.id"), nullable=True, unique=True
    )
    defer_count = Column(Integer, nullable=False, default=0)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=utcnow)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)

    activity = relationship("Activity", back_populates="progress")
    current_slot = relationship("StudySlot", back_populates="progress")

    __table_args__ = (
        CheckConstraint("defer_count >= 0", name="ck_activity_progress_defer_count"),
    )


class ActivityHistory(Base):
    """Log append-only das mudanças de atividade e de slot."""

    __tablename__ = "activity_history"

    id = Column(Integer, primary_key=True, index=True)
    activity_id = Column(
        String, ForeignKey("activities.id"), nullable=False, index=True
    )
    study_slot_id = Column(
        String, ForeignKey("study_slots.id"), nullable=True, index=True
    )
    event_type = Column(String, nullable=False, index=True)
    from_status = Column(String, nullable=True)
    to_status = Column(String, nullable=True)
    note = Column(Text, nullable=False, default="")
    created_at = Column(DateTime, nullable=False, default=utcnow, index=True)

    activity = relationship("Activity", back_populates="history")
    study_slot = relationship("StudySlot", back_populates="history")


class AppSetting(Base):
    """Configuração versionável simples da aplicação."""

    __tablename__ = "app_settings"

    key = Column(String, primary_key=True)
    value = Column(Text, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=utcnow, onupdate=utcnow)


class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(String, unique=True, nullable=False, index=True)
    status = Column(String, default="pending")   # 'pending' | 'done' | 'skipped'
    note = Column(Text, default="")
    # v2.0 — novos campos
    week_num = Column(Integer, nullable=True)    # Semana (1–36)
    lab_type = Column(String, nullable=True)     # 'aula' | 'lab' | 'leitura' | 'projeto' | 'revisao'
    course_url = Column(String, nullable=True)   # URL do curso
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class WeekNote(Base):
    __tablename__ = "week_notes"

    id = Column(Integer, primary_key=True, index=True)
    week_num = Column(Integer, unique=True, nullable=False, index=True)
    note = Column(Text, default="")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, index=True)
    phase_num = Column(Integer, nullable=False)
    label = Column(Text, nullable=False)
    done = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class DeferredLesson(Base):
    """Lição pulada que foi realocada para o próximo dia de FOLGA."""
    __tablename__ = "deferred_lessons"

    id = Column(Integer, primary_key=True, index=True)
    original_lesson_id = Column(String, nullable=False)   # ex: "2026-06-08-0"
    lesson_name = Column(String, nullable=False)
    lesson_hours = Column(Float, nullable=False)
    lesson_type = Column(String, nullable=False)          # aula | lab | leitura | revisao | projeto
    lesson_tag = Column(String, nullable=True)
    lesson_block = Column(String, nullable=False)         # manha | tarde
    target_date = Column(String, nullable=False, index=True)  # próximo dia de FOLGA
    status = Column(String, default="pending")            # pending | done | skipped
    note = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
