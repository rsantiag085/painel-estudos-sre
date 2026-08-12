# GEMINI.md — SRE Tracker

Arquivo de contexto para assistentes de IA (Antigravity/Gemini). Leia este arquivo
antes de qualquer outra coisa neste repositório.

---

## O que é este projeto

**SRE Tracker** é uma aplicação web local para organizar uma trilha de estudos de
SRE/DevOps adaptada à escala de trabalho **12x36** (12 horas trabalhadas, 36 horas
de folga). Não é uma ferramenta genérica de tarefas — ela entende a lógica de
alternância diária da escala e gera slots de estudo automaticamente.

O objetivo de negócio é a **transição de carreira** do usuário de Monitoramento/
Operações para SRE/DevOps/Cloud Engineer.

---

## Stack

| Camada        | Tecnologia                                   |
|---------------|----------------------------------------------|
| Backend       | Python 3.12, FastAPI, Uvicorn                |
| Banco de dados| SQLite (arquivo `sre_tracker.db`)            |
| ORM           | SQLAlchemy 2.x                               |
| Schemas       | Pydantic v2                                  |
| Templates     | Jinja2 (uma única página `index.html`)       |
| Frontend      | HTML + CSS + JavaScript vanilla (sem frameworks) |
| Testes        | Pytest                                       |
| Container     | Docker (Dockerfile disponível)               |

**Comando para rodar:**
```bash
source .venv/bin/activate
python main.py
# Acessa automaticamente http://localhost:8000
```

**Comando para testes:**
```bash
pytest
```

---

## Estrutura de arquivos

```
painel-estudos-sre/
├── main.py                  # Entrypoint: FastAPI app + lifespan + seed + abre browser
├── models.py                # Modelos ORM (SQLAlchemy)
├── schemas.py               # Schemas Pydantic (contratos de API)
├── database.py              # Engine SQLite, SessionLocal, create_tables, seed
├── config.py                # Leitura de variáveis de ambiente
│
├── data/
│   └── curriculum.py        # FONTE OFICIAL de COURSES, ACTIVITIES e MILESTONES
│
├── routers/                 # Cada arquivo = um grupo de endpoints
│   ├── activities.py        # /api/activities — CRUD + transições de estado
│   ├── courses.py           # /api/courses
│   ├── schedule.py          # /api/schedule — agenda do dia, por período, geração de slots
│   ├── progress.py          # /api/progress — por fase e por curso
│   ├── stats.py             # /api/stats — estatísticas consolidadas
│   ├── history.py           # /api/history — log de execução
│   ├── milestones.py        # /api/milestones — marcos por fase
│   ├── settings.py          # /api/settings — configurações por instalação
│   ├── deferred.py          # /api/deferred — atividades adiadas
│   ├── notes.py             # /api/notes
│   └── serializers.py       # Helpers de serialização compartilhados
│
├── services/                # Lógica de negócio (sem acesso direto à HTTP)
│   ├── scale_service.py     # Cálculo FOLGA/TRABALHO pela âncora da escala
│   ├── scheduling_service.py# Alocação, reagendamento e motor de fila
│   ├── curriculum_seed.py   # Seed idempotente de cursos e atividades
│   ├── reporting_service.py # Dados para progresso e estatísticas
│   └── settings_service.py  # Leitura/escrita de AppSetting
│
├── templates/
│   └── index.html           # SPA única; variáveis substituídas pelo FastAPI
│
├── static/
│   ├── app.js               # Toda a lógica do frontend (~30 KB)
│   └── style.css            # Estilos (~66 KB)
│
├── tests/                   # Suíte de testes Pytest
│   ├── conftest.py          # Fixtures compartilhadas (banco em memória)
│   ├── test_api.py          # Testes de integração da API REST
│   ├── test_curriculum_seed.py
│   ├── test_dynamic_models.py
│   ├── test_frontend_static.py
│   ├── test_scale_service.py
│   └── test_scheduling_service.py
│
├── README.md                # Visão geral, princípios, API e estrutura
├── MANUAL_PROJETO_SRE.md    # Contexto de carreira, rotina e regras do domínio
├── COURSES.md               # Catálogo de cursos com ordem pedagógica
├── CHANGELOG.md             # Histórico de alterações (Keep a Changelog)
├── STATE_SAVE.md            # Ponto de retomada da última sessão de desenvolvimento
└── GEMINI.md                # Este arquivo
```

---

## Modelos de dados

### Modelos ativos (nova arquitetura v3)

| Modelo            | Tabela               | Propósito                                              |
|-------------------|----------------------|--------------------------------------------------------|
| `Course`          | `courses`            | Snapshot de um curso do currículo                      |
| `Activity`        | `activities`         | Atividade com ID permanente sem data                   |
| `StudySlot`       | `study_slots`        | Slot materializado da escala (ex: `2026-08-11-F1`)    |
| `ActivityProgress`| `activity_progress`  | Estado mutável atual de uma atividade                  |
| `ActivityHistory` | `activity_history`   | Log append-only de eventos (nunca deletar linhas)      |
| `AppSetting`      | `app_settings`       | Configurações por instalação (chave/valor)             |
| `Milestone`       | `milestones`         | Marcos de conclusão por fase da trilha                 |

### Modelos legados (ainda presentes por compatibilidade)

| Modelo           | Tabela              | Situação                              |
|------------------|---------------------|---------------------------------------|
| `LessonProgress` | `lesson_progress`   | Legado v1/v2; não usar em código novo |
| `WeekNote`       | `week_notes`        | Legado; não usar em código novo       |
| `DeferredLesson` | `deferred_lessons`  | Legado; não usar em código novo       |

---

## Estados de uma atividade

```
pending → in_progress → done
       ↘ deferred → (volta para a fila)
       ↘ blocked
       ↘ skipped
       ↘ cancelled
```

| Status       | Significado                                          |
|--------------|------------------------------------------------------|
| `pending`    | Não iniciada                                         |
| `in_progress`| Iniciada no slot atual                               |
| `done`       | Concluída                                            |
| `deferred`   | Não realizada; devolvida à fila                      |
| `blocked`    | Aguarda recurso ou pré-requisito                     |
| `skipped`    | Retirada conscientemente da fila                     |
| `cancelled`  | Removida definitivamente                             |

---

## Lógica da escala 12x36

A escala é calculada por diferença de dias inteiros a partir de uma data âncora
configurada pelo usuário no primeiro acesso (salva em `AppSetting`).

```python
# Simplificação do scale_service.py
days_diff = (current_date - anchor_date).days
day_type = "FOLGA" if days_diff % 2 == 0 else "TRABALHO"
```

**Slots gerados automaticamente:**

| Tipo de dia | Slots       | Duração de cada slot |
|-------------|-------------|----------------------|
| FOLGA       | F1, F2, F3, F4 | 30 min cada       |
| TRABALHO    | T1, T2      | 30 min cada          |

IDs de slots seguem o padrão `YYYY-MM-DD-{código}` (ex: `2026-08-11-F1`).

---

## API REST principal

### Cursos e atividades

| Método | Endpoint                                    | Finalidade                        |
|--------|---------------------------------------------|-----------------------------------|
| GET    | `/api/courses`                              | Listar cursos                     |
| GET    | `/api/courses/{course_id}`                  | Detalhes de um curso              |
| GET    | `/api/activities`                           | Listar atividades                 |
| GET    | `/api/activities/next`                      | Próxima atividade alocável        |
| GET    | `/api/activities/{id}`                      | Detalhes e progresso              |
| GET    | `/api/activities/{id}/history`              | Histórico da atividade            |
| POST   | `/api/activities/{id}/start`                | Iniciar                           |
| POST   | `/api/activities/{id}/complete`             | Concluir                          |
| POST   | `/api/activities/{id}/defer`                | Adiar e reagendar                 |
| POST   | `/api/activities/{id}/block`                | Bloquear                          |
| POST   | `/api/activities/{id}/skip`                 | Pular                             |
| POST   | `/api/activities/{id}/cancel`               | Cancelar                          |
| POST   | `/api/activities/{id}/note`                 | Adicionar nota sem mudar estado   |

### Agenda

| Método | Endpoint                           | Finalidade                              |
|--------|------------------------------------|-----------------------------------------|
| GET    | `/api/schedule/today`              | Agenda do dia atual                     |
| GET    | `/api/schedule/range`              | Agenda por período                      |
| POST   | `/api/schedule/generate`           | Gerar slots (idempotente)               |
| POST   | `/api/schedule/slots/{id}/allocate`| Alocar atividade em um slot             |

### Progresso e histórico

| Método | Endpoint                  | Finalidade                      |
|--------|---------------------------|---------------------------------|
| GET    | `/api/progress/summary`   | Progresso geral                 |
| GET    | `/api/progress/phases`    | Progresso por fase              |
| GET    | `/api/progress/courses`   | Progresso por curso             |
| GET    | `/api/history`            | Histórico de execução           |
| GET    | `/api/stats`              | Estatísticas consolidadas       |

### Configurações

| Método | Endpoint               | Finalidade                            |
|--------|------------------------|---------------------------------------|
| GET    | `/api/settings`        | Ler configurações da instalação       |
| POST   | `/api/settings`        | Salvar configurações                  |

---

## Convenções e regras do domínio

1. **IDs de atividades nunca contêm datas.**
   - ✅ `linux-admin-sec03-lesson01`
   - ❌ `2026-08-11-linux-admin`

2. **O currículo oficial vive em `data/curriculum.py`.**
   Nunca editar dados de cursos e atividades diretamente no banco.

3. **Seeds são idempotentes.**
   Rodar o seed múltiplas vezes não deve duplicar dados.

4. **`ActivityHistory` é append-only.**
   Nunca deletar registros de histórico.

5. **Slots têm duração fixa de 30 minutos.**
   O banco tem uma constraint que reforça isso.

6. **Não usar `WEEKS` em código novo.**
   É uma abstração legada da v1/v2.

7. **Não impor prazo final rígido.**
   O sistema mede progresso por competências, não por datas.

8. **`preferred_day_type`** pode ser `"FOLGA"`, `"TRABALHO"` ou `"ANY"`.

9. **`preferred_slot`** pode ser `"THEORY"`, `"LAB"`, `"REVIEW"` ou `"ANY"`.

---

## Variáveis de ambiente

| Variável           | Padrão        | Descrição                                      |
|--------------------|---------------|------------------------------------------------|
| `SCALE_ANCHOR_DATE`| `2030-01-01`  | Data âncora inicial (sobreposta pelo AppSetting) |
| `APP_VERSION`      | `dev`         | Versão exibida na interface                    |
| `DATABASE_URL`     | SQLite local  | URL do banco (para override em testes)         |

O arquivo `.env.example` lista todas as variáveis disponíveis.

---

## Testes

```bash
# Rodar toda a suíte
pytest

# Com verbose
pytest -v

# Um arquivo específico
pytest tests/test_api.py -v

# Um teste específico
pytest tests/test_scale_service.py::test_nome_do_teste
```

Os testes usam um banco SQLite **em memória** (configurado em `tests/conftest.py`).
Não interferem no banco de dados real (`sre_tracker.db`).

Resultado esperado da suíte: **51 passed**.

---

## Onde está o quê

| Necessidade                                | Onde olhar                         |
|--------------------------------------------|------------------------------------|
| Adicionar um novo curso                    | `data/curriculum.py`               |
| Adicionar uma nova atividade               | `data/curriculum.py`               |
| Mudar a lógica de cálculo da escala        | `services/scale_service.py`        |
| Mudar a lógica de alocação de atividades   | `services/scheduling_service.py`   |
| Adicionar um endpoint novo                 | `routers/` + registrar em `main.py`|
| Mudar um modelo de banco                   | `models.py` + `schemas.py`         |
| Mudar o visual da interface                | `static/style.css`                 |
| Mudar a lógica do frontend                 | `static/app.js`                    |
| Mudar a estrutura HTML                     | `templates/index.html`             |
| Configurações persistidas por usuário      | `services/settings_service.py`     |
| Ver o que foi feito na última sessão       | `STATE_SAVE.md`                    |
| Ver o histórico de mudanças                | `CHANGELOG.md`                     |

---

## Pendências conhecidas (do STATE_SAVE.md)

- [ ] Paginação, busca ou filtros na tela Fila
- [ ] Migrações versionadas para mudanças futuras de schema
- [ ] Testes end-to-end adicionais para todas as ações
- [ ] Lint e pipeline de CI
- [ ] Favicon (`/favicon.ico` retorna 404 — sem impacto funcional)
- [ ] Remoção final dos modelos legados quando não houver mais consumidores

---

## Protocolo "salvar o ponto"

Ao encerrar uma sessão de desenvolvimento, atualizar `STATE_SAVE.md` com:

```
Data e hora:
Objetivo da sessão:
Concluído:
Arquivos alterados:
Testes executados:
Resultado dos testes:
Erros ou bloqueios:
Decisões e contornos:
Próximo passo exato:
Comando para retomar:
```

Transferir as mudanças relevantes para a seção `[Não lançado]` do `CHANGELOG.md`.
Não fazer commit ou push sem solicitação explícita do usuário.

---

*Versão 3.0 — agenda configurável e sustentável*
