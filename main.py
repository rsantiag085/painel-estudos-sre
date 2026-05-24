"""
main.py -- SRE Tracker -- FastAPI + Uvicorn + SQLite
Execucao: python main.py
"""
import sys
import io
import threading
import webbrowser
from contextlib import asynccontextmanager
from pathlib import Path

# Forcar UTF-8 no stdout para Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse

# Ajuste do path para imports relativos funcionarem
BASE_DIR = Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))

from database import create_tables, SessionLocal
from routers import progress, stats, notes, milestones


# -- Lifespan (substitui on_event deprecado) ----------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    _seed_milestones()
    yield


# -- App ----------------------------------------------------------------------
app = FastAPI(
    title="SRE Tracker",
    description="Painel de Estudos SRE - Robson Santiago",
    version="1.0.0",
    lifespan=lifespan,
)

# -- Static files & Templates -------------------------------------------------
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

# -- Routers ------------------------------------------------------------------
app.include_router(progress.router)
app.include_router(stats.router)
app.include_router(notes.router)
app.include_router(milestones.router)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    import json
    from data.curriculum import PHASES, WEEKS
    html_path = BASE_DIR / "templates" / "index.html"
    html = html_path.read_text(encoding="utf-8")
    # Substituir os placeholders Jinja2 manualmente
    html = html.replace("{{ phases_json | safe }}", json.dumps(PHASES))
    html = html.replace("{{ weeks_json  | safe }}", json.dumps(WEEKS))
    return HTMLResponse(content=html)


# -- Seed ---------------------------------------------------------------------
def _seed_milestones():
    """Insere milestones iniciais se a tabela estiver vazia."""
    from models import Milestone
    from data.curriculum import MILESTONES

    db = SessionLocal()
    try:
        count = db.query(Milestone).count()
        if count == 0:
            for phase_num, labels in MILESTONES.items():
                for label in labels:
                    db.add(Milestone(phase_num=phase_num, label=label, done=False))
            db.commit()
    finally:
        db.close()


# -- Main ---------------------------------------------------------------------
def _open_browser():
    import time
    time.sleep(1.5)
    webbrowser.open("http://localhost:8000")


if __name__ == "__main__":
    print()
    print("+---------------------------------------------+")
    print("|  SRE Tracker -- Robson Santiago             |")
    print("|  http://localhost:8000                      |")
    print("|  Ctrl+C para parar                          |")
    print("+---------------------------------------------+")
    print()

    threading.Thread(target=_open_browser, daemon=True).start()

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="warning",
    )
