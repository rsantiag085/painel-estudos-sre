# SRE Tracker — Robson Santiago

Sistema de acompanhamento de estudos SRE com 31 semanas, 5 fases e ~122,5h de conteúdo.
Cronograma: Maio–Dezembro 2026 | NOC SR → SRE.

## O que é

Aplicação local com backend Python/FastAPI + banco SQLite + frontend HTML/JS.
Abre no browser automaticamente. Todos os dados ficam salvos localmente.

## Como instalar

```bash
cd sre-tracker
pip install -r requirements.txt
```

## Como rodar

```bash
python main.py
```

O sistema irá:
1. Criar o banco `sre_tracker.db` automaticamente
2. Popular os milestones iniciais
3. Iniciar o servidor em `http://localhost:8000`
4. Abrir o browser automaticamente

## Estrutura

```
sre-tracker/
├── main.py              # Entry point
├── database.py          # SQLAlchemy + SQLite
├── models.py            # ORM: LessonProgress, WeekNote, Milestone
├── schemas.py           # Pydantic schemas
├── requirements.txt
├── routers/
│   ├── progress.py      # CRUD progresso por lição
│   ├── stats.py         # Estatísticas + export
│   ├── notes.py         # Notas por semana
│   └── milestones.py    # Checkboxes por fase
├── data/
│   └── curriculum.py    # 31 semanas + 5 fases + milestones
├── static/
│   ├── app.js           # Frontend logic
│   └── style.css        # Dark terminal theme
└── templates/
    └── index.html       # SPA
```

## API REST

```
GET  /api/progress              # Todo o progresso salvo
POST /api/progress/{lesson_id}  # Salva status + nota de uma lição
GET  /api/stats                 # Estatísticas globais e por fase
GET  /api/week/{n}/note         # Nota de uma semana
POST /api/week/{n}/note         # Salva nota de uma semana
GET  /api/milestones            # Lista milestones
POST /api/milestones/{id}       # Toggle done/pending
GET  /api/export                # Backup JSON completo
```

## Backup

Para fazer backup dos seus dados:

```bash
# Via API (JSON completo):
curl http://localhost:8000/api/export > backup.json

# Ou copie diretamente o arquivo SQLite:
cp sre_tracker.db sre_tracker_backup.db
```

## Layout (ASCII)

```
┌──────────────────┬─────────────────────────────────────────┐
│  SRE Tracker     │  ⬡ Dashboard                            │
│  Robson Santiago │  ─────────────────────────────────────  │
│  NOC SR → SRE   │                                         │
│  ────────────── │  [Concluídas] [Total] [Puladas] [Horas]  │
│  ⬡ Dashboard ←  │  ████████░░░░░░░░ 42%                    │
│  📅 Cronograma   │                                         │
│  ✓ Milestones    │  Progresso por Fase                     │
│  📊 Estatísticas │  [F1 ██░ 60%] [F2 █░ 30%] [F3 ░ 0%]   │
│  📤 Exportar     │                                         │
│  ────────────── │  Semana Atual                            │
│  Semana: 5      │  SEG    TER    QUA    QUI    SEX        │
│  42%            │  [✓Git] [✓Py]  [○Py]  [○Py]  [○Py]     │
│  ████░░░░       │                                         │
└──────────────────┴─────────────────────────────────────────┘
```

## Fases do Cronograma

| Fase | Semanas | Tema |
|------|---------|------|
| 1 | 1–4 | Linux · Networking · SRE Mindset |
| 2 | 5–8 | Git · Python · Databases |
| 3 | 9–16 | AWS · Ansible · Terraform · AWX |
| 4 | 17–27 | CI/CD · K8s · Monitoring · Incident Mgmt |
| 5 | 28–31 | Capstone · Carreira · CKA Prep |
