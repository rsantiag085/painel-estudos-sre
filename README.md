# SRE Tracker — Robson Santiago

Sistema de acompanhamento de estudos SRE com **36 semanas**, **5 fases** e ~213h de conteúdo.

> **Cronograma:** Maio 25 – Dezembro 31, 2026 &nbsp;|&nbsp; **NOC Sênior → SRE** &nbsp;|&nbsp; **30 Labs Zabbix**

---

## 🎯 Objetivo

Transformar de **NOC Sênior** em **SRE Engineer** seguindo o roadmap SRE Medium completo (15/15 hard skills), aproveitando a expertise atual em Zabbix como diferencial de carreira.

---

## 📊 Estrutura do Programa

| Item | Quantidade | Horas |
|------|-----------|-------|
| Semanas | 36 (Mai–Dez 2026) | — |
| Fases | 5 | — |
| Cursos pagos | 12 | ~163h |
| Recursos gratuitos | 13 | ~50h |
| Labs Zabbix | 30 (1/semana) | ~30h |
| Escala 12x36 | 4h/folga + 0.5h/plantão | ~560h disponíveis |

---

## 📅 Fases do Cronograma

| Fase | Semanas | Tema | Conteúdo |
|------|---------|------|----------|
| 1 | S05–S08 | Foundation | Linux, Networking, Bash, SRE Mindset |
| 2 | S09–S12 | Core Skills | Python, Git, SQL, Docker |
| 3 | S13–S22 | Cloud & IaC | AWS SAA-C03, Terraform, Ansible, AWX |
| 4 | S23–S29 | Advanced SRE | GitHub Actions, Kubernetes, Prometheus, Incident Management |
| 5 | S30–S36 | Capstone & Carreira | Projeto final, portfolio, preparação carreira |

---

## 🧪 Labs Zabbix (30 total)

Labs práticos semanais para consolidar expertise em monitoramento — **diferencial de carreira**:

| Lab | Semana | Tema |
|-----|--------|------|
| #1  | S05 | Zabbix agent install em VM Ubuntu |
| #2  | S06 | Custom network monitoring items |
| #3  | S07 | Bash external check integrado |
| #4  | S08 | Scripts bash no GitHub |
| #5  | S09 | Python consome Zabbix API |
| ... | ... | ... |
| #27 | S31 | Zabbix on K8s (capstone) |
| #28 | S32 | Prometheus + Zabbix integração |
| #29 | S33 | SLO dashboard Zabbix completo |
| #30 | S34 | End-to-end automated incident response |

Veja a lista completa em `COURSES.md` ou no painel em **🧪 Labs Zabbix**.

---

## 🎓 15 Hard Skills (100% cobertas)

| # | Skill | Curso/Recurso |
|---|-------|--------------|
| 1 | Linux Fundamentals | GNU/Linux Admin (9h) |
| 2 | Networking Basics | Redes para DevOps (6-8h) |
| 3 | Bash Scripting | Linux Admin + OverTheWire |
| 4 | Git/Version Control | YouTube Playlist (6-8h) |
| 5 | Python Programming | Python para DevOps (7.5h) |
| 6 | Databases Basics | SQL (4-6h) |
| 7 | Docker Containerization | Play with Docker + Flask (14h) |
| 8 | Cloud (AWS) | AWS SAA-C03 (30.5h) |
| 9 | Ansible | Ansible + AWX (27h) |
| 10 | Monitoring & Observability | Prometheus + Grafana + Zabbix |
| 11 | CI/CD Pipelines | GitHub Actions (7h) |
| 12 | Kubernetes | K8s Completo (19h) |
| 13 | Incident Management | Google SRE Book + prático (gratuito) |
| 14 | IaC (Terraform) | Terraform Essentials (5h) |
| 15 | Soft Skills | Contínuo ao longo do cronograma |

---

## 🚀 Como Rodar

```bash
# Instalar dependências
pip install -r requirements.txt

# Iniciar o servidor
python main.py
```

Abre automaticamente em `http://localhost:8000`

### Endpoints da API

| Endpoint | Descrição |
|----------|-----------|
| `GET /api/stats` | Estatísticas gerais + Labs Zabbix KPIs |
| `GET /api/progress` | Todo o progresso |
| `GET /api/progress/labs` | Somente Labs Zabbix |
| `GET /api/progress/week/{n}` | Progresso de uma semana |
| `GET /api/progress/next?limit=3` | Próximas lições pendentes |
| `GET /api/export` | Exportar backup JSON |
| `POST /api/import` | Restaurar backup JSON |

---

## 📈 Projeção de Carreira (Jan 2027)

**SRE Engineer Junior/Mid-level** com expertise em:

- ✅ Linux + Networking + Bash (avançado)
- ✅ Python + SQL + Git (intermediário)
- ✅ AWS + Terraform + Ansible (intermediário)
- ✅ Kubernetes + CI/CD (intermediário)
- ✅ Monitoring: Prometheus + Grafana + **Zabbix** (avançado — diferencial!)
- ✅ Incident Management (intermediário)

**Portfolio:** 30+ repos Zabbix labs + 1 sistema capstone production-ready

---

## 📁 Estrutura do Projeto

```
painel-estudos-sre/
├── main.py              # FastAPI app + lifespan
├── models.py            # SQLAlchemy ORM (LessonProgress, WeekNote, Milestone)
├── schemas.py           # Pydantic schemas
├── database.py          # SQLite setup
├── data/
│   └── curriculum.py    # Cronograma completo (36 semanas + 30 labs Zabbix)
├── routers/
│   ├── progress.py      # CRUD progresso + /labs + /week + /next
│   ├── stats.py         # Estatísticas + Labs Zabbix KPIs
│   ├── milestones.py    # Milestones por fase
│   └── notes.py         # Notas por semana
├── templates/
│   └── index.html       # App HTML com sidebar e modal
├── static/
│   ├── app.js           # Frontend SPA (Dashboard, Cronograma, Labs Zabbix, Exportar)
│   └── style.css        # Dark theme NOC/Grafana-inspired
└── COURSES.md           # Catálogo completo de cursos
```

---

*v2.0 | Atualizado: Maio 2026 | 36 semanas | 30 Labs Zabbix | 100% roadmap SRE Medium*
