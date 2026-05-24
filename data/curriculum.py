"""
data/curriculum.py — Cronograma SRE baseado em datas reais da escala 12x36
Período: 10/06/2026 a 16/01/2027 — S05–S36 (início real: segunda-feira 02/06)

Regras da escala:
  Dia ÍMPAR  → FOLGA  → 4h estudo: manhã 09–11h (2h) + tarde 14–16h (2h)
  Dia PAR    → TRABALHO → 0.5h passivo (podcast/revisão)

Lesson ID: "{YYYY-MM-DD}-{idx}"  ex: "2026-06-02-0"
"""

# ── Helpers internos ──────────────────────────────────────────────────────────
def _a(name, h, block="manha", tag=None):
    return {"name": name, "h": h, "tag": tag, "block": block, "type": "aula"}

def _l(name, h, block="tarde", tag="lab"):
    return {"name": name, "h": h, "tag": tag, "block": block, "type": "lab"}

def _b(name, h=2, block="tarde", tag="book"):
    return {"name": name, "h": h, "tag": tag, "block": block, "type": "leitura"}

def _r(name, h=2, block="tarde"):
    return {"name": name, "h": h, "tag": None, "block": block, "type": "revisao"}

def _p(name):
    return {"name": name, "h": 0.5, "tag": "book", "block": "passivo", "type": "revisao"}

def _f(name, h=2, block="free", tag="free"):
    return {"name": name, "h": h, "tag": "free", "block": block, "type": "lab"}

def _z(name, h=1, block="zabbix"):
    """Lab Zabbix semanal — badge especial no frontend."""
    return {"name": name, "h": h, "tag": "zabbix", "block": block, "type": "lab"}

def _proj(name, h=2, block="manha"):
    return {"name": name, "h": h, "tag": None, "block": block, "type": "projeto"}


# ── Fases ─────────────────────────────────────────────────────────────────────
PHASES = {
    1: {
        "label": "Fase 1 — Foundation",
        "sub": "SRE Mindset · Linux · Networking",
        "weeks": [5, 6, 7, 8],
    },
    2: {
        "label": "Fase 2 — Core Skills",
        "sub": "Python · Git · SQL · Docker",
        "weeks": [9, 10, 11, 12],
    },
    3: {
        "label": "Fase 3 — Infra & Cloud",
        "sub": "AWS SAA-C03 · Terraform · Ansible · AWX",
        "weeks": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    },
    4: {
        "label": "Fase 4 — Advanced SRE",
        "sub": "GitHub Actions · Flask DevOps · Kubernetes · Monitoring",
        "weeks": [23, 24, 25, 26, 27, 28, 29],
    },
    5: {
        "label": "Fase 5 — Especialização",
        "sub": "Capstone · Carreira · CKA Prep",
        "weeks": [30, 31, 32, 33, 34, 35, 36],
    },
}

# ── Milestones por fase ───────────────────────────────────────────────────────
MILESTONES = {
    1: [
        "VM Linux administrada com confiança",
        "Script bash funcional enviando dados ao Zabbix",
        "Entende OSI, TCP/IP, DNS, HTTP na prática",
        "Primeiro commit no GitHub com scripts da fase",
    ],
    2: [
        "Git workflow com branches e commits semânticos",
        "Python scripts operacionais (API, log parser, Zabbix integração)",
        "Banco de dados básico com backup automatizado",
        "Projeto Flask containerizado e monitorado",
    ],
    3: [
        "AWS SAA-C03 certificado (ou com data marcada)",
        "Ansible provisiona ambiente inteiro sem toque manual",
        "AWX executa playbooks via webhook do Zabbix",
        "Terraform cria infra completa em AWS",
    ],
    4: [
        "Pipeline CI/CD funcional (GitHub Actions → K8s)",
        "Projeto Flask em K8s com observabilidade completa",
        "SLOs definidos e medidos para seu projeto",
        "Postmortem escrito para um incidente real ou simulado",
    ],
    5: [
        "Capstone publicado no GitHub com README profissional",
        "Portfolio GitHub organizado com todos os projetos",
        "Mock interview gravada e analisada",
        "Blog post publicado sobre o projeto capstone",
    ],
}

# ── Cronograma — S05 a S36 ────────────────────────────────────────────────────
WEEKS = {

    # ════════════════════════════════════════════════════════
    # FASE 1 — Foundation (S05–S08)
    # ════════════════════════════════════════════════════════

    5: {
        "label": "S05",
        "focus": "SRE Mindset — Curso 1 completo + GNU/Linux início",
        "dates": {
            "2026-06-02": {"type": "F", "lessons": [
                _a("SRE DevOps Jornada — M1: O que é SRE, pilares e cultura", 2, "manha"),
                _a("SRE DevOps Jornada — M2: SLOs, SLIs, Error Budget", 2, "tarde"),
            ]},
            "2026-06-03": {"type": "T", "lessons": [
                _p("Podcast 'On-Call Me Maybe' — cultura SRE e DevOps"),
            ]},
            "2026-06-04": {"type": "F", "lessons": [
                _a("SRE DevOps Jornada — M3-4: Toil, Automation, Incident Mgmt (conclusão)", 2, "manha"),
                _b("Google SRE Book — Caps 1-2: Introduction to SRE", 2, "tarde"),
            ]},
            "2026-06-05": {"type": "T", "lessons": [
                _p("Podcast 'Linux For Everyone' — por que Linux importa no SRE"),
            ]},
            "2026-06-06": {"type": "F", "lessons": [
                _a("GNU/Linux — M1: Estrutura de diretórios + comandos básicos (ls, cp, mv, rm)", 2, "manha"),
                _a("GNU/Linux — M2: Permissões, usuários, grupos (chmod, chown, sudo)", 2, "tarde"),
            ]},
            "2026-06-07": {"type": "T", "lessons": [
                _p("Podcast 'Command Line Heroes' — história do Linux"),
            ]},
            "2026-06-08": {"type": "F", "lessons": [
                _a("GNU/Linux — M3: Processos (ps, top, htop, kill, systemctl, journald)", 2, "manha"),
                _a("GNU/Linux — M4: Gerenciamento de pacotes (apt/yum) + SSH (keys, config)", 2, "tarde"),
            ]},
        },
    },

    6: {
        "label": "S06",
        "focus": "GNU/Linux M5-6 + Networking + OverTheWire Bandit",
        "dates": {
            "2026-06-09": {"type": "F", "lessons": [
                _a("GNU/Linux — M5: Logs (journalctl, rsyslog, logrotate, /var/log)", 2, "manha"),
                _a("GNU/Linux — M6: File system, discos, LVM, partições, df/du (conclusão)", 2, "tarde"),
            ]},
            "2026-06-10": {"type": "T", "lessons": [
                _p("Podcast 'Darknet Diaries' — incidentes de infraestrutura"),
            ]},
            "2026-06-11": {"type": "F", "lessons": [
                _f("Practical Networking — OSI model, Ethernet, switches, IP addressing, subnetting", 2, "manha"),
                _l("OverTheWire Bandit — Levels 1-5 (SSH, ls, cat, find, file)", 2, "tarde"),
            ]},
            "2026-06-12": {"type": "T", "lessons": [
                _p("Podcast 'Command Line Heroes' — shell scripting"),
            ]},
            "2026-06-13": {"type": "F", "lessons": [
                _f("Practical Networking — TCP/UDP, DNS, HTTP/HTTPS, TLS handshake", 2, "manha"),
                _l("OverTheWire Bandit — Levels 6-10 (grep, sort, uniq, base64)", 2, "tarde"),
            ]},
            "2026-06-14": {"type": "T", "lessons": [
                _p("Podcast 'Practical Networking' — redes no contexto SRE"),
            ]},
            "2026-06-15": {"type": "F", "lessons": [
                _b("The Linux Command Line — Caps 1-3: Shell, navegação, manipulação de arquivos", 2, "manha"),
                _l("OverTheWire Bandit — Levels 11-15 (rot13, xxd, openssl)", 2, "tarde"),
            ]},
        },
    },

    7: {
        "label": "S07",
        "focus": "Linux avançado + Labs bash/VM + SRE Book",
        "dates": {
            "2026-06-16": {"type": "T", "lessons": [
                _p("Podcast 'Software Defined Talk' — cloud networking e SRE"),
            ]},
            "2026-06-17": {"type": "F", "lessons": [
                _b("The Linux Command Line — Caps 4-6: pipelines, redirecionamento, expansão", 2, "manha"),
                _b("Google SRE Book — Caps 3-4: Embracing Risk, SLOs na prática", 2, "tarde"),
            ]},
            "2026-06-18": {"type": "T", "lessons": [
                _p("Podcast 'Linux For Everyone' — sysadmin no dia a dia"),
            ]},
            "2026-06-19": {"type": "F", "lessons": [
                _l("Lab: configurar VM Linux (Debian/Ubuntu) + SSH key-based auth", 2, "manha"),
                _l("Lab: scripts bash — backup, monitoramento, cron jobs", 2, "tarde"),
            ]},
            "2026-06-20": {"type": "T", "lessons": [
                _p("Podcast 'Command Line Heroes' — bash e automação"),
            ]},
            "2026-06-21": {"type": "F", "lessons": [
                _b("Google SRE Book — Caps 5-6: Eliminating Toil, Monitoring Distributed Systems", 2, "manha"),
                _b("The Linux Command Line — Caps 7-9: processos, ambiente, vi básico", 2, "tarde"),
            ]},
            "2026-06-22": {"type": "T", "lessons": [
                _p("Podcast 'FLOSS Weekly' — ferramentas Linux open source"),
            ]},
        },
    },

    8: {
        "label": "S08",
        "focus": "Revisão Fase 1 + Git setup + preparação Fase 2",
        "dates": {
            "2026-06-23": {"type": "F", "lessons": [
                _r("Revisão Fase 1 — Linux, Networking, SRE Mindset: consolidar conceitos", 2, "manha"),
                _l("Lab: organizar GitHub + primeiro commit com scripts bash da Fase 1", 2, "tarde"),
            ]},
            "2026-06-24": {"type": "T", "lessons": [
                _p("Podcast 'Changelog' — open source e cultura DevOps"),
            ]},
            "2026-06-25": {"type": "F", "lessons": [
                _b("Google SRE Book — Caps 7-8: Automation, Release Engineering", 2, "manha"),
                _f("Learn Git Branching — introdução interativa (commits, branches, merges)", 2, "tarde"),
            ]},
            "2026-06-26": {"type": "T", "lessons": [
                _p("Podcast 'Talk Python to Me' — Python no DevOps"),
            ]},
            "2026-06-27": {"type": "F", "lessons": [
                _l("Lab: criar conta AWS Free Tier + setup IAM + billing alerts", 2, "manha"),
                _a("IA Aplicada a DevOps: Prompt Engineering para scripts Bash/Python e troubleshooting", 2, "tarde"),
            ]},
            "2026-06-28": {"type": "T", "lessons": [
                _p("Podcast 'Python Bytes' — ferramentas para DevOps"),
            ]},
            "2026-06-29": {"type": "F", "lessons": [
                _f("Linux Journey — Grasshopper: revisão comandos e navegação", 2, "manha"),
                _r("Revisão final Fase 1 + planejamento Fase 2 Python/Git/SQL/Docker", 2, "tarde"),
            ]},
        },
    },

    # ════════════════════════════════════════════════════════
    # FASE 2 — Core Skills (S09–S12)
    # ════════════════════════════════════════════════════════

    9: {
        "label": "S09",
        "focus": "Python para DevOps — M1 a M6",
        "dates": {
            "2026-06-30": {"type": "T", "lessons": [
                _p("Podcast 'Talk Python to Me' — Python para automação de infra"),
            ]},
            "2026-07-01": {"type": "F", "lessons": [
                _a("Python para DevOps — M1-2: variáveis, tipos, estruturas de dados", 2, "manha"),
                _a("Python para DevOps — M3-4: funções, listas, dicionários, loops", 2, "tarde"),
            ]},
            "2026-07-02": {"type": "T", "lessons": [
                _p("Podcast 'Python Bytes' — novidades Python 3.12+"),
            ]},
            "2026-07-03": {"type": "F", "lessons": [
                _a("Python para DevOps — M5-6: error handling, logging, exceptions", 2, "manha"),
                _b("Automate the Boring Stuff — Caps 1-2: Python básico, strings, listas", 2, "tarde"),
            ]},
            "2026-07-04": {"type": "T", "lessons": [
                _p("Podcast 'Real Python' — boas práticas Python"),
            ]},
            "2026-07-05": {"type": "F", "lessons": [
                _a("Python para DevOps — M7-8: subprocess, venv, pip, gerenciamento de dependências", 2, "manha"),
                _b("Automate the Boring Stuff — Caps 3-4: programas linha de comando, regex", 2, "tarde"),
            ]},
            "2026-07-06": {"type": "T", "lessons": [
                _p("Podcast 'Talk Python to Me' — automação com Python"),
            ]},
        },
    },

    10: {
        "label": "S10",
        "focus": "Python conclusão + SQL + Git",
        "dates": {
            "2026-07-07": {"type": "F", "lessons": [
                _a("Python para DevOps — M9-10: requests, APIs REST, JSON (conclusão Curso 3)", 2, "manha"),
                _l("Lab: script Python para integração com API REST (requisições, auth, JSON)", 2, "tarde"),
            ]},
            "2026-07-08": {"type": "T", "lessons": [
                _p("Podcast 'Python Bytes' — ferramentas de linting e formatação"),
            ]},
            "2026-07-09": {"type": "F", "lessons": [
                _f("SQLBolt — SQL fundamentos: SELECT, WHERE, JOINs (interativo)", 2, "manha"),
                _f("SQLBolt — SQL avançado: GROUP BY, subqueries, transactions", 2, "tarde"),
            ]},
            "2026-07-10": {"type": "T", "lessons": [
                _p("Podcast 'Talk Python to Me' — testing com pytest"),
            ]},
            "2026-07-11": {"type": "F", "lessons": [
                _l("Lab: banco de dados SQLite + Python + backup automatizado com cron", 2, "manha"),
                _a("IA Aplicada a SRE: Gerando e validando YAMLs (Ansible/K8s) e analisando logs", 2, "tarde"),
            ]},
            "2026-07-12": {"type": "T", "lessons": [
                _p("Podcast 'Changelog' — DevOps e open source"),
            ]},
            "2026-07-13": {"type": "F", "lessons": [
                _b("Pro Git Book — Caps 1-2: Getting Started, Git Basics", 2, "manha"),
                _b("Pro Git Book — Caps 3-5: Branching, Remote Branches, Rebasing", 2, "tarde"),
            ]},
        },
    },

    11: {
        "label": "S11",
        "focus": "Git avançado + Docker + Flask intro",
        "dates": {
            "2026-07-14": {"type": "T", "lessons": [
                _p("Podcast 'DevOps and Docker Talk' — containers no SRE"),
            ]},
            "2026-07-15": {"type": "F", "lessons": [
                _l("Lab: Git workflow completo — feature branch, merge, rebase, PR", 2, "manha"),
                _b("Automate the Boring Stuff — Caps 7-8: pattern matching, manipulação de arquivos", 2, "tarde"),
            ]},
            "2026-07-16": {"type": "T", "lessons": [
                _p("Podcast 'Software Defined Talk' — microserviços e containers"),
            ]},
            "2026-07-17": {"type": "F", "lessons": [
                _l("Lab: Docker — build, run, volumes, networks, docker-compose", 2, "manha"),
                _l("Lab: Flask API básica — rotas, SQLAlchemy, retornos JSON", 2, "tarde"),
            ]},
            "2026-07-18": {"type": "T", "lessons": [
                _p("Podcast 'Talk Python to Me' — Flask e APIs REST"),
            ]},
            "2026-07-19": {"type": "F", "lessons": [
                _l("Lab: containerizar Flask app — Dockerfile multi-stage + compose", 2, "manha"),
                _l("Lab: Python script de integração Zabbix API (criar host, disparar alerta)", 2, "tarde"),
            ]},
            "2026-07-20": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — introdução a orquestração"),
            ]},
        },
    },

    12: {
        "label": "S12",
        "focus": "Revisão Fase 2 + buffer + preparação Fase 3",
        "dates": {
            "2026-07-21": {"type": "F", "lessons": [
                _r("Revisão Fase 2 — Git + Python + SQL + Docker: consolidar", 2, "manha"),
                _l("Lab: commit GitHub organizado — scripts Fase 2 com README", 2, "tarde"),
            ]},
            "2026-07-22": {"type": "T", "lessons": [
                _p("Podcast 'AWS re:Invent talks' — AWS fundamentals overview"),
            ]},
            "2026-07-23": {"type": "F", "lessons": [
                _l("Lab: Zabbix integração Python API — criar templates e triggers", 2, "manha"),
                _b("Google SRE Book — Caps 9-10: Being On-Call, Troubleshooting Production", 2, "tarde"),
            ]},
            "2026-07-24": {"type": "T", "lessons": [
                _p("Flashcards AWS no celular — conceitos fundamentais"),
            ]},
            "2026-07-25": {"type": "F", "lessons": [
                _b("Pro Git Book — Caps 4-5: protocolos, rebasing, workflow de times", 2, "manha"),
                _r("Buffer Fase 2 + revisão pontos fracos + planejamento Fase 3 AWS", 2, "tarde"),
            ]},
            "2026-07-26": {"type": "T", "lessons": [
                _p("Podcast 'Software Defined Talk' — cloud computing fundamentos"),
            ]},
            "2026-07-27": {"type": "F", "lessons": [
                _r("Revisão final Fase 2 + setup ambiente AWS (CLI, credenciais, região)", 2, "manha"),
                _l("Lab: AWS CLI setup + primeiro comando S3 + IAM user criado", 2, "tarde"),
            ]},
        },
    },

    # ════════════════════════════════════════════════════════
    # FASE 3 — Infra & Cloud (S13–S22)
    # ════════════════════════════════════════════════════════

    13: {
        "label": "S13",
        "focus": "AWS SAA-C03 — IAM, EC2, VPC",
        "dates": {
            "2026-07-28": {"type": "T", "lessons": [
                _p("Podcast 'AWS re:Invent' — AWS fundamentals e arquitetura"),
            ]},
            "2026-07-29": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — IAM: users, roles, policies, MFA, best practices", 2, "manha", "aws"),
                _l("Lab: IAM console — criar roles, políticas customizadas, MFA setup", 2, "tarde"),
            ]},
            "2026-07-30": {"type": "T", "lessons": [
                _p("Flashcards AWS — IAM e EC2"),
            ]},
            "2026-07-31": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — EC2: instance types, AMIs, pricing, spot vs reserved", 2, "manha", "aws"),
                _l("Lab: EC2 — launch, connect SSH, security groups, Elastic IP", 2, "tarde"),
            ]},
            "2026-08-01": {"type": "T", "lessons": [
                _p("Podcast 'AWS re:Invent' — VPC deep dive"),
            ]},
            "2026-08-02": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — VPC: subnets, route tables, IGW, NAT Gateway, VPN", 2, "manha", "aws"),
                _l("Lab: VPC customizada — subnets públicas/privadas + Security Groups", 2, "tarde"),
            ]},
            "2026-08-03": {"type": "T", "lessons": [
                _p("Flashcards AWS — VPC e redes"),
            ]},
        },
    },

    14: {
        "label": "S14",
        "focus": "AWS — S3, RDS, ELB, Route 53",
        "dates": {
            "2026-08-04": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — S3: storage classes, versionamento, lifecycle, replication", 2, "manha", "aws"),
                _l("Lab: S3 bucket — policies, versionamento, static website hosting", 2, "tarde"),
            ]},
            "2026-08-05": {"type": "T", "lessons": [
                _p("Podcast 'AWS re:Invent' — S3 e storage"),
            ]},
            "2026-08-06": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — RDS: Multi-AZ, read replicas, backups, Aurora", 2, "manha", "aws"),
                _l("Lab: RDS MySQL — launch, snapshots, restore, parameter groups", 2, "tarde"),
            ]},
            "2026-08-07": {"type": "T", "lessons": [
                _p("Flashcards AWS — databases e storage"),
            ]},
            "2026-08-08": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — ELB: ALB, NLB, CLB, target groups, health checks", 2, "manha", "aws"),
                _l("Lab: ALB + Auto Scaling Group — launch template, scaling policies", 2, "tarde"),
            ]},
            "2026-08-09": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — Route 53: DNS, routing policies (latency, failover, weighted)", 2, "manha", "aws"),
                _l("Lab: Route 53 — hosted zone, health checks, failover routing", 2, "tarde"),
            ]},
            "2026-08-10": {"type": "T", "lessons": [
                _p("Podcast 'Software Defined Talk' — load balancing e HA"),
            ]},
        },
    },

    15: {
        "label": "S15",
        "focus": "AWS — CloudWatch, CloudFront, Security",
        "dates": {
            "2026-08-11": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — CloudWatch: metrics, alarms, logs, insights, dashboards", 2, "manha", "aws"),
                _l("Lab: CloudWatch — dashboards EC2, alarmes SNS, log groups", 2, "tarde"),
            ]},
            "2026-08-12": {"type": "T", "lessons": [
                _p("Podcast 'AWS re:Invent' — observabilidade na AWS"),
            ]},
            "2026-08-13": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — CloudFront: distribuição CDN, cache behaviors, OAI", 2, "manha", "aws"),
                _l("Lab: CloudFront distribution — S3 origin + cache policies + HTTPS", 2, "tarde"),
            ]},
            "2026-08-14": {"type": "T", "lessons": [
                _p("Flashcards AWS — segurança e compliance"),
            ]},
            "2026-08-15": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — Security: KMS, ACM, WAF, Shield, GuardDuty, Macie", 2, "manha", "aws"),
                _l("Lab: security hardening — KMS encryption, WAF rules, GuardDuty enable", 2, "tarde"),
            ]},
            "2026-08-16": {"type": "T", "lessons": [
                _p("Podcast 'AWS re:Invent' — security best practices"),
            ]},
            "2026-08-17": {"type": "F", "lessons": [
                _r("Revisão AWS S3+RDS+ELB+Route53+CloudWatch+Security", 2, "manha"),
                _b("Google SRE Book — Monitoring Distributed Systems: the four golden signals", 2, "tarde"),
            ]},
        },
    },

    16: {
        "label": "S16",
        "focus": "AWS — Lambda, SQS/SNS, ECS + revisão geral",
        "dates": {
            "2026-08-18": {"type": "T", "lessons": [
                _p("Flashcards AWS — serverless e mensageria"),
            ]},
            "2026-08-19": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — Lambda: funções, triggers, limites, layers, concurrency", 2, "manha", "aws"),
                _l("Lab: Lambda Python — trigger S3, API Gateway integration, CloudWatch logs", 2, "tarde"),
            ]},
            "2026-08-20": {"type": "T", "lessons": [
                _p("Podcast 'AWS re:Invent' — event-driven architecture"),
            ]},
            "2026-08-21": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — SQS + SNS: filas, dead letter queues, pub/sub, fanout", 2, "manha", "aws"),
                _l("Lab: SQS FIFO queue + Lambda consumer + DLQ setup", 2, "tarde"),
            ]},
            "2026-08-22": {"type": "T", "lessons": [
                _p("Podcast 'AWS re:Invent' — ECS e containers na AWS"),
            ]},
            "2026-08-23": {"type": "F", "lessons": [
                _a("AWS SAA-C03 — ECS: task definitions, services, Fargate, EKS overview", 2, "manha", "aws"),
                _l("Lab: ECS Fargate — task definition + service + ALB integration", 2, "tarde"),
            ]},
            "2026-08-24": {"type": "T", "lessons": [
                _p("Flashcards AWS — ECS, Lambda, SQS"),
            ]},
        },
    },

    17: {
        "label": "S17",
        "focus": "AWS — revisão final SAA-C03 + Terraform prep",
        "dates": {
            "2026-08-25": {"type": "F", "lessons": [
                _r("AWS SAA-C03 — revisão geral: todos os serviços, arquiteturas", 2, "manha"),
                _r("Simulado parcial SAA-C03 — 40 questões práticas + revisão de erros", 2, "tarde"),
            ]},
            "2026-08-26": {"type": "T", "lessons": [
                _p("Podcast 'AWS re:Invent' — arquiteturas serverless"),
            ]},
            "2026-08-27": {"type": "F", "lessons": [
                _r("AWS SAA-C03 — revisão pontos fracos + simulado parcial 2 (65 questões)", 2, "manha"),
                _r("Simulado completo SAA-C03 — 65 questões formato real + análise detalhada", 2, "tarde"),
            ]},
            "2026-08-28": {"type": "T", "lessons": [
                _p("Flashcards AWS — revisão final geral"),
            ]},
            "2026-08-29": {"type": "F", "lessons": [
                _r("AWS SAA-C03 — revisão final: pontos críticos + agendar prova SAA-C03", 2, "manha"),
                _l("Lab: arquitetura AWS 3-tier — VPC + EC2 + RDS + ELB + CloudWatch", 2, "tarde", "aws"),
            ]},
            "2026-08-30": {"type": "T", "lessons": [
                _p("Podcast 'HashiCorp talks' — Terraform no mercado"),
            ]},
            "2026-08-31": {"type": "F", "lessons": [
                _r("Buffer AWS + anotações finais + preparação transição para IaC", 2, "manha"),
                _l("Lab: setup ambiente Terraform — install, provider AWS, primeiro apply", 2, "tarde"),
            ]},
        },
    },

    18: {
        "label": "S18",
        "focus": "Terraform Essentials — sintaxe, módulos, state",
        "dates": {
            "2026-09-01": {"type": "T", "lessons": [
                _p("Podcast 'Infrastructure as Code' — Terraform best practices"),
            ]},
            "2026-09-02": {"type": "F", "lessons": [
                _a("Terraform Essentials — sintaxe HCL, providers, resources, data sources", 2, "manha"),
                _l("Lab: Terraform apply na AWS — VPC + EC2 + Security Groups", 2, "tarde"),
            ]},
            "2026-09-03": {"type": "T", "lessons": [
                _p("Podcast 'HashiCorp talks' — Terraform state management"),
            ]},
            "2026-09-04": {"type": "F", "lessons": [
                _a("Terraform Essentials — variables, outputs, tfvars, locals", 2, "manha"),
                _l("Lab: Terraform módulos — criar e reutilizar modules de VPC e EC2", 2, "tarde"),
            ]},
            "2026-09-05": {"type": "T", "lessons": [
                _p("Podcast 'HashiCorp talks' — Terraform remote state"),
            ]},
            "2026-09-06": {"type": "F", "lessons": [
                _a("Terraform Essentials — state backend (S3+DynamoDB), workspaces, módulos", 2, "manha"),
                _l("Lab: Terraform remote backend + state locking com DynamoDB", 2, "tarde"),
            ]},
            "2026-09-07": {"type": "T", "lessons": [
                _p("Podcast 'Ansible automates' — automação de infra"),
            ]},
        },
    },

    19: {
        "label": "S19",
        "focus": "Terraform conclusão + Ansible início",
        "dates": {
            "2026-09-08": {"type": "F", "lessons": [
                _a("Terraform conclusão — boas práticas, formatação, linting, segurança", 2, "manha"),
                _l("Lab Zabbix semanal — dashboard de alertas + template customizado", 2, "tarde"),
            ]},
            "2026-09-09": {"type": "F", "lessons": [
                _a("Ansible para SysAdmin — M1-2: fundamentos, inventários, ad-hoc commands", 2, "manha"),
                _l("Lab: ambiente Ansible setup — inventários estáticos e dinâmicos", 2, "tarde"),
            ]},
            "2026-09-10": {"type": "T", "lessons": [
                _p("Podcast 'Ansible automates' — playbooks e roles"),
            ]},
            "2026-09-11": {"type": "F", "lessons": [
                _a("Ansible para SysAdmin — M3-4: playbooks básicos, vars, loops, conditionals", 2, "manha"),
                _l("Lab: playbook Ansible — provisionamento completo servidor web Nginx", 2, "tarde"),
            ]},
            "2026-09-12": {"type": "T", "lessons": [
                _p("Podcast 'Ansible automates' — inventários dinâmicos"),
            ]},
            "2026-09-13": {"type": "F", "lessons": [
                _a("Ansible para SysAdmin — M5-6: roles estruturadas, ansible-galaxy, collections", 2, "manha"),
                _l("Lab: roles Ansible para stack completa (Nginx + PostgreSQL + app)", 2, "tarde"),
            ]},
            "2026-09-14": {"type": "T", "lessons": [
                _p("Podcast 'Ansible automates' — roles e galaxy"),
            ]},
        },
    },

    20: {
        "label": "S20",
        "focus": "Ansible — Vault, handlers, avançado",
        "dates": {
            "2026-09-15": {"type": "F", "lessons": [
                _a("Ansible para SysAdmin — M7-8: ansible-vault, handlers, tags, error handling", 2, "manha"),
                _l("Lab: Ansible vault — criptografar secrets, group_vars, host_vars", 2, "tarde"),
            ]},
            "2026-09-16": {"type": "T", "lessons": [
                _p("Podcast 'Ansible automates' — vault e segurança"),
            ]},
            "2026-09-17": {"type": "F", "lessons": [
                _a("Ansible para SysAdmin — M9-10: templates Jinja2, collections, callbacks", 2, "manha"),
                _l("Lab: roles Ansible complexas — idempotência e testando com molecule", 2, "tarde"),
            ]},
            "2026-09-18": {"type": "T", "lessons": [
                _p("Podcast 'Ansible automates' — testes e CI com Ansible"),
            ]},
            "2026-09-19": {"type": "F", "lessons": [
                _a("Ansible para SysAdmin — M11-12: avançado, plugins, callbacks, lookup", 2, "manha"),
                _l("Lab: Ansible dynamic inventory com AWS EC2 e script customizado", 2, "tarde"),
            ]},
            "2026-09-20": {"type": "T", "lessons": [
                _p("Podcast 'Changelog' — automação de infraestrutura"),
            ]},
            "2026-09-21": {"type": "F", "lessons": [
                _l("Lab Zabbix + Ansible — remediação automática de alertas via playbook", 2, "manha"),
                _r("Revisão Ansible M1-12 + commit GitHub com roles e playbooks", 2, "tarde"),
            ]},
        },
    },

    21: {
        "label": "S21",
        "focus": "Ansible avançado — performance, dynamic inventory, projeto",
        "dates": {
            "2026-09-22": {"type": "T", "lessons": [
                _p("Podcast 'Ansible automates' — deploy em produção"),
            ]},
            "2026-09-23": {"type": "F", "lessons": [
                _a("Ansible para SysAdmin — M13-14: when, until, async, poll, error handling", 2, "manha"),
                _l("Lab: Ansible completo — provisionar servidor web com zero downtime", 2, "tarde"),
            ]},
            "2026-09-24": {"type": "T", "lessons": [
                _p("Podcast 'Software Defined Talk' — IaC comparativo"),
            ]},
            "2026-09-25": {"type": "F", "lessons": [
                _a("Ansible para SysAdmin — M15: performance tuning, forks, pipelining, mitogen", 2, "manha"),
                _l("Lab: Ansible projeto final parte 1 — deploy completo infra + app", 2, "tarde"),
            ]},
            "2026-09-26": {"type": "T", "lessons": [
                _p("Podcast 'Ansible automates' — AWX e automação enterprise"),
            ]},
            "2026-09-27": {"type": "F", "lessons": [
                _a("Ansible para SysAdmin — M16-17: projeto final, pipeline CI/CD com Ansible", 2, "manha"),
                _l("Lab: Ansible projeto final parte 2 — refinamento, idempotência, docs", 2, "tarde"),
            ]},
            "2026-09-28": {"type": "T", "lessons": [
                _p("Podcast 'AWX automates' — automação enterprise"),
            ]},
        },
    },

    22: {
        "label": "S22",
        "focus": "Ansible conclusão + AWX instalação e configuração",
        "dates": {
            "2026-09-29": {"type": "F", "lessons": [
                _a("Ansible conclusão + AWX para SysAdmin — overview, arquitetura", 2, "manha"),
                _l("Lab: AWX instalação e configuração — Docker Compose setup", 2, "tarde"),
            ]},
            "2026-09-30": {"type": "T", "lessons": [
                _p("Podcast 'AWX automates' — job templates e workflows"),
            ]},
            "2026-10-01": {"type": "F", "lessons": [
                _a("AWX para SysAdmin — inventários, projetos, credenciais, organizações", 2, "manha"),
                _l("Lab: AWX Job Templates, Schedules, Surveys, Workflows", 2, "tarde"),
            ]},
            "2026-10-02": {"type": "T", "lessons": [
                _p("Podcast 'AWX automates' — RBAC e webhooks"),
            ]},
            "2026-10-03": {"type": "F", "lessons": [
                _a("AWX para SysAdmin — Webhooks, RBAC, REST API, notificações Slack", 2, "manha"),
                _l("Lab: AWX workflows complexos com aprovação manual e notificações", 2, "tarde"),
            ]},
            "2026-10-04": {"type": "T", "lessons": [
                _p("Podcast 'GitHub Actions tips' — CI/CD moderno"),
            ]},
            "2026-10-05": {"type": "F", "lessons": [
                _l("Lab: AWX projeto integrador — Zabbix alerta → AWX → remediação automática", 2, "manha"),
                _a("AWX — projeto final: Zabbix → AWX → remediação (conclusão Curso 6)", 2, "tarde"),
            ]},
        },
    },

    # ════════════════════════════════════════════════════════
    # FASE 4 — Advanced SRE (S23–S29)
    # ════════════════════════════════════════════════════════

    23: {
        "label": "S23",
        "focus": "GitHub Actions — CI/CD completo",
        "dates": {
            "2026-10-06": {"type": "T", "lessons": [
                _p("Podcast 'DevOps and Docker Talk' — GitHub Actions na prática"),
            ]},
            "2026-10-07": {"type": "F", "lessons": [
                _a("GitHub Actions — M1-2: sintaxe YAML, workflows, events, runners, contexts", 2, "manha"),
                _l("Lab: CI pipeline completa — lint + test + Docker build + push ao Registry", 2, "tarde"),
            ]},
            "2026-10-08": {"type": "T", "lessons": [
                _p("Podcast 'GitHub Actions tips' — reusable workflows"),
            ]},
            "2026-10-09": {"type": "F", "lessons": [
                _a("GitHub Actions — M3-4: secrets, Docker builds, matrix strategy, artifacts", 2, "manha"),
                _l("Lab: CD pipeline — deploy automático no K8s via GitHub Actions", 2, "tarde"),
            ]},
            "2026-10-10": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — GitOps e Argo CD"),
            ]},
            "2026-10-11": {"type": "F", "lessons": [
                _a("GitHub Actions — M5-6: environments, deployment gates, reusable workflows, caching (Curso 4 completo)", 2, "manha"),
                _b("Prometheus Docs + Tutorials — introdução a métricas e PromQL", 2, "tarde"),
            ]},
            "2026-10-12": {"type": "T", "lessons": [
                _p("Podcast 'Software Defined Talk' — observabilidade e métricas"),
            ]},
        },
    },

    24: {
        "label": "S24",
        "focus": "Prometheus/Grafana + Flask DevOps projeto",
        "dates": {
            "2026-10-13": {"type": "F", "lessons": [
                _l("Lab: Prometheus setup — scraping, exporters, alertmanager, PromQL básico", 2, "manha"),
                _l("Lab: Grafana dashboards — métricas do sistema + alertas e notificações", 2, "tarde"),
            ]},
            "2026-10-14": {"type": "T", "lessons": [
                _p("Podcast 'Python Bytes' — Flask e APIs REST"),
            ]},
            "2026-10-15": {"type": "F", "lessons": [
                _a("Flask API DevOps — M1: estrutura do projeto, rotas, SQLAlchemy, migrations", 2, "manha"),
                _a("Flask API DevOps — M2: Docker multi-stage + docker-compose + env vars", 2, "tarde"),
            ]},
            "2026-10-16": {"type": "T", "lessons": [
                _p("Podcast 'Talk Python to Me' — testing em Flask"),
            ]},
            "2026-10-17": {"type": "F", "lessons": [
                _a("Flask API DevOps — M3: testes pytest + coverage + fixtures + mocks", 2, "manha"),
                _a("Flask API DevOps — M4: CI pipeline GitHub Actions — lint, test, build, push", 2, "tarde"),
            ]},
            "2026-10-18": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — deploy de apps no K8s"),
            ]},
            "2026-10-19": {"type": "F", "lessons": [
                _a("Flask API DevOps — M5: deploy Kubernetes — manifests, services, ingress", 2, "manha"),
                _a("Flask API DevOps — M6: Prometheus client Python + métricas customizadas + Grafana", 2, "tarde"),
            ]},
        },
    },

    25: {
        "label": "S25",
        "focus": "Flask DevOps conclusão + Kubernetes fundamentos",
        "dates": {
            "2026-10-20": {"type": "T", "lessons": [
                _p("Podcast 'DevOps and Docker Talk' — K8s e microserviços"),
            ]},
            "2026-10-21": {"type": "F", "lessons": [
                _a("Flask API DevOps — M7: HPA, resource limits, QoS + conclusão Curso 7", 2, "manha"),
                _l("Lab: projeto Flask completo — demo, testes de carga com k6, documentação", 2, "tarde"),
            ]},
            "2026-10-22": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — arquitetura do cluster"),
            ]},
            "2026-10-23": {"type": "F", "lessons": [
                _a("Kubernetes — arquitetura: control plane, nodes, etcd, API server, scheduler", 2, "manha"),
                _f("KillerCoda K8s — scenarios introdutórios interativos", 2, "tarde"),
            ]},
            "2026-10-24": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — pods e deployments"),
            ]},
            "2026-10-25": {"type": "F", "lessons": [
                _l("Lab: kubectl básico — get, describe, logs, exec, port-forward, apply", 2, "manha"),
                _a("Kubernetes — M1-2: pods, deployments, ReplicaSets, rolling updates, rollback", 2, "tarde"),
            ]},
            "2026-10-26": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — services e networking"),
            ]},
        },
    },

    26: {
        "label": "S26",
        "focus": "Kubernetes — Services, ConfigMaps, Volumes, Ingress",
        "dates": {
            "2026-10-27": {"type": "F", "lessons": [
                _l("Lab: deployments — rolling update, rollback, canary deployment manual", 2, "manha"),
                _a("Kubernetes — M3: services (ClusterIP, NodePort, LB), networking, kube-proxy", 2, "tarde"),
            ]},
            "2026-10-28": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — storage e volumes"),
            ]},
            "2026-10-29": {"type": "F", "lessons": [
                _l("Lab: K8s services — ClusterIP interno, NodePort externo, ExternalName", 2, "manha"),
                _a("Kubernetes — M4: ConfigMaps, Secrets, env vars, volume mounts", 2, "tarde"),
            ]},
            "2026-10-30": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — ConfigMaps e Secrets"),
            ]},
            "2026-10-31": {"type": "F", "lessons": [
                _l("Lab: ConfigMaps + Secrets — injetar em pods, rotação de secrets", 2, "manha"),
                _a("Kubernetes — M5: Volumes, PersistentVolumes, PVC, StorageClass, StatefulSets", 2, "tarde"),
            ]},
            "2026-11-01": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — Ingress e TLS"),
            ]},
            "2026-11-02": {"type": "F", "lessons": [
                _l("Lab: PersistentVolumes + StorageClass — deploy MySQL com PVC", 2, "manha"),
                _a("Kubernetes — M6: Ingress, IngressController (nginx), TLS, path-based routing", 2, "tarde"),
            ]},
        },
    },

    27: {
        "label": "S27",
        "focus": "Kubernetes — RBAC, HPA, Helm",
        "dates": {
            "2026-11-03": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — RBAC e segurança"),
            ]},
            "2026-11-04": {"type": "F", "lessons": [
                _l("Lab: Ingress Controller — cert-manager + Let's Encrypt, multiple hosts", 2, "manha"),
                _a("Kubernetes — M7: RBAC, ServiceAccounts, ClusterRoles, RoleBindings", 2, "tarde"),
            ]},
            "2026-11-05": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — Helm e package management"),
            ]},
            "2026-11-06": {"type": "F", "lessons": [
                _l("Lab: RBAC completo — criar ServiceAccount, Role, ClusterRole, Binding", 2, "manha"),
                _a("Kubernetes — M8: HPA, VPA, resource requests/limits, LimitRange, ResourceQuota", 2, "tarde"),
            ]},
            "2026-11-07": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — GitOps com Flux ou ArgoCD"),
            ]},
            "2026-11-08": {"type": "F", "lessons": [
                _l("Lab: HPA scaling — métricas CPU/memória + custom metrics com Prometheus", 2, "manha"),
                _a("Kubernetes — M9: Helm — charts, templates, values, releases, repositórios", 2, "tarde"),
            ]},
            "2026-11-09": {"type": "F", "lessons": [
                _l("Lab: Helm deploy — instalar, atualizar, rollback, criar chart customizado", 2, "manha"),
                _f("KillerCoda K8s — scenarios avançados: networkpolicies, securitycontexts", 2, "tarde"),
            ]},
        },
    },

    28: {
        "label": "S28",
        "focus": "Kubernetes — Monitoring stack + Projeto DevOps",
        "dates": {
            "2026-11-10": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — observabilidade completa"),
            ]},
            "2026-11-11": {"type": "F", "lessons": [
                _a("Kubernetes — M10: Prometheus Operator, ServiceMonitor, PrometheusRule", 2, "manha"),
                _l("Lab: Prometheus stack no K8s — kube-prometheus-stack via Helm", 2, "tarde"),
            ]},
            "2026-11-12": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — projeto DevOps completo"),
            ]},
            "2026-11-13": {"type": "F", "lessons": [
                _l("Lab: Grafana dashboards K8s — USE method, node exporter, pod metrics", 2, "manha"),
                _b("Google SRE Book — SLOs na prática, Error Budgets, burn rate alerts", 2, "tarde"),
            ]},
            "2026-11-14": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — conclusão e próximos passos"),
            ]},
            "2026-11-15": {"type": "F", "lessons": [
                _l("Lab: K8s projeto DevOps parte 1 — Flask app com full stack K8s", 2, "manha"),
                _a("Kubernetes — M11: projeto DevOps K8s parte 1 (pipeline + deploy)", 2, "tarde"),
            ]},
            "2026-11-16": {"type": "T", "lessons": [
                _p("Podcast 'Kubernetes Podcast' — chaos engineering"),
            ]},
        },
    },

    29: {
        "label": "S29",
        "focus": "K8s projeto DevOps conclusão + Chaos Engineering + fechamento Fase 4",
        "dates": {
            "2026-11-17": {"type": "F", "lessons": [
                _l("Lab: K8s projeto DevOps parte 2 — observabilidade + HPA + chaos tests", 2, "manha"),
                _a("Kubernetes — M11: projeto DevOps conclusão + revisão (Curso 8 completo)", 2, "tarde"),
            ]},
            "2026-11-18": {"type": "T", "lessons": [
                _p("Podcast 'On-Call Me Maybe' — chaos engineering no Netflix"),
            ]},
            "2026-11-19": {"type": "F", "lessons": [
                _b("Chaos Engineering — princípios, hipóteses, blast radius, GameDays", 2, "manha"),
                _l("Lab: chaos experiments no K8s — pod failure, network latency, node drain", 2, "tarde"),
            ]},
            "2026-11-20": {"type": "T", "lessons": [
                _p("Podcast 'Software Defined Talk' — SRE sênior skills"),
            ]},
            "2026-11-21": {"type": "F", "lessons": [
                _l("Lab: SLO setup completo — SLIs, SLOs, Error Budget policy, burn rate alerts", 2, "manha"),
                _r("Postmortem: escrita e análise de um incidente real ou simulado", 2, "tarde"),
            ]},
            "2026-11-22": {"type": "T", "lessons": [
                _p("Podcast 'On-Call Me Maybe' — postmortem cultura"),
            ]},
            "2026-11-23": {"type": "F", "lessons": [
                _r("Revisão Fase 4 completa — CI/CD, Kubernetes, Monitoring, Incident Mgmt", 2, "manha"),
                _l("Lab Zabbix: incident simulation completa + postmortem template", 2, "tarde"),
            ]},
        },
    },

    # ════════════════════════════════════════════════════════
    # FASE 5 — Especialização (S30–S36)
    # ════════════════════════════════════════════════════════

    30: {
        "label": "S30",
        "focus": "Capstone — planejamento e infraestrutura",
        "dates": {
            "2026-11-24": {"type": "T", "lessons": [
                _p("Alura Línguas — 20min inglês técnico: leitura de documentação SRE"),
            ]},
            "2026-11-25": {"type": "F", "lessons": [
                _proj("Capstone: planejamento completo — arquitetura, escopo, stack tecnológica", 2, "manha"),
                _proj("Capstone: setup repositório GitHub + CI skeleton + README inicial", 2, "tarde"),
            ]},
            "2026-11-26": {"type": "T", "lessons": [
                _p("Alura Línguas — listening: podcasts SRE em inglês"),
            ]},
            "2026-11-27": {"type": "F", "lessons": [
                _proj("Capstone: infraestrutura Terraform — VPC, EC2, RDS, S3 (IaC completa)", 2, "manha"),
                _proj("Capstone: deploy base Kubernetes — namespaces, RBAC, secrets, configmaps", 2, "tarde"),
            ]},
            "2026-11-28": {"type": "T", "lessons": [
                _p("Alura Línguas — escrita: commit messages e README em inglês"),
            ]},
            "2026-11-29": {"type": "F", "lessons": [
                _proj("Capstone: observabilidade — Prometheus + Grafana + alertas configurados", 2, "manha"),
                _proj("Capstone: SLOs definidos + Error Budget policy + alertmanager", 2, "tarde"),
            ]},
            "2026-11-30": {"type": "T", "lessons": [
                _p("Alura Línguas — listening: SRE talks no YouTube"),
            ]},
        },
    },

    31: {
        "label": "S31",
        "focus": "Capstone — CI/CD, testes, documentação",
        "dates": {
            "2026-12-01": {"type": "F", "lessons": [
                _proj("Capstone: pipeline CI/CD completa — build, test, scan, deploy automático", 2, "manha"),
                _proj("Capstone: testes de carga com k6 + análise de performance e bottlenecks", 2, "tarde"),
            ]},
            "2026-12-02": {"type": "T", "lessons": [
                _p("Alura Línguas — leitura: artigos técnicos SRE em inglês"),
            ]},
            "2026-12-03": {"type": "F", "lessons": [
                _proj("Capstone: refinamento — bugfixes, hardening de segurança, otimização", 2, "manha"),
                _a("Alura Línguas — sessão 30min inglês técnico + revisão documentação SRE", 2, "tarde"),
            ]},
            "2026-12-04": {"type": "T", "lessons": [
                _p("Alura Línguas — listening: conference talks DevOps em inglês"),
            ]},
            "2026-12-05": {"type": "F", "lessons": [
                _proj("Capstone: README profissional — arquitetura, quickstart, screenshots, badges", 2, "manha"),
                _proj("Capstone: demo gravada + apresentação técnica do projeto", 2, "tarde"),
            ]},
            "2026-12-06": {"type": "T", "lessons": [
                _p("Alura Línguas — prática escrita: PR descriptions em inglês"),
            ]},
            "2026-12-07": {"type": "F", "lessons": [
                _r("Revisão capstone completo — checklist de qualidade e entrega", 2, "manha"),
                _l("Lab: troubleshooting scenarios avançados K8s + AWS", 2, "tarde"),
            ]},
        },
    },

    32: {
        "label": "S32",
        "focus": "Preparação de carreira — LinkedIn, portfolio, entrevistas",
        "dates": {
            "2026-12-08": {"type": "T", "lessons": [
                _p("Alura Línguas — listening: entrevistas com SREs seniores"),
            ]},
            "2026-12-09": {"type": "F", "lessons": [
                _r("Preparação carreira: LinkedIn otimizado + GitHub portfolio com todos projetos", 2, "manha"),
                _proj("Blog post: write-up técnico do projeto capstone (publicar Medium/Dev.to)", 2, "tarde"),
            ]},
            "2026-12-10": {"type": "T", "lessons": [
                _p("Alura Línguas — prática speaking: gravar explicação técnica em inglês"),
            ]},
            "2026-12-11": {"type": "F", "lessons": [
                _r("Mock interview: questões SRE técnicas — Linux, K8s, AWS, CI/CD", 2, "manha"),
                _l("Lab: revisão técnica geral — resolver Katas do KillerCoda", 2, "tarde"),
            ]},
            "2026-12-12": {"type": "T", "lessons": [
                _p("Alura Línguas — listening: podcasts carreira em TI em inglês"),
            ]},
            "2026-12-13": {"type": "F", "lessons": [
                _r("Preparação carreira: CV em português e inglês + carta de motivação", 2, "manha"),
                _b("Google SRE Book — capítulos finais: Cascading Failures, Managing Load", 2, "tarde"),
            ]},
            "2026-12-14": {"type": "T", "lessons": [
                _p("Alura Línguas — escrita: email de candidatura em inglês"),
            ]},
        },
    },

    33: {
        "label": "S33",
        "focus": "Mock interviews + revisão técnica avançada",
        "dates": {
            "2026-12-15": {"type": "F", "lessons": [
                _r("Mock interview gravada e analisada — feedback e pontos de melhoria", 2, "manha"),
                _l("Lab: cenários de incidente completos — diagnóstico e remediação", 2, "tarde"),
            ]},
            "2026-12-16": {"type": "T", "lessons": [
                _p("Alura Línguas — revisão vocabulário técnico SRE"),
            ]},
            "2026-12-17": {"type": "F", "lessons": [
                _l("Lab: Kubernetes avançado — NetworkPolicies + OPA Gatekeeper + RBAC audit", 2, "manha"),
                _r("Revisão: Ansible + Terraform — cenários complexos e boas práticas", 2, "tarde"),
            ]},
            "2026-12-18": {"type": "T", "lessons": [
                _p("Alura Línguas — inglês técnico intensivo"),
            ]},
            "2026-12-19": {"type": "F", "lessons": [
                _l("Lab: CI/CD pipeline avançada — GitOps com ArgoCD + rollback automático", 2, "manha"),
                _r("Revisão: GitHub Actions + ArgoCD — pipelines complexas e estratégias de deploy", 2, "tarde"),
            ]},
            "2026-12-20": {"type": "T", "lessons": [
                _p("Alura Línguas — prática escrita final"),
            ]},
            "2026-12-21": {"type": "F", "lessons": [
                _l("Lab: observabilidade completa — traces (OpenTelemetry), metrics, logs (Loki)", 2, "manha"),
                _r("Revisão: Prometheus + Grafana + Loki — stack de observabilidade completa", 2, "tarde"),
            ]},
        },
    },

    34: {
        "label": "S34",
        "focus": "Revisão final técnica + portfolio + carreira",
        "dates": {
            "2026-12-22": {"type": "T", "lessons": [
                _p("Alura Línguas — prática final de inglês técnico"),
            ]},
            "2026-12-23": {"type": "F", "lessons": [
                _r("Revisão técnica final: SRE foundations — Linux, networking, escalabilidade", 2, "manha"),
                _l("Lab: incidente simulado completo — detecção, diagnóstico, remediação, postmortem", 2, "tarde"),
            ]},
            "2026-12-24": {"type": "T", "lessons": [
                _p("Alura Línguas — listening: conferência SRE Summit"),
            ]},
            "2026-12-25": {"type": "F", "lessons": [
                _a("Alura Línguas — sessão speaking: apresentar projetos em inglês (simular entrevista)", 2, "manha"),
                _l("Lab: otimização de performance — profiling, bottlenecks, tuning", 2, "tarde"),
            ]},
            "2026-12-26": {"type": "T", "lessons": [
                _p("Alura Línguas — revisão final inglês"),
            ]},
            "2026-12-27": {"type": "F", "lessons": [
                _r("Portfolio: organização final — README de cada projeto, badges, demos", 2, "manha"),
                _proj("Blog: segundo post técnico — Kubernetes + Observabilidade na prática", 2, "tarde"),
            ]},
            "2026-12-28": {"type": "T", "lessons": [
                _p("Alura Línguas — prática final de escrita técnica"),
            ]},
        },
    },

    35: {
        "label": "S35",
        "focus": "Buffer + revisão + CKA prep planejamento",
        "dates": {
            "2026-12-29": {"type": "F", "lessons": [
                _r("Revisão final: todo o roadmap SRE 2026 — pontos-chave de cada fase", 2, "manha"),
                _l("Lab: demonstração final completa — showcase do capstone ao vivo", 2, "tarde"),
            ]},
            "2026-12-30": {"type": "T", "lessons": [
                _p("Revisão mental — podcast 'On-Call Me Maybe'"),
            ]},
            "2026-12-31": {"type": "F", "lessons": [
                _r("Buffer / tempo livre — reforçar qualquer ponto ainda fraco", 2, "manha"),
                _r("Reflexão: o que aprendi, como cresci, próximos passos em 2027", 2, "tarde"),
            ]},
            "2027-01-01": {"type": "T", "lessons": [
                _p("Natal — revisão mental leve, descanso merecido"),
            ]},
            "2027-01-02": {"type": "F", "lessons": [
                _r("Buffer — estudar tópico de maior interesse ou explorar novidade", 2, "manha"),
                _r("Celebração: revisão da jornada SRE 2026 — do NOC Sênior ao SRE", 2, "tarde"),
            ]},
            "2027-01-03": {"type": "T", "lessons": [
                _p("Revisão mental — próximos objetivos"),
            ]},
            "2027-01-04": {"type": "F", "lessons": [
                _r("CKA prep: material de estudo, plano de estudos Jan/Fev 2027", 2, "manha"),
                _r("Revisão carreira: próximos passos — CKA 2027, vagas SRE, networking", 2, "tarde"),
            ]},
        },
    },

    36: {
        "label": "S36",
        "focus": "Conclusão do programa SRE 2026",
        "dates": {
            "2027-01-05": {"type": "T", "lessons": [
                _p("Revisão mental — balanço final do ano de estudos"),
            ]},
            "2027-01-06": {"type": "F", "lessons": [
                _r("Balanço final: certificações conquistadas, portfolio, métricas do programa", 2, "manha"),
                _l("Lab: setup CKA prep 2027 — ambiente, primeiros simulados, material", 2, "tarde"),
            ]},
            "2027-01-07": {"type": "T", "lessons": [
                _p("Revisão mental — metas 2027"),
            ]},
            "2027-01-08": {"type": "F", "lessons": [
                _r("Celebração final: conclusão do programa SRE 2026 (NOC Sr → SRE)", 2, "manha"),
                _r("Planejamento 2027: CKA, vagas SRE sênior, open source contributions", 2, "tarde"),
            ]},
        },
    },
}


# ── Helpers públicos ──────────────────────────────────────────────────────────
def get_phase_for_week(week_num: int) -> int | None:
    for phase_num, phase_data in PHASES.items():
        if week_num in phase_data["weeks"]:
            return phase_num
    return None


def get_all_lesson_ids() -> list[str]:
    ids = []
    for week_data in WEEKS.values():
        for date, date_data in week_data["dates"].items():
            for idx in range(len(date_data["lessons"])):
                ids.append(f"{date}-{idx}")
    return ids


# ── Labs Zabbix — 30 labs semanais (S05–S34) ─────────────────────────────────
# Mapeamento: semana → (data de inserção, título do lab)
# Seguindo o cronograma_final_sre_robson.md
ZABBIX_LABS = {
    5:  ("2026-06-04", "🧪 LAB ZABBIX #1: Zabbix agent install em VM Ubuntu"),
    6:  ("2026-06-11", "🧪 LAB ZABBIX #2: Custom network monitoring items (interface eth0)"),
    7:  ("2026-06-18", "🧪 LAB ZABBIX #3: Bash external check — health_check.sh integrado"),
    8:  ("2026-06-25", "🧪 LAB ZABBIX #4: Todos os scripts bash no GitHub via commits semânticos"),
    9:  ("2026-07-02", "🧪 LAB ZABBIX #5: Python consome Zabbix API — zabbix_api.py funcional"),
    10: ("2026-07-09", "🧪 LAB ZABBIX #6: Python + Zabbix + SQLite data pipeline"),
    11: ("2026-07-16", "🧪 LAB ZABBIX #7: Python script integração Zabbix API — templates e triggers"),
    12: ("2026-07-23", "🧪 LAB ZABBIX #8: Zabbix integração Python API — criar templates"),
    13: ("2026-07-30", "🧪 LAB ZABBIX #9: AWS EC2 com Zabbix agent via user-data script"),
    14: ("2026-08-06", "🧪 LAB ZABBIX #10: RDS MySQL monitorada via CloudWatch + Zabbix"),
    15: ("2026-08-13", "🧪 LAB ZABBIX #11: Lambda + SNS → Zabbix webhook integration"),
    16: ("2026-08-20", "🧪 LAB ZABBIX #12: Stack completa AWS monitorada end-to-end no Zabbix"),
    17: ("2026-08-27", "🧪 LAB ZABBIX #13: Ansible playbook instala Zabbix agent em 5 VMs"),
    18: ("2026-09-03", "🧪 LAB ZABBIX #14: Ansible gerencia templates Zabbix via API"),
    19: ("2026-09-10", "🧪 LAB ZABBIX #15: Alerta Zabbix → Webhook → AWX Job → remediação"),
    20: ("2026-09-17", "🧪 LAB ZABBIX #16: Flask Docker + Zabbix HTTP agent health check"),
    21: ("2026-09-24", "🧪 LAB ZABBIX #17: Terraform + Ansible + Zabbix integrados (IaC)"),
    22: ("2026-10-01", "🧪 LAB ZABBIX #18: AWX workflow: Zabbix alerta → AWX → remediação auto"),
    23: ("2026-10-08", "🧪 LAB ZABBIX #19: GitHub Actions → Zabbix event API notification"),
    24: ("2026-10-15", "🧪 LAB ZABBIX #20: Deploy validation via Zabbix HTTP agent"),
    25: ("2026-10-22", "🧪 LAB ZABBIX #21: K8s nodes monitorados via kube-state-metrics + Zabbix"),
    26: ("2026-10-29", "🧪 LAB ZABBIX #22: Zabbix on K8s via Helm — self-monitoring cluster"),
    27: ("2026-11-05", "🧪 LAB ZABBIX #23: Zabbix → Prometheus exporter → Grafana dashboard unificado"),
    28: ("2026-11-12", "🧪 LAB ZABBIX #24: Error budget tracking em Zabbix dashboard"),
    29: ("2026-11-19", "🧪 LAB ZABBIX #25: Mock incident — Zabbix alerta, segue runbook, postmortem"),
    30: ("2026-11-26", "🧪 LAB ZABBIX #26: Full automation: Deploy → Monitor → Alert → Remediate"),
    31: ("2026-12-03", "🧪 LAB ZABBIX #27: Zabbix on K8s (capstone) — custom template para aplicação"),
    32: ("2026-12-10", "🧪 LAB ZABBIX #28: Prometheus + Zabbix integração — métricas unificadas"),
    33: ("2026-12-17", "🧪 LAB ZABBIX #29: SLO dashboard Zabbix completo + error budget visualization"),
    34: ("2026-12-24", "🧪 LAB ZABBIX #30: End-to-end automated incident response + postmortem auto"),
}


def _inject_zabbix_labs():
    """Injeta os 30 Labs Zabbix semanais nas semanas correspondentes do WEEKS."""
    for week_num, (date, title) in ZABBIX_LABS.items():
        week_data = WEEKS.get(week_num)
        if not week_data:
            continue
        # Verificar se a data existe na semana
        if date in week_data["dates"]:
            # Adicionar lab ao final das lições do dia
            week_data["dates"][date]["lessons"].append(
                _z(title)
            )
        else:
            # Adicionar a data com o lab (dia não estava no cronograma)
            week_data["dates"][date] = {
                "type": "F" if int(date.split("-")[2]) % 2 != 0 else "T",
                "lessons": [_z(title)],
            }


# Executar injeção ao importar o módulo
_inject_zabbix_labs()
