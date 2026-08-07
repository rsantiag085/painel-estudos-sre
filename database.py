"""
database.py — SQLAlchemy setup + SQLite connection
"""
import os
import sqlite3
from pathlib import Path

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

import config  # noqa: F401  # carrega o .env antes de DATABASE_URL

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sre_tracker.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    # Importa todos os modelos para registrá-los no mesmo metadata. create_all
    # é aditivo: não remove nem altera as tabelas legadas existentes.
    from models import (  # noqa: F401
        Activity,
        ActivityHistory,
        ActivityProgress,
        AppSetting,
        Course,
        DeferredLesson,
        LessonProgress,
        Milestone,
        StudySlot,
        WeekNote,
    )

    backup_sqlite_before_dynamic_schema()
    Base.metadata.create_all(bind=engine)


def backup_sqlite_before_dynamic_schema() -> Path | None:
    """Cria um backup consistente uma única vez antes das tabelas novas.

    Bancos não SQLite, bancos em memória, arquivos inexistentes e bancos que já
    possuem a tabela ``courses`` não precisam desse backup de transição.
    """
    if engine.dialect.name != "sqlite" or inspect(engine).has_table("courses"):
        return None

    database_name = engine.url.database
    if not database_name or database_name == ":memory:":
        return None

    source = Path(database_name).resolve()
    if not source.exists() or source.stat().st_size == 0:
        return None

    backup_dir = source.parent / ".backups"
    backup_dir.mkdir(parents=True, exist_ok=True)
    destination = backup_dir / f"{source.stem}-pre-dynamic-models{source.suffix}"
    if destination.exists():
        return destination

    with sqlite3.connect(source) as source_db, sqlite3.connect(destination) as backup_db:
        source_db.backup(backup_db)

    return destination


def seed_curriculum_data():
    """Executa o seed do catálogo em uma transação única."""
    from services.curriculum_seed import seed_curriculum

    with SessionLocal.begin() as db:
        return seed_curriculum(db)
