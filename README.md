# SRE Tracker

Aplicação local para organizar uma trilha de estudos de SRE/DevOps adaptada à escala 12x36.

O sistema deixa de operar como um calendário rígido e passa a trabalhar com:

- fila ordenada de atividades;
- slots de estudo gerados pela escala real;
- reagendamento automático;
- progresso por competência;
- cursos principais e trilhas paralelas;
- projetos de portfólio;
- histórico de execução.

> **Data-base da escala:** definida por `SCALE_ANCHOR_DATE`
> **Meta mínima:** 2h nas folgas e 1h nos dias de trabalho  
> **Objetivo:** transição sustentável de Monitoramento para SRE/DevOps remoto

---

## Objetivo

Preparar o usuário para concorrer a vagas de:

- Site Reliability Engineer;
- DevOps Engineer;
- Cloud Operations Engineer;
- Platform Engineer;
- Analista de Infraestrutura com foco em automação;
- Analista de Observabilidade.

A aplicação deve ajudar a consolidar competências em:

```text
Linux e redes
→ Git, SQL e Python
→ Docker
→ AWS
→ Terraform e Ansible
→ GitHub Actions
→ Kubernetes
→ Prometheus, Grafana e OpenTelemetry
→ SLI, SLO, error budget e incidentes
```

O Zabbix permanece como diferencial técnico, integrado aos projetos e laboratórios.

## Primeiro acesso

Cada instalação mantém seu próprio perfil, agenda e progresso no banco local.
No primeiro acesso, o painel solicita:

- nome de exibição;
- data em que os estudos devem começar;
- uma data conhecida da escala 12x36;
- se essa data conhecida corresponde a `FOLGA` ou `TRABALHO`.

Depois da configuração inicial, os dados podem ser consultados ou ajustados pelo
botão **Configurar**. A lista de cursos faz parte do projeto e é compartilhada;
os dados pessoais ficam somente no banco local, que é ignorado pelo Git.

---

## Princípios do cronograma

### Sem prazo final rígido

O sistema não deve considerar o aluno atrasado por não concluir uma atividade em uma data específica.

O progresso será medido por:

- atividades concluídas;
- blocos de estudo realizados;
- horas práticas;
- competências consolidadas;
- projetos entregues;
- revisões concluídas.

### Uma trilha principal por vez

A aplicação deve manter:

1. um curso técnico principal;
2. uma trilha paralela obrigatória, quando existente:
   - AWS re/Start;
   - Canvas;
   - Google Cloud Skills.

### Prática obrigatória

Cada curso deve gerar pelo menos um resultado concreto:

- laboratório;
- script;
- pipeline;
- dashboard;
- infraestrutura;
- documentação;
- runbook;
- post-mortem;
- projeto de portfólio.

---

## Escala 12x36

A escala é calculada pela sequência de dias corridos. O formulário do primeiro
acesso é a forma recomendada de configurá-la. `SCALE_ANCHOR_DATE` continua
disponível como valor inicial para instalações automatizadas.

```python
from datetime import date

SCALE_ANCHOR = date.fromisoformat(os.getenv("SCALE_ANCHOR_DATE", "2030-01-01"))

def get_day_type(current_date: date) -> str:
    days = (current_date - SCALE_ANCHOR).days
    return "FOLGA" if days % 2 == 0 else "TRABALHO"
```

Não utilizar regras mensais de dias pares ou ímpares.

### Slots de folga

| Slot | Horário sugerido | Tipo |
|---|---|---|
| F1 | 13h30–14h00 | teoria |
| F2 | 14h10–14h40 | teoria ou exercício |
| F3 | 15h20–15h50 | laboratório |
| F4 | 16h00–16h30 | laboratório, revisão ou AWS |

Carga mínima: 2 horas.

### Slots de trabalho

| Slot | Horário sugerido | Tipo |
|---|---|---|
| T1 | 7h00–7h30 | curso principal |
| T2 | intervalo de almoço | revisão ou AWS |

Carga mínima: 1 hora.

---

## Reagendamento

Os IDs das atividades não podem conter datas.

Exemplo:

```text
linux-admin-sec03-lesson01
python-devops-alert-router-setup
terraform-state-backend-lab
```

Estados esperados:

| Status | Significado |
|---|---|
| `pending` | não iniciada |
| `in_progress` | iniciada |
| `done` | concluída |
| `deferred` | adiada e devolvida à fila |
| `blocked` | depende de recurso ou pré-requisito |
| `skipped` | retirada conscientemente |
| `cancelled` | removida definitivamente |

Ao marcar uma atividade como não feita:

1. registrar o slot perdido;
2. alterar o status para `deferred`;
3. devolver a atividade à fila;
4. alocar o próximo slot compatível;
5. preservar atividades concluídas;
6. não recalcular manualmente todo o calendário.

---

## Fases da trilha

| Fase | Tema | Conteúdo |
|---|---|---|
| 1 | Fundamentos operacionais | Linux, redes, Git, SQL e Python |
| 2 | Containers, cloud e IaC | Docker, AWS, Terraform e Ansible |
| 3 | CI/CD e orquestração | GitHub Actions, Kubernetes e Flask API |
| 4 | Observabilidade e SRE | Prometheus, Grafana, OpenTelemetry, SLO e incidentes |
| 5 | Especializações e carreira | Zabbix avançado, AWX, Google Cloud, IA e portfólio |

A lista detalhada de cursos está em [`COURSES.md`](./COURSES.md).

O contexto e as regras do projeto estão em [`MANUAL_PROJETO_SRE.md`](./MANUAL_PROJETO_SRE.md).

---

## Projetos de portfólio

### Linux, Ansible e Zabbix

Demonstrar:

- administração Linux;
- scripts Bash;
- automação com Ansible;
- instalação do Zabbix Agent;
- template e LLD;
- troubleshooting;
- documentação.

### Flask API em AWS e Kubernetes

Demonstrar:

- Python;
- testes;
- Docker;
- CI/CD;
- Terraform;
- AWS;
- Kubernetes;
- Helm;
- segurança;
- deploy.

### Observabilidade e confiabilidade

Demonstrar:

- Prometheus;
- Grafana;
- Loki;
- Tempo ou Jaeger;
- OpenTelemetry;
- SLI;
- SLO;
- error budget;
- alerta;
- runbook;
- post-mortem.

### Assistente agêntico controlado

Demonstrar:

- leitura de alertas;
- coleta autorizada de contexto;
- sugestão de diagnóstico;
- aprovação humana;
- auditoria.

---

## Trilhas paralelas

### AWS re/Start — Campinho Digital

Trilha paralela obrigatória com **prazo de encerramento: ~25/09/2026**.

As aulas acontecem de **segunda a sexta, das 19h às 20h** (registro manual no painel).

A aplicação permite registrar:

- aulas (slot de registro manual);
- módulos do Canvas;
- exercícios;
- revisões;
- pendências.

### Preparatório AWS Cloud Practitioner CLF-C02

Curso sequencial ao AWS re/Start. **Acesso expira em 25/10/2026.**

- Iniciar após o encerramento do re/Start (~25/09);
- cursar completo dentro da janela de acesso (≈ 30 dias);
- prioridade `high` — não adiar.

### Google Cloud Skills

Programa principal:

```text
Professional Cloud DevOps Engineer
https://www.skills.google/paths/20
```

Recursos disponíveis:

- 30 créditos mensais;
- US$ 10 mensais para Google Cloud.

Frequência sugerida:

- a cada quarta folga;
- substituir dois blocos da trilha principal;
- não adicionar como terceira trilha simultânea.

---

## Arquivos de configuração pessoal

Alguns arquivos contêm informações específicas de cada instalação (rotina, objetivos,
notas de sessão) e **não são versionados** — cada um está no `.gitignore`.

O repositório fornece versões de exemplo com o sufixo `.example.md`. Antes de usar
a aplicação, copie cada um e preencha com seus dados:

| Arquivo a criar | Template disponível | O que configurar |
|---|---|---|
| `MANUAL_PROJETO_SRE.md` | `MANUAL_PROJETO_SRE.example.md` | Rotina, objetivos, horários de estudo |
| `STATE_SAVE.md` | `STATE_SAVE.example.md` | Ponto de retomada entre sessões de dev |
| `.env` | `.env.example` | Data âncora da escala (`SCALE_ANCHOR_DATE`) |

```bash
# Exemplo: copiar e editar o manual
cp MANUAL_PROJETO_SRE.example.md MANUAL_PROJETO_SRE.md
# Abra o arquivo e substitua os placeholders [...] com suas informações

# Copiar e editar o ponto de retomada
cp STATE_SAVE.example.md STATE_SAVE.md

# Copiar e editar as variáveis de ambiente
cp .env.example .env
# Defina SCALE_ANCHOR_DATE com uma data real de FOLGA da sua escala
```

> Esses arquivos ficam apenas na sua máquina local. Qualquer `git push` os ignora automaticamente.

---


Existem dois modos de execução. O **Docker Compose é o método recomendado** para uso
cotidiano — isola dependências e garante persistência automática do banco de dados.

---

### Modo 1 — Docker Compose (recomendado)

#### Requisitos

- Docker e Docker Compose instalados.

#### Primeiro uso

```bash
cd ~/projetos/painel-estudos-sre

# Garante que o arquivo de banco existe antes do primeiro up
touch sre_tracker.db

docker compose up -d
```

A aplicação ficará disponível em:

```text
http://localhost:8000
```

O arquivo `docker-compose.yml` já configura:

- publicação da porta `8000` no host;
- bind mount do `sre_tracker.db` (seus dados nunca ficam dentro da imagem);
- restart automático (`unless-stopped`);
- health check a cada 60 s.

#### Atualizar a aplicação sem perder dados

```bash
# 1. Backup de segurança
cp sre_tracker.db sre_tracker.db.bak-$(date +%Y%m%d-%H%M)

# 2. Rebuild com o código novo
docker compose build

# 3. Recria o container (o banco no host não é tocado)
docker compose up -d
```

> **Nota:** se um curso for removido do currículo, as atividades e progresso
> associados não são deletados automaticamente (proteção contra perda acidental).
> Para remover registros órfãos do banco, execute uma migração manual com
> `sqlite3 sre_tracker.db` antes de subir a nova imagem.

#### Comandos úteis

```bash
# Ver status e porta publicada
docker compose ps

# Acompanhar logs em tempo real
docker compose logs -f --tail=30

# Parar sem remover o container
docker compose stop

# Parar e remover o container (banco permanece no host)
docker compose down
```

---

### Modo 2 — Python local (desenvolvimento)

#### Requisitos

- Python 3.12 ou compatível;
- ambiente virtual recomendado.

#### Instalação

```bash
cd ~/projetos/painel-estudos-sre

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

#### Inicialização

```bash
# Abre o navegador automaticamente
python main.py

# Ou com hot-reload para desenvolvimento
uvicorn main:app --reload
```

A aplicação ficará disponível em:

```text
http://localhost:8000
```

#### Testes

```bash
pytest
# ou com verbose
pytest -v
```

---

## API atual

### Cursos e atividades

| Método | Endpoint | Finalidade |
|---|---|---|
| `GET` | `/api/courses` | listar cursos |
| `GET` | `/api/courses/{course_id}` | detalhes de um curso |
| `GET` | `/api/activities` | listar atividades |
| `GET` | `/api/activities/next` | próxima atividade alocável |
| `GET` | `/api/activities/{activity_id}` | detalhes e progresso de uma atividade |
| `GET` | `/api/activities/{activity_id}/history` | histórico da atividade |
| `POST` | `/api/activities/{activity_id}/start` | iniciar atividade alocada |
| `POST` | `/api/activities/{activity_id}/complete` | concluir atividade |
| `POST` | `/api/activities/{activity_id}/defer` | registrar não feito/adiamento e reagendar |
| `POST` | `/api/activities/{activity_id}/block` | bloquear atividade |
| `POST` | `/api/activities/{activity_id}/skip` | pular atividade |
| `POST` | `/api/activities/{activity_id}/cancel` | cancelar atividade |
| `POST` | `/api/activities/{activity_id}/note` | adicionar nota sem mudar o estado |
| `POST` | `/api/activities/{activity_id}/reopen` | reabrir atividade concluída/iniciada por engano |

### Agenda e escala

| Método | Endpoint | Finalidade |
|---|---|---|
| `GET` | `/api/schedule/today` | agenda do dia |
| `GET` | `/api/schedule/range` | agenda por período |
| `POST` | `/api/schedule/generate` | gerar slots idempotentemente e, opcionalmente, alocar atividades |
| `POST` | `/api/schedule/slots/{slot_id}/allocate` | alocar a próxima atividade ou uma atividade específica |

### Progresso

| Método | Endpoint | Finalidade |
|---|---|---|
| `GET` | `/api/progress/summary` | progresso geral |
| `GET` | `/api/progress/phases` | progresso por fase |
| `GET` | `/api/progress/courses` | progresso por curso |
| `GET` | `/api/history` | histórico de execução |
| `GET` | `/api/stats` | estatísticas consolidadas |

### Backup

| Método | Endpoint | Finalidade |
|---|---|---|
| `GET` | `/api/export` | exportar dados |
| `POST` | `/api/import` | restaurar dados |

---

## Modelo de dados implementado

### Course

```python
{
    "id": "linux-admin",
    "name": "Administração de Sistemas GNU/Linux",
    "provider": "Udemy",
    "url": "https://...",
    "video_hours": 9.18,
    "priority": "very_high",
    "execution": "full",
    "phase": 1,
    "status": "available",
}
```

### Activity

```python
{
    "id": "linux-admin-sec03-lesson01",
    "course_id": "linux-admin",
    "sequence": 1,
    "name": "Pipes e redirecionamentos",
    "duration_minutes": 30,
    "activity_type": "lesson",
    "preferred_day_type": "ANY",
    "preferred_slot": "THEORY",
    "status": "pending",
}
```

### StudySlot

```python
{
    "id": "2030-01-01-F1",
    "study_date": "2030-01-01",
    "day_type": "FOLGA",
    "slot_code": "F1",
    "start_time": "13:30",
    "duration_minutes": 30,
    "slot_type": "THEORY",
    "activity_id": None,
    "status": "available",
}
```

### ActivityHistory

```python
{
    "activity_id": "linux-admin-sec03-lesson01",
    "slot_id": "2030-01-01-F1",
    "event_type": "deferred",
    "note": "Atendimento inesperado",
    "created_at": "2030-01-01T14:05:00",
}
```

---

## Estrutura atual do projeto

```text
painel-estudos-sre/
├── main.py                  # Entrypoint: FastAPI + lifespan + seed + abre browser
├── models.py                # Modelos ORM (SQLAlchemy)
├── schemas.py               # Schemas Pydantic
├── database.py              # Engine SQLite, SessionLocal, create_tables
├── config.py                # Leitura de variáveis de ambiente
├── data/
│   └── curriculum.py        # FONTE OFICIAL de COURSES, ACTIVITIES e MILESTONES
├── routers/
│   ├── activities.py
│   ├── courses.py
│   ├── history.py
│   ├── schedule.py
│   ├── progress.py
│   ├── stats.py
│   ├── milestones.py
│   ├── settings.py
│   ├── deferred.py
│   ├── notes.py
│   └── serializers.py
├── services/
│   ├── curriculum_seed.py
│   ├── scale_service.py
│   ├── scheduling_service.py
│   ├── reporting_service.py
│   └── settings_service.py
├── templates/
│   └── index.html
├── static/
│   ├── app.js
│   └── style.css
├── tests/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── COURSES.md
├── MANUAL_PROJETO_SRE.md
├── CHANGELOG.md
├── STATE_SAVE.md
└── README.md
```

---

## Roadmap de evolução da aplicação

### Concluído

- documentação principal alinhada à agenda dinâmica;
- modelos, schemas e seed do currículo;
- escala 12x36 e geração idempotente de slots;
- motor de alocação e reagendamento;
- API dinâmica e compatibilidade de exportação;
- frontend com Hoje, Fila, Cursos, Roadmap, Projetos, trilhas, Histórico e Estatísticas;
- testes unitários, de integração e de contrato do frontend;
- Docker Compose com bind mount para persistência do banco;
- currículo ajustado: prazos do AWS re/Start (~25/09) e CLF-C02 (acesso até 25/10);
- seed robusto: `sequence` não é atualizada em atividades existentes (evita conflito UNIQUE).

### Próximas melhorias

- paginação, busca ou filtros na Fila;
- migrações versionadas para mudanças futuras de schema;
- testes end-to-end adicionais para todas as ações;
- lint e pipeline de integração contínua;
- remoção final dos adaptadores legados quando não houver consumidores.

---

## Critérios de sucesso do sistema

O painel será considerado funcional quando:

- identificar corretamente folgas e trabalhos;
- gerar 4 slots nas folgas;
- gerar 2 slots nos trabalhos;
- permitir concluir uma atividade;
- permitir adiar sem perder a atividade;
- alocar a atividade adiada no próximo slot compatível;
- preservar histórico;
- mostrar a próxima atividade correta;
- calcular progresso por competência;
- não depender de prazo final rígido;
- exportar e restaurar dados.

---

## Direção de carreira

Não é necessário concluir todo o roadmap para começar a concorrer a vagas.

A candidatura pode começar quando houver domínio demonstrável de:

- Linux;
- redes;
- Git;
- Python ou Bash;
- Docker;
- fundamentos de cloud;
- Terraform;
- CI/CD;
- Kubernetes básico;
- monitoramento;
- incidentes;
- dois projetos documentados.

---

## Documentação relacionada

- [`COURSES.md`](./COURSES.md): catálogo e ordem pedagógica;
- [`MANUAL_PROJETO_SRE.md`](./MANUAL_PROJETO_SRE.md): contexto, rotina e regras;
- [`CHANGELOG.md`](./CHANGELOG.md): histórico das alterações implementadas;
- [`STATE_SAVE.md`](./STATE_SAVE.md): último ponto de retomada do desenvolvimento;
- `data/curriculum.py`: fonte oficial de `COURSES` e `ACTIVITIES`;
- `docs_planejamento/`: documentos históricos do cronograma anterior, não normativos.

---

*Versão 3.1 — currículo com prazos, Docker Compose e seed robusto*  
*Cronograma dinâmico para escala 12x36*  
*Conhecimento consolidado, projetos verificáveis e transição sustentável.*
