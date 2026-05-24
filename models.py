"""
models.py — ORM models: LessonProgress, WeekNote, Milestone
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from database import Base


class LessonProgress(Base):
    __tablename__ = "lesson_progress"

    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(String, unique=True, nullable=False, index=True)
    status = Column(String, default="pending")   # 'pending' | 'done' | 'skipped'
    note = Column(Text, default="")
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
