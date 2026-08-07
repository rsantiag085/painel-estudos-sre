"""
data/curriculum.py — Catálogo dinâmico do roadmap SRE/DevOps

Versão 3.0
Data-base da escala: 05/08/2026 = FOLGA

Este módulo não distribui atividades em datas fixas.
Ele define:

- fases;
- cursos;
- atividades ordenadas;
- milestones;
- regras de escala 12x36;
- tipos de slot;
- estados permitidos.

A alocação de atividades em datas deve ser feita por um serviço de agenda.
Os IDs das atividades são permanentes e não contêm datas.
"""

from __future__ import annotations

from datetime import date
from typing import Final, Literal, TypedDict


# ============================================================================
# Tipos
# ============================================================================

DayType = Literal["FOLGA", "TRABALHO", "ANY"]
SlotType = Literal["THEORY", "PRACTICE", "REVIEW", "AWS", "READING", "ANY"]
ActivityType = Literal[
    "lesson",
    "lab",
    "project",
    "review",
    "reading",
    "quiz",
    "exam",
]
CoursePriority = Literal["very_high", "high", "medium", "low"]
CourseExecution = Literal["full", "selective", "optional"]
CourseStatus = Literal["available", "in_progress", "planned", "future"]
ActivityStatus = Literal[
    "pending",
    "in_progress",
    "done",
    "deferred",
    "blocked",
    "skipped",
    "cancelled",
]


class PhaseData(TypedDict):
    label: str
    sub: str
    order: int


class CourseData(TypedDict):
    id: str
    name: str
    provider: str
    url: str
    video_hours: float
    priority: CoursePriority
    execution: CourseExecution
    phase: int
    status: CourseStatus
    prerequisites: list[str]
    notes: str


class ActivityData(TypedDict):
    id: str
    course_id: str
    sequence: int
    name: str
    duration_minutes: int
    activity_type: ActivityType
    preferred_day_type: DayType
    preferred_slot: SlotType
    prerequisites: list[str]
    tags: list[str]
    required: bool


class MilestoneData(TypedDict):
    id: str
    phase: int
    label: str
    required: bool


# ============================================================================
# Escala 12x36
# ============================================================================

SCALE_ANCHOR: Final[date] = date(2026, 8, 5)
"""Data conhecida como FOLGA. A sequência alterna a cada dia corrido."""

FOLGA_SLOTS: Final[list[dict[str, object]]] = [
    {
        "code": "F1",
        "label": "Folga — teoria 1",
        "start_time": "13:30",
        "duration_minutes": 30,
        "slot_type": "THEORY",
    },
    {
        "code": "F2",
        "label": "Folga — teoria 2",
        "start_time": "14:10",
        "duration_minutes": 30,
        "slot_type": "THEORY",
    },
    {
        "code": "F3",
        "label": "Folga — prática 1",
        "start_time": "15:20",
        "duration_minutes": 30,
        "slot_type": "PRACTICE",
    },
    {
        "code": "F4",
        "label": "Folga — prática/revisão",
        "start_time": "16:00",
        "duration_minutes": 30,
        "slot_type": "PRACTICE",
    },
]

TRABALHO_SLOTS: Final[list[dict[str, object]]] = [
    {
        "code": "T1",
        "label": "Trabalho — curso principal",
        "start_time": "07:00",
        "duration_minutes": 30,
        "slot_type": "THEORY",
    },
    {
        "code": "T2",
        "label": "Trabalho — almoço/revisão",
        "start_time": "12:00",
        "duration_minutes": 30,
        "slot_type": "REVIEW",
    },
]

OPTIONAL_SLOTS: Final[list[dict[str, object]]] = [
    {
        "code": "FX",
        "label": "Espera do ônibus — revisão opcional",
        "start_time": "10:30",
        "duration_minutes": 30,
        "slot_type": "READING",
    }
]

ALLOWED_ACTIVITY_STATUSES: Final[tuple[ActivityStatus, ...]] = (
    "pending",
    "in_progress",
    "done",
    "deferred",
    "blocked",
    "skipped",
    "cancelled",
)


def get_day_type(current_date: date | str) -> Literal["FOLGA", "TRABALHO"]:
    """Retorna o tipo do dia usando a sequência real 12x36."""
    if isinstance(current_date, str):
        current_date = date.fromisoformat(current_date)

    elapsed_days = (current_date - SCALE_ANCHOR).days
    return "FOLGA" if elapsed_days % 2 == 0 else "TRABALHO"


def get_slots_for_day(
    current_date: date | str,
    *,
    include_optional: bool = False,
) -> list[dict[str, object]]:
    """Retorna os modelos de slot disponíveis para uma data."""
    slots = FOLGA_SLOTS if get_day_type(current_date) == "FOLGA" else TRABALHO_SLOTS
    result = [dict(slot) for slot in slots]

    if include_optional and get_day_type(current_date) == "FOLGA":
        result.extend(dict(slot) for slot in OPTIONAL_SLOTS)

    return result


# ============================================================================
# Fases
# ============================================================================

PHASES: Final[dict[int, PhaseData]] = {
    1: {
        "label": "Fase 1 — Fundamentos Operacionais",
        "sub": "Linux · Redes · Git · SQL · Python",
        "order": 1,
    },
    2: {
        "label": "Fase 2 — Containers, Cloud e IaC",
        "sub": "Docker · AWS · Terraform · Ansible",
        "order": 2,
    },
    3: {
        "label": "Fase 3 — CI/CD e Orquestração",
        "sub": "GitHub Actions · Kubernetes · Flask API",
        "order": 3,
    },
    4: {
        "label": "Fase 4 — Observabilidade e SRE",
        "sub": "Prometheus · Grafana · OpenTelemetry · SLO · Incidentes",
        "order": 4,
    },
    5: {
        "label": "Fase 5 — Especializações e Carreira",
        "sub": "Zabbix avançado · AWX · Google Cloud · IA · Portfólio",
        "order": 5,
    },
}


# ============================================================================
# Cursos
# ============================================================================

COURSES: Final[list[CourseData]] = [
    {
        "id": "linux-admin",
        "name": "Administração de Sistemas GNU/Linux: Fundamentos e Prática",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/adm-so-gnulinux/",
        "video_hours": 9.18,
        "priority": "very_high",
        "execution": "full",
        "phase": 1,
        "status": "available",
        "prerequisites": [],
        "notes": "Curso principal de Linux. Acelerar conteúdos já dominados.",
    },
    {
        "id": "networks-devops",
        "name": "Fundamentos de Redes para DevOps",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/fundamentos-de-redes-para-devops/?couponCode=KEEPLEARNING",
        "video_hours": 0.0,
        "priority": "very_high",
        "execution": "full",
        "phase": 1,
        "status": "planned",
        "prerequisites": ["linux-admin"],
        "notes": "Curso ainda não adquirido. Principal lacuna atual.",
    },
    {
        "id": "git-github",
        "name": "Git e GitHub — trilha gratuita",
        "provider": "GitHub Skills / Learn Git Branching / Pro Git",
        "url": "https://www.youtube.com/watch?v=84FhNXNWoig&list=PLvlkVRRKOYFQyKmdrassLNxkzSMM6tcSL",
        "video_hours": 0.0,
        "priority": "high",
        "execution": "full",
        "phase": 1,
        "status": "available",
        "prerequisites": ["linux-admin"],
        "notes": "Usar recursos gratuitos antes de comprar curso específico.",
    },
    {
        "id": "sql-intro",
        "name": "Introdução a Bancos de Dados e Linguagem SQL",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/introducao-a-bancos-de-dados-e-linguagem-sql/",
        "video_hours": 1.97,
        "priority": "medium",
        "execution": "full",
        "phase": 1,
        "status": "available",
        "prerequisites": [],
        "notes": "Fundamentos relacionais, DDL, DML, SELECT e JOIN.",
    },
    {
        "id": "python-devops",
        "name": "Python para DevOps",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/python-para-devops/",
        "video_hours": 7.30,
        "priority": "high",
        "execution": "full",
        "phase": 1,
        "status": "available",
        "prerequisites": ["linux-admin", "git-github"],
        "notes": "Curso principal de Python aplicado a operações.",
    },
    {
        "id": "docker",
        "name": "Docker — formação dedicada",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/docker-zero-avancado",
        "video_hours": 0.0,
        "priority": "very_high",
        "execution": "full",
        "phase": 2,
        "status": "planned",
        "prerequisites": ["linux-admin", "git-github"],
        "notes": "Curso ainda não adquirido. Deve vir antes de Kubernetes.",
    },
    {
        "id": "aws-restart",
        "name": "AWS re/Start — Campinho Digital",
        "provider": "Campinho Digital",
        "url": "",
        "video_hours": 0.0,
        "priority": "very_high",
        "execution": "full",
        "phase": 2,
        "status": "in_progress",
        "prerequisites": [],
        "notes": "Trilha paralela obrigatória enquanto estiver ativa.",
    },
    {
        "id": "aws-clf",
        "name": "Preparatório AWS Cloud Practitioner CLF-C02",
        "provider": "Cloud Basics Academy",
        "url": "https://cloudbasics.academy/plataforma/cursos/2732",
        "video_hours": 11.40,
        "priority": "low",
        "execution": "selective",
        "phase": 2,
        "status": "available",
        "prerequisites": [],
        "notes": "Usar seletivamente como nivelamento. Certificação não obrigatória.",
    },
    {
        "id": "aws-saa",
        "name": "Certificação AWS Solutions Architect Associate SAA-C03",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/certificacao-amazon-aws-2019-solutions-architect/",
        "video_hours": 30.52,
        "priority": "very_high",
        "execution": "full",
        "phase": 2,
        "status": "available",
        "prerequisites": ["linux-admin", "networks-devops"],
        "notes": "Curso principal de AWS e arquitetura cloud.",
    },
    {
        "id": "terraform-essentials",
        "name": "Terraform Essentials",
        "provider": "LinuxTips",
        "url": "https://linuxtips.io/treinamento/terraform-essentials/",
        "video_hours": 5.0,
        "priority": "high",
        "execution": "full",
        "phase": 2,
        "status": "available",
        "prerequisites": ["aws-saa", "git-github"],
        "notes": "State, backend, módulos, import e boas práticas.",
    },
    {
        "id": "ansible-sysadmin",
        "name": "Ansible para SysAdmin",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/ansible-para-sysadmin/",
        "video_hours": 18.93,
        "priority": "high",
        "execution": "full",
        "phase": 2,
        "status": "available",
        "prerequisites": ["linux-admin", "git-github"],
        "notes": "Curso principal de automação de configuração.",
    },
    {
        "id": "github-actions",
        "name": "GitHub Actions: Guia Completo — Do Zero ao Deploy",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/github-actions-guia-completo-do-zero-ao-deploy/",
        "video_hours": 7.12,
        "priority": "high",
        "execution": "full",
        "phase": 3,
        "status": "available",
        "prerequisites": ["git-github", "python-devops", "docker"],
        "notes": "Curso principal de CI/CD.",
    },
    {
        "id": "kubernetes-completo",
        "name": "Kubernetes Completo: Orquestração Docker + Projeto DevOps",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/kubernetes-power-profissional-formacao-inicial-completa/",
        "video_hours": 18.85,
        "priority": "very_high",
        "execution": "full",
        "phase": 3,
        "status": "available",
        "prerequisites": ["docker", "networks-devops"],
        "notes": "Curso principal de Kubernetes.",
    },
    {
        "id": "flask-devops",
        "name": "Projeto DevOps: Flask API — Do Código ao Deploy",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/projeto-devops-flask-api-do-codigo-ao-deploy/",
        "video_hours": 14.13,
        "priority": "very_high",
        "execution": "full",
        "phase": 3,
        "status": "available",
        "prerequisites": [
            "python-devops",
            "docker",
            "github-actions",
            "terraform-essentials",
            "kubernetes-completo",
        ],
        "notes": "Projeto integrador principal da trilha.",
    },
    {
        "id": "prometheus-grafana",
        "name": "Monitoramento de Aplicações com Prometheus e Grafana",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/monitorando-aplicacoes-com-prometheus-e-grafana/",
        "video_hours": 5.62,
        "priority": "high",
        "execution": "full",
        "phase": 4,
        "status": "available",
        "prerequisites": ["docker"],
        "notes": "Instrumentação, PromQL e dashboards.",
    },
    {
        "id": "opentelemetry",
        "name": "OpenTelemetry, logs e traces",
        "provider": "A definir",
        "url": "",
        "video_hours": 0.0,
        "priority": "high",
        "execution": "full",
        "phase": 4,
        "status": "future",
        "prerequisites": ["docker", "kubernetes-completo", "prometheus-grafana"],
        "notes": "Comprar apenas após Kubernetes e Prometheus.",
    },
    {
        "id": "sre-practices",
        "name": "Google SRE Book + Site Reliability Workbook",
        "provider": "Google",
        "url": "https://sre.google/workbook/table-of-contents/",
        "video_hours": 0.0,
        "priority": "very_high",
        "execution": "full",
        "phase": 4,
        "status": "available",
        "prerequisites": [],
        "notes": "Leitura e aplicação contínuas.",
    },
    {
        "id": "zabbix-7",
        "name": "Curso de Zabbix 7 — Completo e atualizado",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/curso-de-zabbix/",
        "video_hours": 30.20,
        "priority": "medium",
        "execution": "selective",
        "phase": 5,
        "status": "available",
        "prerequisites": ["linux-admin"],
        "notes": "Priorizar HA, LLD, Proxy, API, segurança, SLA e integrações.",
    },
    {
        "id": "awx-sysadmin",
        "name": "AWX para SysAdmin",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/awx-para-sysadmin/",
        "video_hours": 7.80,
        "priority": "medium",
        "execution": "full",
        "phase": 5,
        "status": "available",
        "prerequisites": ["ansible-sysadmin", "kubernetes-completo"],
        "notes": "Especialização em automação centralizada.",
    },
    {
        "id": "devops-automacao",
        "name": "DevOps: Automação sem Enrolação",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/devops-automacao-sem-enrolacao/",
        "video_hours": 14.58,
        "priority": "medium",
        "execution": "selective",
        "phase": 5,
        "status": "available",
        "prerequisites": [
            "docker",
            "terraform-essentials",
            "ansible-sysadmin",
            "github-actions",
            "kubernetes-completo",
        ],
        "notes": "Priorizar integração multi-cloud, KEDA, pipelines e troubleshooting.",
    },
    {
        "id": "devops-jornada",
        "name": "SRE DevOps: Jornada do Início ao Fim",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/jornada-devops-sre-do-inicio-ao-fim/",
        "video_hours": 4.03,
        "priority": "low",
        "execution": "optional",
        "phase": 5,
        "status": "available",
        "prerequisites": [],
        "notes": "Usar apenas como visão panorâmica.",
    },
    {
        "id": "devops-agentico",
        "name": "DevOps Agêntico: Sem Enrolação",
        "provider": "Udemy",
        "url": "https://www.udemy.com/course/devops-agentico-sem-enrolacao/",
        "video_hours": 4.98,
        "priority": "medium",
        "execution": "full",
        "phase": 5,
        "status": "available",
        "prerequisites": [
            "python-devops",
            "github-actions",
            "kubernetes-completo",
            "prometheus-grafana",
        ],
        "notes": "Executar no final da trilha, com segurança e aprovação humana.",
    },
    {
        "id": "google-cloud-devops",
        "name": "Professional Cloud DevOps Engineer",
        "provider": "Google Skills",
        "url": "https://www.skills.google/paths/20",
        "video_hours": 0.0,
        "priority": "medium",
        "execution": "full",
        "phase": 5,
        "status": "in_progress",
        "prerequisites": [],
        "notes": "Trilha paralela. Usar a cada quarta folga.",
    },
]


COURSE_BY_ID: Final[dict[str, CourseData]] = {
    course["id"]: course for course in COURSES
}


# ============================================================================
# Atividades
# ============================================================================

_activities: list[ActivityData] = []
_sequence = 0


def _add(
    activity_id: str,
    course_id: str,
    name: str,
    *,
    duration_minutes: int = 30,
    activity_type: ActivityType = "lesson",
    preferred_day_type: DayType = "ANY",
    preferred_slot: SlotType = "ANY",
    prerequisites: list[str] | None = None,
    tags: list[str] | None = None,
    required: bool = True,
) -> None:
    global _sequence

    if course_id not in COURSE_BY_ID:
        raise ValueError(f"Curso inexistente: {course_id}")

    if duration_minutes <= 0 or duration_minutes % 30 != 0:
        raise ValueError(
            f"A duração deve ser positiva e múltipla de 30: {activity_id}"
        )

    _sequence += 1
    _activities.append(
        {
            "id": activity_id,
            "course_id": course_id,
            "sequence": _sequence,
            "name": name,
            "duration_minutes": duration_minutes,
            "activity_type": activity_type,
            "preferred_day_type": preferred_day_type,
            "preferred_slot": preferred_slot,
            "prerequisites": prerequisites or [],
            "tags": tags or [],
            "required": required,
        }
    )


def _add_course_units(
    course_id: str,
    units: list[tuple[str, str, ActivityType, SlotType]],
    *,
    tag: str,
) -> None:
    for index, (unit_id, name, activity_type, slot_type) in enumerate(units, start=1):
        _add(
            activity_id=f"{course_id}-{unit_id}",
            course_id=course_id,
            name=name,
            activity_type=activity_type,
            preferred_slot=slot_type,
            tags=[tag],
        )


# Fase 1 — Linux
_add_course_units(
    "linux-admin",
    [
        ("001", "Preparar ambiente Linux e repositório de estudos", "lab", "PRACTICE"),
        ("002", "Estrutura de diretórios e navegação", "lesson", "THEORY"),
        ("003", "Manipulação de arquivos e diretórios", "lab", "PRACTICE"),
        ("004", "Pipes e redirecionamentos", "lesson", "THEORY"),
        ("005", "grep, cut, sort, uniq, tr e wc", "lab", "PRACTICE"),
        ("006", "sed, awk e expressões regulares", "lesson", "THEORY"),
        ("007", "Laboratório de análise de logs", "lab", "PRACTICE"),
        ("008", "Usuários, grupos e permissões", "lesson", "THEORY"),
        ("009", "sudoers e princípio do menor privilégio", "lab", "PRACTICE"),
        ("010", "Processos e sinais", "lesson", "THEORY"),
        ("011", "systemd e journald — complemento", "lab", "PRACTICE"),
        ("012", "Shell Script: variáveis, condições e loops", "lesson", "THEORY"),
        ("013", "Shell Script: funções e tratamento de erros", "lab", "PRACTICE"),
        ("014", "Criar check_cpu.sh e check_memory.sh", "project", "PRACTICE"),
        ("015", "Criar check_disk.sh e check_process.sh", "project", "PRACTICE"),
        ("016", "Criar check_port.sh e analyze_log.sh", "project", "PRACTICE"),
        ("017", "Documentar linux-sre-toolkit", "project", "PRACTICE"),
        ("018", "Revisão e desafio final de Linux", "review", "REVIEW"),
    ],
    tag="linux",
)

# Redes
_add_course_units(
    "networks-devops",
    [
        ("001", "Modelo TCP/IP e encapsulamento", "lesson", "THEORY"),
        ("002", "IPv4, CIDR e subnetting", "lesson", "THEORY"),
        ("003", "Roteamento, gateway, NAT e firewall", "lesson", "THEORY"),
        ("004", "TCP, UDP, portas e sockets", "lesson", "THEORY"),
        ("005", "DNS na prática com dig e resolvectl", "lab", "PRACTICE"),
        ("006", "HTTP e HTTPS com curl", "lab", "PRACTICE"),
        ("007", "TLS com openssl s_client", "lab", "PRACTICE"),
        ("008", "Diagnóstico com ip, ss, ping, traceroute e mtr", "lab", "PRACTICE"),
        ("009", "Captura básica com tcpdump", "lab", "PRACTICE"),
        ("010", "Criar runbook de troubleshooting de rede", "project", "PRACTICE"),
        ("011", "Revisão de redes para SRE", "review", "REVIEW"),
    ],
    tag="network",
)

# Git
_add_course_units(
    "git-github",
    [
        ("001", "Configurar Git e identidade", "lab", "PRACTICE"),
        ("002", "Commits, histórico e boas mensagens", "lesson", "THEORY"),
        ("003", "Branches e merge", "lab", "PRACTICE"),
        ("004", "Rebase e resolução de conflitos", "lab", "PRACTICE"),
        ("005", "Remotos, fetch, pull e push", "lesson", "THEORY"),
        ("006", "Pull request e revisão", "lab", "PRACTICE"),
        ("007", "Tags, releases e .gitignore", "lesson", "THEORY"),
        ("008", "Publicar linux-sre-toolkit no GitHub", "project", "PRACTICE"),
        ("009", "Revisão de Git e GitHub", "review", "REVIEW"),
    ],
    tag="git",
)

# SQL
_add_course_units(
    "sql-intro",
    [
        ("001", "Banco relacional, tabelas e chaves", "lesson", "THEORY"),
        ("002", "DDL: CREATE, ALTER e DROP", "lab", "PRACTICE"),
        ("003", "DML: INSERT, UPDATE e DELETE", "lab", "PRACTICE"),
        ("004", "SELECT, filtros e ordenação", "lab", "PRACTICE"),
        ("005", "JOIN e agregações", "lab", "PRACTICE"),
        ("006", "Modelar incident-database", "project", "PRACTICE"),
        ("007", "Criar consultas operacionais", "project", "PRACTICE"),
        ("008", "Revisão de SQL", "review", "REVIEW"),
    ],
    tag="sql",
)

# Python
_add_course_units(
    "python-devops",
    [
        ("001", "Ambiente virtual, projeto e dependências", "lab", "PRACTICE"),
        ("002", "Variáveis, tipos e estruturas", "lesson", "THEORY"),
        ("003", "Condições, loops e funções", "lesson", "THEORY"),
        ("004", "Type hints e organização de código", "lesson", "THEORY"),
        ("005", "Tratamento de erros", "lab", "PRACTICE"),
        ("006", "Logging estruturado", "lab", "PRACTICE"),
        ("007", "Leitura e escrita de YAML e JSON", "lab", "PRACTICE"),
        ("008", "Criar CLI parametrizada", "project", "PRACTICE"),
        ("009", "Consumir API REST com timeout", "lab", "PRACTICE"),
        ("010", "Retries e backoff — complemento", "lab", "PRACTICE"),
        ("011", "Projeto Freeze Checker", "project", "PRACTICE"),
        ("012", "Kubernetes Python SDK — teoria", "lesson", "THEORY"),
        ("013", "Projeto CLI Kubernetes", "project", "PRACTICE"),
        ("014", "FastAPI e endpoints", "lesson", "THEORY"),
        ("015", "Projeto Alert Router — estrutura", "project", "PRACTICE"),
        ("016", "Alert Router — classificação e entrega", "project", "PRACTICE"),
        ("017", "Adicionar health check e métricas", "project", "PRACTICE"),
        ("018", "Adicionar pytest — complemento", "project", "PRACTICE"),
        ("019", "Documentar e publicar projetos Python", "project", "PRACTICE"),
        ("020", "Revisão de Python para DevOps", "review", "REVIEW"),
    ],
    tag="python",
)

# Fase 2 — Docker
_add_course_units(
    "docker",
    [
        ("001", "Containers, imagens e arquitetura Docker", "lesson", "THEORY"),
        ("002", "docker run, exec, logs e inspect", "lab", "PRACTICE"),
        ("003", "Dockerfile e camadas", "lesson", "THEORY"),
        ("004", "Criar imagem de aplicação", "lab", "PRACTICE"),
        ("005", "Volumes e persistência", "lab", "PRACTICE"),
        ("006", "Redes Docker", "lab", "PRACTICE"),
        ("007", "Docker Compose", "lab", "PRACTICE"),
        ("008", "Health checks", "lab", "PRACTICE"),
        ("009", "Multi-stage build", "lab", "PRACTICE"),
        ("010", "Segurança e usuário não root", "lesson", "THEORY"),
        ("011", "Containerizar Alert Router", "project", "PRACTICE"),
        ("012", "Troubleshooting de containers", "lab", "PRACTICE"),
        ("013", "Revisão de Docker", "review", "REVIEW"),
    ],
    tag="docker",
)

# AWS re/Start — placeholders controlados
_add_course_units(
    "aws-restart",
    [
        ("001", "Registrar aula AWS re/Start", "lesson", "AWS"),
        ("002", "Registrar módulo obrigatório do Canvas", "lesson", "AWS"),
        ("003", "Registrar exercício prático AWS", "lab", "PRACTICE"),
        ("004", "Revisar pendências da semana AWS re/Start", "review", "REVIEW"),
    ],
    tag="aws-restart",
)

# AWS SAA
_add_course_units(
    "aws-saa",
    [
        ("001", "IAM, roles, policies e responsabilidade compartilhada", "lesson", "THEORY"),
        ("002", "Laboratório IAM com menor privilégio", "lab", "PRACTICE"),
        ("003", "EC2, AMI, EBS e modelos de compra", "lesson", "THEORY"),
        ("004", "Laboratório EC2 e Security Groups", "lab", "PRACTICE"),
        ("005", "VPC, subnets, rotas, IGW e NAT", "lesson", "THEORY"),
        ("006", "Laboratório VPC pública e privada", "lab", "PRACTICE"),
        ("007", "S3, classes, lifecycle e replicação", "lesson", "THEORY"),
        ("008", "Laboratório S3 e políticas", "lab", "PRACTICE"),
        ("009", "RDS, Aurora, Multi-AZ e réplicas", "lesson", "THEORY"),
        ("010", "Laboratório RDS e backup", "lab", "PRACTICE"),
        ("011", "ELB e Auto Scaling", "lesson", "THEORY"),
        ("012", "Laboratório ALB e Auto Scaling Group", "lab", "PRACTICE"),
        ("013", "Route 53 e políticas de roteamento", "lesson", "THEORY"),
        ("014", "CloudFront e entrega de conteúdo", "lesson", "THEORY"),
        ("015", "CloudWatch, CloudTrail e AWS Config", "lesson", "THEORY"),
        ("016", "Laboratório observabilidade AWS", "lab", "PRACTICE"),
        ("017", "Lambda, API Gateway e eventos", "lesson", "THEORY"),
        ("018", "SQS, SNS e arquiteturas assíncronas", "lesson", "THEORY"),
        ("019", "ECS, Fargate e visão geral de EKS", "lesson", "THEORY"),
        ("020", "Segurança: KMS, ACM, WAF e serviços de detecção", "lesson", "THEORY"),
        ("021", "Arquiteturas resilientes e DR", "lesson", "THEORY"),
        ("022", "Arquiteturas de custo e performance", "lesson", "THEORY"),
        ("023", "Projeto arquitetura 3 camadas", "project", "PRACTICE"),
        ("024", "Simulado parcial 1", "quiz", "REVIEW"),
        ("025", "Revisar erros do simulado 1", "review", "REVIEW"),
        ("026", "Simulado parcial 2", "quiz", "REVIEW"),
        ("027", "Revisar erros do simulado 2", "review", "REVIEW"),
        ("028", "Simulado completo", "exam", "REVIEW"),
        ("029", "Revisão final SAA-C03", "review", "REVIEW"),
    ],
    tag="aws",
)

# Terraform
_add_course_units(
    "terraform-essentials",
    [
        ("001", "Instalação, HCL e comandos principais", "lesson", "THEORY"),
        ("002", "Providers e resources", "lab", "PRACTICE"),
        ("003", "Variables, outputs e tfvars", "lab", "PRACTICE"),
        ("004", "Data sources e locals — complemento", "lab", "PRACTICE"),
        ("005", "State e ciclo de vida", "lesson", "THEORY"),
        ("006", "Backend remoto e locking", "lab", "PRACTICE"),
        ("007", "Módulos", "lesson", "THEORY"),
        ("008", "Criar módulo VPC", "project", "PRACTICE"),
        ("009", "for_each e lifecycle — complemento", "lab", "PRACTICE"),
        ("010", "Import e drift", "lab", "PRACTICE"),
        ("011", "Estruturar ambientes", "project", "PRACTICE"),
        ("012", "Validar, formatar e documentar", "project", "PRACTICE"),
        ("013", "Revisão de Terraform", "review", "REVIEW"),
    ],
    tag="terraform",
)

# Ansible
_add_course_units(
    "ansible-sysadmin",
    [
        ("001", "Arquitetura, instalação e ansible.cfg", "lesson", "THEORY"),
        ("002", "Inventário estático e ad hoc", "lab", "PRACTICE"),
        ("003", "YAML e playbooks", "lesson", "THEORY"),
        ("004", "Variables, facts e templates", "lab", "PRACTICE"),
        ("005", "Handlers, conditions e loops", "lab", "PRACTICE"),
        ("006", "Blocks e tratamento de erros", "lab", "PRACTICE"),
        ("007", "Roles", "lesson", "THEORY"),
        ("008", "Criar role Nginx", "project", "PRACTICE"),
        ("009", "Galaxy e Collections", "lesson", "THEORY"),
        ("010", "Ansible Vault", "lab", "PRACTICE"),
        ("011", "Linux e Windows", "lesson", "THEORY"),
        ("012", "Inventário dinâmico AWS", "lab", "PRACTICE"),
        ("013", "Instalar Docker com Ansible", "project", "PRACTICE"),
        ("014", "Instalar Zabbix Agent com Ansible", "project", "PRACTICE"),
        ("015", "Validar idempotência", "lab", "PRACTICE"),
        ("016", "Adicionar ansible-lint — complemento", "lab", "PRACTICE"),
        ("017", "Documentar ansible-sre-lab", "project", "PRACTICE"),
        ("018", "Revisão de Ansible", "review", "REVIEW"),
    ],
    tag="ansible",
)

# Fase 3 — GitHub Actions
_add_course_units(
    "github-actions",
    [
        ("001", "Workflows, jobs, steps e actions", "lesson", "THEORY"),
        ("002", "Eventos e filtros", "lab", "PRACTICE"),
        ("003", "Contexts, expressions e conditions", "lab", "PRACTICE"),
        ("004", "Jobs paralelos e dependências", "lab", "PRACTICE"),
        ("005", "Matrix strategy", "lab", "PRACTICE"),
        ("006", "Secrets e environments", "lesson", "THEORY"),
        ("007", "Pipeline Python: lint e testes", "project", "PRACTICE"),
        ("008", "Pipeline Python: segurança", "project", "PRACTICE"),
        ("009", "Pipeline Docker: build e push", "project", "PRACTICE"),
        ("010", "Cache e artifacts — complemento", "lab", "PRACTICE"),
        ("011", "Concurrency — complemento", "lab", "PRACTICE"),
        ("012", "Reusable workflows — complemento", "lab", "PRACTICE"),
        ("013", "OIDC para cloud — complemento", "lab", "PRACTICE"),
        ("014", "Pipeline Terraform", "project", "PRACTICE"),
        ("015", "Deploy com aprovação", "project", "PRACTICE"),
        ("016", "Documentar pipeline completa", "project", "PRACTICE"),
        ("017", "Revisão de GitHub Actions", "review", "REVIEW"),
    ],
    tag="cicd",
)

# Kubernetes
_add_course_units(
    "kubernetes-completo",
    [
        ("001", "Arquitetura e componentes", "lesson", "THEORY"),
        ("002", "kubectl e YAML", "lab", "PRACTICE"),
        ("003", "Pods, ReplicaSets e Deployments", "lesson", "THEORY"),
        ("004", "Rollout e rollback", "lab", "PRACTICE"),
        ("005", "Namespaces e Services", "lesson", "THEORY"),
        ("006", "Laboratório de Services", "lab", "PRACTICE"),
        ("007", "Liveness, readiness e startup probes", "lab", "PRACTICE"),
        ("008", "Requests, limits e QoS", "lab", "PRACTICE"),
        ("009", "ConfigMaps e Secrets", "lab", "PRACTICE"),
        ("010", "Volumes, PV e PVC", "lesson", "THEORY"),
        ("011", "StatefulSets", "lab", "PRACTICE"),
        ("012", "DaemonSets, Jobs e CronJobs", "lesson", "THEORY"),
        ("013", "Endpoints e EndpointSlices", "lesson", "THEORY"),
        ("014", "RBAC e ServiceAccounts", "lab", "PRACTICE"),
        ("015", "Ingress — complemento", "lab", "PRACTICE"),
        ("016", "HPA — complemento", "lab", "PRACTICE"),
        ("017", "NetworkPolicy — complemento", "lab", "PRACTICE"),
        ("018", "Affinity, taints e tolerations — complemento", "lab", "PRACTICE"),
        ("019", "PodDisruptionBudget — complemento", "lab", "PRACTICE"),
        ("020", "Troubleshooting de workloads", "lab", "PRACTICE"),
        ("021", "Projeto Kubernetes", "project", "PRACTICE"),
        ("022", "Documentar runbook Kubernetes", "project", "PRACTICE"),
        ("023", "Revisão de Kubernetes", "review", "REVIEW"),
    ],
    tag="kubernetes",
)

# Flask integrador
_add_course_units(
    "flask-devops",
    [
        ("001", "Estrutura Flask e MongoDB", "lesson", "THEORY"),
        ("002", "Testes com pytest", "lab", "PRACTICE"),
        ("003", "Docker e Compose", "project", "PRACTICE"),
        ("004", "Makefile, Black, Flake8 e Bandit", "lab", "PRACTICE"),
        ("005", "Pipeline CI", "project", "PRACTICE"),
        ("006", "Kind e manifests Kubernetes", "project", "PRACTICE"),
        ("007", "Probes e recursos", "lab", "PRACTICE"),
        ("008", "Helm", "project", "PRACTICE"),
        ("009", "Sealed Secrets", "lab", "PRACTICE"),
        ("010", "Terraform, EKS e ECR", "project", "PRACTICE"),
        ("011", "Ansible e ambiente auxiliar", "project", "PRACTICE"),
        ("012", "Route 53, ExternalDNS e TLS", "project", "PRACTICE"),
        ("013", "OIDC GitHub para AWS", "lab", "PRACTICE"),
        ("014", "RBAC", "lab", "PRACTICE"),
        ("015", "Adicionar métricas RED", "project", "PRACTICE"),
        ("016", "Adicionar logs estruturados", "project", "PRACTICE"),
        ("017", "Adicionar tracing", "project", "PRACTICE"),
        ("018", "Definir SLO e alertas", "project", "PRACTICE"),
        ("019", "Criar runbook", "project", "PRACTICE"),
        ("020", "Executar incidente simulado e post-mortem", "project", "PRACTICE"),
        ("021", "Revisar e publicar projeto", "review", "REVIEW"),
    ],
    tag="capstone",
)

# Fase 4 — Prometheus/Grafana
_add_course_units(
    "prometheus-grafana",
    [
        ("001", "Arquitetura e pull model", "lesson", "THEORY"),
        ("002", "Counter e Gauge", "lab", "PRACTICE"),
        ("003", "Histogram e Summary", "lab", "PRACTICE"),
        ("004", "Instrumentar aplicação", "project", "PRACTICE"),
        ("005", "PromQL básico", "lesson", "THEORY"),
        ("006", "PromQL aplicado a RED", "lab", "PRACTICE"),
        ("007", "Dashboard Grafana", "project", "PRACTICE"),
        ("008", "Alertmanager — complemento", "lab", "PRACTICE"),
        ("009", "Recording rules — complemento", "lab", "PRACTICE"),
        ("010", "Service discovery e relabeling — complemento", "lesson", "THEORY"),
        ("011", "Cardinalidade — complemento", "review", "REVIEW"),
        ("012", "Node Exporter e Blackbox Exporter", "lab", "PRACTICE"),
        ("013", "kube-state-metrics", "lab", "PRACTICE"),
        ("014", "Criar prometheus-sre-lab", "project", "PRACTICE"),
        ("015", "Revisão de Prometheus e Grafana", "review", "REVIEW"),
    ],
    tag="observability",
)

# OpenTelemetry
_add_course_units(
    "opentelemetry",
    [
        ("001", "Conceitos de métricas, logs e traces", "lesson", "THEORY"),
        ("002", "OpenTelemetry SDK", "lesson", "THEORY"),
        ("003", "Instrumentação automática", "lab", "PRACTICE"),
        ("004", "Instrumentação manual", "lab", "PRACTICE"),
        ("005", "Collector", "lesson", "THEORY"),
        ("006", "Pipelines do Collector", "lab", "PRACTICE"),
        ("007", "Propagação de contexto", "lab", "PRACTICE"),
        ("008", "Sampling e cardinalidade", "review", "REVIEW"),
        ("009", "Loki", "lab", "PRACTICE"),
        ("010", "Tempo ou Jaeger", "lab", "PRACTICE"),
        ("011", "Correlação no Grafana", "project", "PRACTICE"),
        ("012", "OpenTelemetry em Kubernetes", "project", "PRACTICE"),
        ("013", "Revisão de OpenTelemetry", "review", "REVIEW"),
    ],
    tag="opentelemetry",
)

# SRE practices
_add_course_units(
    "sre-practices",
    [
        ("001", "Introdução a SRE e gestão de risco", "reading", "READING"),
        ("002", "SLI, SLO e SLA", "reading", "READING"),
        ("003", "Criar SLO de disponibilidade", "project", "PRACTICE"),
        ("004", "Criar SLO de latência", "project", "PRACTICE"),
        ("005", "Error budget", "reading", "READING"),
        ("006", "Política de error budget", "project", "PRACTICE"),
        ("007", "Burn rate e alertas multiwindow", "project", "PRACTICE"),
        ("008", "Toil e automação", "reading", "READING"),
        ("009", "Mapear toil da rotina atual", "project", "PRACTICE"),
        ("010", "Monitoramento de sistemas distribuídos", "reading", "READING"),
        ("011", "Alertas acionáveis", "project", "PRACTICE"),
        ("012", "On-call e resposta a incidentes", "reading", "READING"),
        ("013", "Criar runbook", "project", "PRACTICE"),
        ("014", "Executar exercício de incidente", "project", "PRACTICE"),
        ("015", "Escrever post-mortem sem culpabilização", "project", "PRACTICE"),
        ("016", "Capacidade e performance", "reading", "READING"),
        ("017", "Revisão de práticas SRE", "review", "REVIEW"),
    ],
    tag="sre",
)

# Fase 5 — Zabbix
_add_course_units(
    "zabbix-7",
    [
        ("001", "Revisar arquitetura atual do Zabbix", "review", "REVIEW"),
        ("002", "PostgreSQL e TimescaleDB", "lesson", "THEORY"),
        ("003", "Alta disponibilidade", "lab", "PRACTICE"),
        ("004", "LLD avançado", "lab", "PRACTICE"),
        ("005", "Zabbix Proxy", "lab", "PRACTICE"),
        ("006", "Segurança, AD e 2FA", "lab", "PRACTICE"),
        ("007", "API com Python", "project", "PRACTICE"),
        ("008", "Triggers avançadas", "lab", "PRACTICE"),
        ("009", "SLA e serviços", "project", "PRACTICE"),
        ("010", "ODBC, SNMP e web monitoring", "lab", "PRACTICE"),
        ("011", "Integração com Grafana", "project", "PRACTICE"),
        ("012", "Criar zabbix-platform-lab", "project", "PRACTICE"),
        ("013", "Documentar backup e recuperação", "project", "PRACTICE"),
        ("014", "Revisão Zabbix avançado", "review", "REVIEW"),
    ],
    tag="zabbix",
)

# AWX
_add_course_units(
    "awx-sysadmin",
    [
        ("001", "Instalação com AWX Operator", "lab", "PRACTICE"),
        ("002", "Organizações, usuários e equipes", "lesson", "THEORY"),
        ("003", "RBAC e auditoria", "lab", "PRACTICE"),
        ("004", "LDAP/AD", "lab", "PRACTICE"),
        ("005", "Projetos Git", "lab", "PRACTICE"),
        ("006", "Inventários e fontes cloud", "lab", "PRACTICE"),
        ("007", "Credenciais", "lesson", "THEORY"),
        ("008", "Job Templates e Surveys", "lab", "PRACTICE"),
        ("009", "Workflows e aprovações", "project", "PRACTICE"),
        ("010", "Agendamentos e notificações", "lab", "PRACTICE"),
        ("011", "Integração Zabbix → AWX", "project", "PRACTICE"),
        ("012", "Backup e recuperação — complemento", "project", "PRACTICE"),
        ("013", "Revisão AWX", "review", "REVIEW"),
    ],
    tag="awx",
)

# Automação sem enrolação
_add_course_units(
    "devops-automacao",
    [
        ("001", "AWS CLI e jq", "lab", "PRACTICE"),
        ("002", "Azure CLI e jq", "lab", "PRACTICE"),
        ("003", "Docker multi-stage — revisão", "lab", "PRACTICE"),
        ("004", "Pipeline Terraform + Ansible + GitHub Actions", "project", "PRACTICE"),
        ("005", "AKS, HPA e Ingress", "lab", "PRACTICE"),
        ("006", "KEDA", "lab", "PRACTICE"),
        ("007", "Datadog em Kubernetes e EC2", "lab", "PRACTICE"),
        ("008", "Troubleshooting integrado", "project", "PRACTICE"),
        ("009", "Revisão seletiva", "review", "REVIEW"),
    ],
    tag="integration",
)

# Jornada panorâmica
_add_course_units(
    "devops-jornada",
    [
        ("001", "Visão panorâmica do fluxo DevOps/SRE", "lesson", "THEORY"),
        ("002", "Revisão arquitetural das integrações", "review", "REVIEW"),
    ],
    tag="overview",
)

# DevOps agêntico
_add_course_units(
    "devops-agentico",
    [
        ("001", "Conceitos de agentes e ferramentas", "lesson", "THEORY"),
        ("002", "Contexto e arquivos de instrução", "lab", "PRACTICE"),
        ("003", "Agente em modo somente leitura", "lab", "PRACTICE"),
        ("004", "Geração de código e pull request", "project", "PRACTICE"),
        ("005", "Segurança, permissões e blast radius", "lesson", "THEORY"),
        ("006", "Human-in-the-loop", "lab", "PRACTICE"),
        ("007", "Auditoria e observabilidade", "lab", "PRACTICE"),
        ("008", "Criar agentic-sre-assistant", "project", "PRACTICE"),
        ("009", "Revisão de DevOps agêntico", "review", "REVIEW"),
    ],
    tag="ai",
)

# Google Cloud Skills — placeholders
_add_course_units(
    "google-cloud-devops",
    [
        ("001", "Registrar atividade do path Professional Cloud DevOps Engineer", "lesson", "AWS"),
        ("002", "Executar laboratório Google Skills", "lab", "PRACTICE"),
        ("003", "Registrar créditos Google Skills consumidos", "review", "REVIEW"),
        ("004", "Registrar custo e remoção de recursos GCP", "review", "REVIEW"),
    ],
    tag="gcp",
)


ACTIVITIES: Final[list[ActivityData]] = list(_activities)
ACTIVITY_BY_ID: Final[dict[str, ActivityData]] = {
    activity["id"]: activity for activity in ACTIVITIES
}


# ============================================================================
# Milestones
# ============================================================================

MILESTONES: Final[list[MilestoneData]] = [
    {
        "id": "phase-1-linux",
        "phase": 1,
        "label": "Administrar uma VM Linux e diagnosticar problemas básicos",
        "required": True,
    },
    {
        "id": "phase-1-network",
        "phase": 1,
        "label": "Diagnosticar DNS, HTTP, TLS e conectividade",
        "required": True,
    },
    {
        "id": "phase-1-code",
        "phase": 1,
        "label": "Publicar scripts Bash e Python documentados",
        "required": True,
    },
    {
        "id": "phase-2-docker",
        "phase": 2,
        "label": "Containerizar e diagnosticar uma aplicação",
        "required": True,
    },
    {
        "id": "phase-2-cloud",
        "phase": 2,
        "label": "Projetar uma arquitetura AWS resiliente e com controle de custos",
        "required": True,
    },
    {
        "id": "phase-2-iac",
        "phase": 2,
        "label": "Provisionar e configurar infraestrutura com Terraform e Ansible",
        "required": True,
    },
    {
        "id": "phase-3-cicd",
        "phase": 3,
        "label": "Implementar pipeline de CI/CD com testes e deploy controlado",
        "required": True,
    },
    {
        "id": "phase-3-k8s",
        "phase": 3,
        "label": "Operar aplicação em Kubernetes com probes, recursos e RBAC",
        "required": True,
    },
    {
        "id": "phase-3-flask",
        "phase": 3,
        "label": "Publicar o projeto Flask API do código ao deploy",
        "required": True,
    },
    {
        "id": "phase-4-observability",
        "phase": 4,
        "label": "Instrumentar aplicação com métricas, logs e traces",
        "required": True,
    },
    {
        "id": "phase-4-sre",
        "phase": 4,
        "label": "Definir SLO, error budget, alertas e runbook",
        "required": True,
    },
    {
        "id": "phase-4-incident",
        "phase": 4,
        "label": "Executar incidente simulado e escrever post-mortem",
        "required": True,
    },
    {
        "id": "phase-5-zabbix",
        "phase": 5,
        "label": "Demonstrar Zabbix integrado a automação e observabilidade",
        "required": True,
    },
    {
        "id": "phase-5-portfolio",
        "phase": 5,
        "label": "Organizar portfólio e iniciar candidaturas",
        "required": True,
    },
]


# ============================================================================
# Helpers de consulta
# ============================================================================

def get_course(course_id: str) -> CourseData | None:
    return COURSE_BY_ID.get(course_id)


def get_activity(activity_id: str) -> ActivityData | None:
    return ACTIVITY_BY_ID.get(activity_id)


def get_courses_by_phase(phase: int) -> list[CourseData]:
    return [course for course in COURSES if course["phase"] == phase]


def get_activities_by_course(course_id: str) -> list[ActivityData]:
    return [
        activity
        for activity in ACTIVITIES
        if activity["course_id"] == course_id
    ]


def get_required_activities() -> list[ActivityData]:
    return [activity for activity in ACTIVITIES if activity["required"]]


def validate_curriculum() -> list[str]:
    """Valida integridade básica e retorna erros encontrados."""
    errors: list[str] = []

    course_ids = [course["id"] for course in COURSES]
    if len(course_ids) != len(set(course_ids)):
        errors.append("Existem IDs de curso duplicados.")

    activity_ids = [activity["id"] for activity in ACTIVITIES]
    if len(activity_ids) != len(set(activity_ids)):
        errors.append("Existem IDs de atividade duplicados.")

    for course in COURSES:
        for prerequisite in course["prerequisites"]:
            if prerequisite not in COURSE_BY_ID:
                errors.append(
                    f"Curso {course['id']} depende de curso inexistente: {prerequisite}"
                )

    for activity in ACTIVITIES:
        if activity["course_id"] not in COURSE_BY_ID:
            errors.append(
                f"Atividade {activity['id']} referencia curso inexistente."
            )

        for prerequisite in activity["prerequisites"]:
            if prerequisite not in ACTIVITY_BY_ID:
                errors.append(
                    f"Atividade {activity['id']} depende de atividade inexistente: "
                    f"{prerequisite}"
                )

    return errors


# ============================================================================
# Compatibilidade temporária
# ============================================================================

# O código antigo importa WEEKS. Ele permanece como dicionário vazio apenas para
# evitar ImportError durante a migração. Endpoints baseados em semanas devem ser
# substituídos e não devem usar este valor como fonte de verdade.
WEEKS: Final[dict[int, dict[str, object]]] = {}

# Alias temporário para código antigo que importava START_DATE.
START_DATE: Final[date] = SCALE_ANCHOR


if __name__ == "__main__":
    validation_errors = validate_curriculum()

    print(f"Cursos: {len(COURSES)}")
    print(f"Atividades: {len(ACTIVITIES)}")
    print(f"Data-base: {SCALE_ANCHOR.isoformat()} = {get_day_type(SCALE_ANCHOR)}")

    if validation_errors:
        print("Erros encontrados:")
        for error in validation_errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Currículo válido.")
