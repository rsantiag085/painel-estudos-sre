"""
data/curriculum.py — Dados completos do cronograma SRE (31 semanas, 5 fases)
Extraídos de painel_sre_v2.html (const PHASES + const WEEKS)
"""

PHASES = {
    1: {
        "label": "Fase 1 — Foundation",
        "sub": "Linux · Networking · SRE Mindset",
        "weeks": [1, 2, 3, 4],
    },
    2: {
        "label": "Fase 2 — Core Skills",
        "sub": "Git · Python · Databases",
        "weeks": [5, 6, 7, 8],
    },
    3: {
        "label": "Fase 3 — Infra & Cloud",
        "sub": "AWS · Ansible · Terraform · AWX",
        "weeks": [9, 10, 11, 12, 13, 14, 15, 16],
    },
    4: {
        "label": "Fase 4 — Advanced SRE",
        "sub": "CI/CD · Kubernetes · Monitoring · Incident Mgmt",
        "weeks": [17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27],
    },
    5: {
        "label": "Fase 5 — Especialização",
        "sub": "Capstone · Carreira · CKA Prep",
        "weeks": [28, 29, 30, 31],
    },
}

# Milestones por fase (inseridos no banco na inicialização)
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
        "Projeto Flask containerizado e monitorado pelo Zabbix",
    ],
    3: [
        "AWS SAA-C03 certificado (ou com data marcada)",
        "Ansible provisiona ambiente inteiro sem toque manual",
        "AWX executa playbooks via webhook do Zabbix",
        "Terraform cria infra completa em Proxmox e AWS",
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

WEEKS = {
    1: {
        "label": "Semana 1",
        "focus": "SRE Mindset + Linux Core",
        "days": {
            "seg": [
                {"name": "SRE DevOps Jornada — Módulo 1: O que é SRE", "h": 2, "tag": None},
                {"name": "SRE DevOps Jornada — Módulo 2: SLOs e Error Budget", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "SRE DevOps Jornada — Módulo 3: Toil + Automation", "h": 2, "tag": None},
                {"name": "Linux GNU — Módulo 1: Estrutura + comandos básicos", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Linux GNU — Módulo 2: Permissões, usuários, grupos", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Alerta customizado + revisar config", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Linux GNU — Módulo 3: Processos (ps, top, kill, systemctl)", "h": 2, "tag": None},
                {"name": "Linux GNU — Módulo 4: Pacotes (apt/yum) + SSH", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Linux GNU — Módulo 5: Logs (journalctl, rsyslog)", "h": 2, "tag": None},
                {"name": "Revisão + commit GitHub: scripts da semana", "h": 1, "tag": "free"},
            ],
        },
    },
    2: {
        "label": "Semana 2",
        "focus": "Linux Avançado + Networking",
        "days": {
            "seg": [
                {"name": "Linux GNU — Módulo 6: File system, discos, LVM", "h": 2, "tag": None},
                {"name": "Linux GNU — Módulo 7: Rede (ip, ss, netstat)", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Linux GNU — Módulo 8: Segurança, firewall, SELinux", "h": 2, "tag": None},
                {"name": "Linux GNU — Módulo 9: Performance (vmstat, iostat, sar)", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Linux GNU — Módulo 10: Bash scripting básico", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Itens customizados de performance", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Networking: OSI model + TCP/IP (Practical Networking YT)", "h": 2, "tag": "free"},
                {"name": "Networking: DNS deep dive — como funciona de verdade", "h": 2, "tag": "free"},
            ],
            "sex": [
                {"name": "Networking: HTTP/HTTPS + ports + curl + ping + traceroute", "h": 2, "tag": "free"},
                {"name": "Networking: Wireshark básico — captura de tráfego", "h": 2, "tag": "free"},
            ],
        },
    },
    3: {
        "label": "Semana 3",
        "focus": "Linux Performance + Bash Scripting",
        "days": {
            "seg": [
                {"name": "Linux GNU — Revisão módulos 1–5 + exercícios práticos", "h": 2, "tag": None},
                {"name": "Bash: variáveis, condicionais, loops", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Bash: funções, leitura de arquivos, argumentos CLI", "h": 2, "tag": None},
                {"name": "Bash: error handling, exit codes, trap", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Bash: cron jobs — agendamento de tarefas", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Script bash → external check Zabbix", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Linux GNU — Módulo Final: Troubleshooting real-world", "h": 2, "tag": None},
                {"name": "Bash: regex com grep/sed/awk", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Projeto: system_health.sh — monitor de sistema completo", "h": 2, "tag": None},
                {"name": "Revisão geral Linux + commit no GitHub", "h": 1, "tag": "free"},
            ],
        },
    },
    4: {
        "label": "Semana 4",
        "focus": "Consolidação Fase 1 + Google SRE Book",
        "days": {
            "seg": [
                {"name": "Revisão Linux: simulação troubleshooting (quebra VM e conserta)", "h": 2, "tag": None},
                {"name": "Revisão Networking: lab de diagnóstico completo", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Bash: projeto integrador — monitoramento com alertas", "h": 2, "tag": None},
                {"name": "Bash: integração com zabbix_sender", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "OverTheWire Bandit: levels 1–10 (prática gamificada)", "h": 2, "tag": "free"},
                {"name": "LAB ZABBIX: Envio de métricas customizadas via Python sender", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Google SRE Book: cap 1–3 — Introdução ao SRE", "h": 2, "tag": "book"},
                {"name": "Google SRE Book: cap 4–5 — Eliminando Toil", "h": 2, "tag": "book"},
            ],
            "sex": [
                {"name": "Revisão Fase 1 completa + milestone checklist", "h": 2, "tag": None},
                {"name": "Setup Python para próxima fase", "h": 1, "tag": None},
            ],
        },
    },
    5: {
        "label": "Semana 5",
        "focus": "Git + Python Fundamentos",
        "days": {
            "seg": [
                {"name": "Git: init, add, commit, push, pull, clone", "h": 2, "tag": "free"},
                {"name": "Git: branching, merge, rebase", "h": 2, "tag": "free"},
            ],
            "ter": [
                {"name": "Git: GitHub flow, PR, code review básico", "h": 2, "tag": "free"},
                {"name": "Python DevOps — Módulo 1: variáveis, tipos, estruturas", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Python DevOps — Módulo 2: funções, módulos, imports", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Python lista hosts via Zabbix API (JSON-RPC)", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Python DevOps — Módulo 3: leitura/escrita de arquivos", "h": 2, "tag": None},
                {"name": "Python DevOps — Módulo 4: requests library + consumir APIs", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Git: .gitignore, tags, stash, cherry-pick", "h": 2, "tag": "free"},
                {"name": "Revisão + push scripts Python no GitHub", "h": 1, "tag": None},
            ],
        },
    },
    6: {
        "label": "Semana 6",
        "focus": "Python para SRE (foco operacional)",
        "days": {
            "seg": [
                {"name": "Python DevOps — Módulo 5: error handling + logging", "h": 2, "tag": None},
                {"name": "Python DevOps — Módulo 6: regex e parsing de logs", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Python DevOps — Módulo 7: subprocess (executar comandos)", "h": 2, "tag": None},
                {"name": "Python DevOps — Módulo 8: virtual environments + pip", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Python: argparse — scripts com argumentos de linha de comando", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Python cria host via Zabbix API automaticamente", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Python DevOps — Módulo 9: automação com os e shutil", "h": 2, "tag": None},
                {"name": "Python DevOps — Módulo 10: APScheduler (agendamento)", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Python: projeto log_analyzer.py", "h": 2, "tag": None},
                {"name": "Python DevOps — Conclusão + revisão geral", "h": 1, "tag": None},
            ],
        },
    },
    7: {
        "label": "Semana 7",
        "focus": "Python Avançado + Databases",
        "days": {
            "seg": [
                {"name": "Python: classes e OOP básico para SRE", "h": 2, "tag": None},
                {"name": "Python: decorators, context managers", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Python: threading/multiprocessing básico", "h": 2, "tag": None},
                {"name": "Python: pytest — testes unitários", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Databases: SQL básico — SQLBolt tutorial (gratuito)", "h": 2, "tag": "free"},
                {"name": "LAB ZABBIX: Queries direto no banco MySQL do Zabbix", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Databases: PostgreSQL/MySQL admin básico", "h": 2, "tag": None},
                {"name": "Databases: backup e restore automatizado", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Databases: índices, EXPLAIN, performance básica", "h": 2, "tag": None},
                {"name": "Python + SQLite: script que persiste dados de monitoramento", "h": 2, "tag": None},
            ],
        },
    },
    8: {
        "label": "Semana 8",
        "focus": "Projeto Integrador Fase 2",
        "days": {
            "seg": [
                {"name": "Projeto: API Python consulta Zabbix + persiste em SQLite", "h": 2, "tag": None},
                {"name": "Projeto: endpoint /metrics com Flask básico", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Projeto: autenticação básica + logging estruturado", "h": 2, "tag": None},
                {"name": "Projeto: testes com pytest + cobertura", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Projeto: dockerizar aplicação Flask", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Zabbix monitora a API Python (HTTP agent)", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Git: workflow completo do projeto (branches, PR, merge)", "h": 2, "tag": "free"},
                {"name": "Revisão geral Python + Databases", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Milestone Fase 2 review + atualizar painel", "h": 2, "tag": None},
                {"name": "Leitura: Automate Boring Stuff cap 1–5 (gratuito)", "h": 1, "tag": "book"},
            ],
        },
    },
    9: {
        "label": "Semana 9",
        "focus": "AWS Core: IAM, EC2, VPC, S3",
        "days": {
            "seg": [
                {"name": "AWS SAA — IAM: users, roles, policies, MFA", "h": 2, "tag": "aws"},
                {"name": "AWS SAA — EC2: tipos, launch, security groups", "h": 2, "tag": "aws"},
            ],
            "ter": [
                {"name": "AWS SAA — EC2: EBS, snapshots, AMIs", "h": 2, "tag": "aws"},
                {"name": "AWS SAA — VPC: subnets, route tables, internet gateway", "h": 2, "tag": "aws"},
            ],
            "qua": [
                {"name": "AWS SAA — VPC: NAT gateway, security groups vs NACLs", "h": 2, "tag": "aws"},
                {"name": "LAB ZABBIX: EC2 com Zabbix agent via user-data script", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "AWS SAA — S3: buckets, policies, versioning, storage classes", "h": 2, "tag": "aws"},
                {"name": "AWS SAA — S3: lifecycle, replication, encryption", "h": 2, "tag": "aws"},
            ],
            "sex": [
                {"name": "AWS SAA — CLI: configurar + comandos essenciais", "h": 2, "tag": "aws"},
                {"name": "Flashcards: IAM, EC2, VPC, S3 revisão", "h": 1, "tag": None},
            ],
        },
    },
    10: {
        "label": "Semana 10",
        "focus": "AWS Mid-tier: RDS, ELB, Auto Scaling",
        "days": {
            "seg": [
                {"name": "AWS SAA — RDS: MySQL, Multi-AZ, Read Replica", "h": 2, "tag": "aws"},
                {"name": "AWS SAA — ElastiCache: Redis, Memcached", "h": 2, "tag": "aws"},
            ],
            "ter": [
                {"name": "AWS SAA — ELB: ALB, NLB, target groups, health checks", "h": 2, "tag": "aws"},
                {"name": "AWS SAA — Auto Scaling Groups + Launch Templates", "h": 2, "tag": "aws"},
            ],
            "qua": [
                {"name": "AWS SAA — Route53: record types, routing policies", "h": 2, "tag": "aws"},
                {"name": "LAB ZABBIX: Monitorar RDS via CloudWatch + Zabbix bridge", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "AWS SAA — CloudFront: distributions, behaviors, cache", "h": 2, "tag": "aws"},
                {"name": "AWS SAA — SQS/SNS: mensageria básica", "h": 2, "tag": "aws"},
            ],
            "sex": [
                {"name": "AWS SAA — Lambda básico + API Gateway", "h": 2, "tag": "aws"},
                {"name": "Simulado parcial: ELB, ASG, RDS", "h": 1, "tag": None},
            ],
        },
    },
    11: {
        "label": "Semana 11",
        "focus": "AWS Advanced: CloudFormation, Security, Monitoring",
        "days": {
            "seg": [
                {"name": "AWS SAA — CloudWatch: métricas, logs, alarms, dashboards", "h": 2, "tag": "aws"},
                {"name": "AWS SAA — CloudTrail, Config, Trusted Advisor", "h": 2, "tag": "aws"},
            ],
            "ter": [
                {"name": "AWS SAA — CloudFormation: templates, stacks, drift", "h": 2, "tag": "aws"},
                {"name": "AWS SAA — Systems Manager: SSM, Parameter Store", "h": 2, "tag": "aws"},
            ],
            "qua": [
                {"name": "AWS SAA — KMS, Secrets Manager, Shield, WAF", "h": 2, "tag": "aws"},
                {"name": "LAB ZABBIX: Lambda dispara alerta Zabbix via SNS webhook", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "AWS SAA — ECS basics + Cost Explorer + Budgets", "h": 2, "tag": "aws"},
                {"name": "AWS SAA — Well-Architected Framework (5 pillars)", "h": 2, "tag": "aws"},
            ],
            "sex": [
                {"name": "Simulado parcial SAA-C03 completo", "h": 2, "tag": None},
                {"name": "Revisão tópicos fracos do simulado", "h": 2, "tag": None},
            ],
        },
    },
    12: {
        "label": "Semana 12",
        "focus": "AWS Simulados + Agendamento da Prova",
        "days": {
            "seg": [
                {"name": "Simulado SAA-C03 (65 questões)", "h": 2, "tag": "aws"},
                {"name": "Revisão tópicos fracos — VPC deep dive", "h": 2, "tag": "aws"},
            ],
            "ter": [
                {"name": "Revisão: HA/DR strategies — Multi-AZ, Multi-Region", "h": 2, "tag": "aws"},
                {"name": "Simulado 2 — foco arquitetura e boas práticas", "h": 2, "tag": "aws"},
            ],
            "qua": [
                {"name": "Revisão: Security + especialidades SAA", "h": 2, "tag": "aws"},
                {"name": "LAB ZABBIX: Arquitetura completa EC2+RDS+S3 monitorada", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Simulado 3 + análise detalhada de erros", "h": 2, "tag": "aws"},
                {"name": "Agendar prova SAA-C03 (Pearson ou PSI)", "h": 1, "tag": "aws"},
            ],
            "sex": [
                {"name": "Revisão final AWS + Alura Línguas (inglês técnico)", "h": 2, "tag": None},
                {"name": "Milestone AWS: decidir data e confirmar agendamento", "h": 1, "tag": "aws"},
            ],
        },
    },
    13: {
        "label": "Semana 13",
        "focus": "Ansible Fundamentos",
        "days": {
            "seg": [
                {"name": "Ansible — Conceitos: agentless, SSH, inventories", "h": 2, "tag": None},
                {"name": "Ansible — Ad-hoc commands: ping, command, shell, copy", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Ansible — Playbooks: estrutura YAML, tasks, handlers", "h": 2, "tag": None},
                {"name": "Ansible — Variáveis: vars, defaults, group_vars, host_vars", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Ansible — Módulos: apt, yum, service, file, template", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Ansible instala Zabbix agent em 5 VMs de uma vez", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Ansible — Conditionals, loops, register, set_fact", "h": 2, "tag": None},
                {"name": "Ansible — Templates Jinja2: configurações dinâmicas", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Ansible — Tags, notificações, verbosity, debug", "h": 2, "tag": None},
                {"name": "Projeto: playbook que provisiona ambiente completo do zero", "h": 2, "tag": None},
            ],
        },
    },
    14: {
        "label": "Semana 14",
        "focus": "Ansible Roles + Vault + AWX",
        "days": {
            "seg": [
                {"name": "Ansible — Roles: estrutura, defaults, tasks, handlers", "h": 2, "tag": None},
                {"name": "Ansible — Galaxy: baixar e usar roles da comunidade", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Ansible — Vault: criptografar secrets com segurança", "h": 2, "tag": None},
                {"name": "Ansible — Dynamic inventory + error handling (block/rescue)", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Ansible — Performance: pipelining, forks, async tasks", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Ansible gerencia templates Zabbix via API", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Ansible — Projeto: role completa para Zabbix server", "h": 2, "tag": None},
                {"name": "AWX — Instalação, conceitos, organizações, inventários", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "AWX — Job templates, workflows, schedules", "h": 2, "tag": None},
                {"name": "AWX — Webhooks + RBAC + notificações", "h": 2, "tag": None},
            ],
        },
    },
    15: {
        "label": "Semana 15",
        "focus": "AWX Avançado + Terraform",
        "days": {
            "seg": [
                {"name": "AWX — Credenciais, projetos, surveys interativos", "h": 2, "tag": None},
                {"name": "AWX — API REST: chamar jobs programaticamente", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Terraform Essentials — Sintaxe HCL, providers, resources", "h": 2, "tag": None},
                {"name": "Terraform Essentials — Variables, outputs, locals", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Terraform Essentials — State management, import, workspace", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Alerta Zabbix → Webhook AWX → Playbook remedia", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Terraform Essentials — Módulos, remote state (S3 backend)", "h": 2, "tag": None},
                {"name": "Terraform Essentials — Boas práticas + revisão", "h": 1, "tag": None},
            ],
            "sex": [
                {"name": "Lab integrador: Terraform provisiona VMs + Ansible configura tudo", "h": 2, "tag": None},
                {"name": "Documentar projeto IaC no GitHub", "h": 2, "tag": None},
            ],
        },
    },
    16: {
        "label": "Semana 16",
        "focus": "Consolidação Fase 3 + Milestone",
        "days": {
            "seg": [
                {"name": "Lab integrador: Terraform EC2 + Ansible configura + Zabbix monitora", "h": 2, "tag": None},
                {"name": "Revisão Ansible: roles, vault, AWX workflows", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Revisão Terraform: boas práticas + state remoto", "h": 2, "tag": None},
                {"name": "Leitura: Google SRE Book — 'Eliminating Toil' (cap gratuito)", "h": 2, "tag": "book"},
            ],
            "qua": [
                {"name": "Projeto: IaC repo organizado — README + diagrama de arquitetura", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Automação completa alerta → remediação → notificação", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Revisão Fase 3 completa — o que sei, o que preciso aprofundar", "h": 2, "tag": None},
                {"name": "Milestone checklist Fase 3", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Planejamento Fase 4 + Alura Línguas: vocabulário DevOps/SRE", "h": 2, "tag": None},
                {"name": "Update painel de progresso + commit GitHub", "h": 1, "tag": None},
            ],
        },
    },
    17: {
        "label": "Semana 17",
        "focus": "GitHub Actions — Parte 1",
        "days": {
            "seg": [
                {"name": "GitHub Actions — Workflows, events, triggers", "h": 2, "tag": None},
                {"name": "GitHub Actions — Jobs, steps, runners (ubuntu/self-hosted)", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "GitHub Actions — Secrets, contexts, environment variables", "h": 2, "tag": None},
                {"name": "GitHub Actions — Docker build + push para DockerHub", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "GitHub Actions — Matrix builds, artifacts, cache", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Action notifica Zabbix de deploy via API", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "GitHub Actions — Deployment environments + approvals", "h": 2, "tag": None},
                {"name": "GitHub Actions — Reusable workflows + composite actions", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "GitHub Actions — Conclusão do curso", "h": 1, "tag": None},
                {"name": "Lab: pipeline test → build → push para API Python", "h": 2, "tag": None},
            ],
        },
    },
    18: {
        "label": "Semana 18",
        "focus": "CI/CD Estratégias + Pipeline Completo",
        "days": {
            "seg": [
                {"name": "CI/CD conceitos: blue/green, canary, rolling updates, feature flags", "h": 2, "tag": None},
                {"name": "Pipeline: deploy em EC2 após testes passarem (staging → prod)", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Pipeline: rollback automático + health checks pós-deploy", "h": 2, "tag": None},
                {"name": "Estratégia: deployment slots, traffic splitting", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Lab: pipeline zero-downtime para Flask API em K8s", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Zabbix valida health da aplicação após cada deploy", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Leitura: 'Continuous Delivery' — conceitos chave (artigos gratuitos)", "h": 2, "tag": "book"},
                {"name": "Documentar runbook de deploy: passo a passo + rollback", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Revisão CI/CD completo + commit pipelines no GitHub", "h": 2, "tag": None},
                {"name": "Alura Línguas: leitura técnica em inglês", "h": 1, "tag": None},
            ],
        },
    },
    19: {
        "label": "Semana 19",
        "focus": "Kubernetes Core: Pods, Deployments, Services",
        "days": {
            "seg": [
                {"name": "K8s — Arquitetura: control plane, nodes, etcd, kubelet", "h": 2, "tag": None},
                {"name": "K8s — kubectl: comandos essenciais, contextos, namespaces", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "K8s — Pods: lifecycle, restart policies, multi-container", "h": 2, "tag": None},
                {"name": "K8s — Deployments: replicas, rolling update, rollback", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "K8s — Services: ClusterIP, NodePort, LoadBalancer, ExternalName", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Monitorar K8s nodes via kube-state-metrics", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "K8s — ConfigMaps e Secrets: como usar corretamente", "h": 2, "tag": None},
                {"name": "K8s — Volumes: emptyDir, hostPath, PVC, PV", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Lab: deploy Flask API em minikube (Proxmox home lab)", "h": 2, "tag": None},
                {"name": "Revisão + diagrama arquitetura K8s", "h": 1, "tag": None},
            ],
        },
    },
    20: {
        "label": "Semana 20",
        "focus": "Kubernetes Avançado: StatefulSets, Ingress, RBAC",
        "days": {
            "seg": [
                {"name": "K8s — StatefulSets: bancos de dados, ordenação de pods", "h": 2, "tag": None},
                {"name": "K8s — DaemonSets, Jobs, CronJobs", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "K8s — Ingress + Nginx Ingress Controller", "h": 2, "tag": None},
                {"name": "K8s — Network Policies: segmentação de tráfego", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "K8s — RBAC: service accounts, roles, clusterroles, bindings", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Custom exporter K8s → envia métricas para Zabbix", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "K8s — Liveness, Readiness e Startup probes", "h": 2, "tag": None},
                {"name": "K8s — Resource requests, limits, QoS classes", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "K8s — HPA: Horizontal Pod Autoscaler baseado em CPU/métricas", "h": 2, "tag": None},
                {"name": "Lab: auto-scaling baseado em carga real", "h": 2, "tag": None},
            ],
        },
    },
    21: {
        "label": "Semana 21",
        "focus": "Kubernetes Helm + Observabilidade no Cluster",
        "days": {
            "seg": [
                {"name": "Helm — Charts, repos, values, upgrade, rollback", "h": 2, "tag": None},
                {"name": "Helm — Deploy Zabbix no K8s via Helm chart oficial", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "K8s Monitoring — Prometheus + Grafana via Helm (kube-prometheus-stack)", "h": 2, "tag": None},
                {"name": "K8s Monitoring — ServiceMonitor, PrometheusRule, alertas", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "K8s Logging — Loki + Promtail para logs do cluster", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Zabbix + Prometheus side-by-side — diferenças práticas", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "K8s Tools — k9s, Kubernetes Dashboard, Lens", "h": 2, "tag": None},
                {"name": "K8s Troubleshooting: CrashLoopBackOff, OOMKilled, Pending", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Lab: stack observabilidade completa no cluster (Prom + Grafana + Loki)", "h": 2, "tag": None},
                {"name": "Documentar runbooks de troubleshooting K8s", "h": 2, "tag": None},
            ],
        },
    },
    22: {
        "label": "Semana 22",
        "focus": "K8s + GitOps + CI/CD Integrado",
        "days": {
            "seg": [
                {"name": "K8s — Curso: Seções finais + Projeto DevOps integrado", "h": 2, "tag": None},
                {"name": "Pipeline: GitHub Actions → build → push → deploy em K8s", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "GitOps: conceito + ArgoCD básico — sync automático", "h": 2, "tag": "free"},
                {"name": "K8s — Multi-environment: dev/staging/prod com namespaces", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "K8s — Storage: StorageClass, dynamic provisioning", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Alertas Zabbix baseados em métricas K8s coletadas", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "K8s — Security: PodSecurityAdmission, NetworkPolicies", "h": 2, "tag": None},
                {"name": "K8s — Upgrade de cluster + manutenção de nodes", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Revisão K8s completo + lista de gaps", "h": 2, "tag": None},
                {"name": "Lab integrador: deploy completo via pipeline + validação automática", "h": 2, "tag": None},
            ],
        },
    },
    23: {
        "label": "Semana 23",
        "focus": "Projeto DevOps Flask API (semana dedicada)",
        "days": {
            "seg": [
                {"name": "Flask API — Estrutura do projeto, rotas, Dockerfile", "h": 2, "tag": None},
                {"name": "Flask API — Testes unitários + cobertura com pytest", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Flask API — Pipeline CI: lint → test → build → push", "h": 2, "tag": None},
                {"name": "Flask API — Deploy em K8s: manifests, service, ingress", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Flask API — Observabilidade: métricas Prometheus nativas", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Flask expõe métricas → Zabbix HTTP agent consome", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Flask API — Escalabilidade: HPA + load test com k6", "h": 2, "tag": None},
                {"name": "Flask API — Disaster recovery: failover e rollback documentado", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Flask API — Documentação completa: README + diagrama + runbooks", "h": 2, "tag": None},
                {"name": "Demo: apresente o projeto como se fosse entrevista (grave vídeo)", "h": 2, "tag": None},
            ],
        },
    },
    24: {
        "label": "Semana 24",
        "focus": "Monitoring & Observability Avançado",
        "days": {
            "seg": [
                {"name": "Prometheus — Conceitos, PromQL básico, exporters", "h": 2, "tag": "free"},
                {"name": "Prometheus — Alertmanager: regras, silences, routing", "h": 2, "tag": "free"},
            ],
            "ter": [
                {"name": "Grafana — Dashboards, data sources, variáveis, anotações", "h": 2, "tag": "free"},
                {"name": "Grafana — Alertas, notificações, on-call routing", "h": 2, "tag": "free"},
            ],
            "qua": [
                {"name": "ELK/Loki: Elasticsearch + Kibana ou Loki — logs centralizados", "h": 2, "tag": "free"},
                {"name": "LAB ZABBIX: Exportar métricas Zabbix → Grafana (unified view)", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Distributed tracing: Jaeger básico — traces end-to-end", "h": 2, "tag": "free"},
                {"name": "SLIs e SLOs: definir para projeto Flask — availability + latency", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Error budget: calcular, visualizar e comunicar para stakeholders", "h": 2, "tag": None},
                {"name": "Revisão pilares observabilidade: métricas + logs + traces", "h": 2, "tag": None},
            ],
        },
    },
    25: {
        "label": "Semana 25",
        "focus": "SRE Book + Chaos Engineering",
        "days": {
            "seg": [
                {"name": "Google SRE Book — 'Monitoring Distributed Systems' (gratuito)", "h": 2, "tag": "book"},
                {"name": "Alerting filosofia: alertas acionáveis vs ruído", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Chaos Engineering: conceitos + Chaos Monkey + Gremlin", "h": 2, "tag": "free"},
                {"name": "Lab: simular falha de node K8s e medir MTTR", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Capacity planning: métricas de crescimento + projeção", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Dashboard unificado Zabbix + Grafana para gestão", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Google SRE Book — Parte I completa (caps gratuitos online)", "h": 2, "tag": "book"},
                {"name": "Resumo e anotações: o que aprendi de observabilidade", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Revisão Fase 4 parcial (semanas 17–25)", "h": 2, "tag": None},
                {"name": "Alura Línguas: reading comprehension técnico", "h": 1, "tag": None},
            ],
        },
    },
    26: {
        "label": "Semana 26",
        "focus": "Incident Management + Runbooks",
        "days": {
            "seg": [
                {"name": "Incident response: roles (commander, scribe, comms), processo", "h": 2, "tag": None},
                {"name": "Runbooks: estrutura, boas práticas, manutenção contínua", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Blameless postmortem: template + exemplo real do seu trabalho", "h": 2, "tag": None},
                {"name": "On-call: best practices, rotação, escalonamento, burnout", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "PagerDuty/OpsGenie: conceitos (docs oficiais gratuitos)", "h": 2, "tag": "free"},
                {"name": "LAB ZABBIX: Action automático → ticket simulado (webhook + script)", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Lab: mock incident drill — quebra propositalmente, resolve, documenta", "h": 2, "tag": None},
                {"name": "Postmortem do incident drill: escrever o documento completo", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Escalation procedures + comunicação com stakeholders não-técnicos", "h": 2, "tag": None},
                {"name": "Google SRE Book — capítulo Incident Response (gratuito)", "h": 2, "tag": "book"},
            ],
        },
    },
    27: {
        "label": "Semana 27",
        "focus": "Consolidação Fase 4 + Portfolio",
        "days": {
            "seg": [
                {"name": "Revisão completa Fase 4 (17–26)", "h": 2, "tag": None},
                {"name": "Lab: pipeline completo com alertas + auto-remediação", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Simulação: 'dia completo como SRE' — incidents, deploys, monit", "h": 2, "tag": None},
                {"name": "Documentar todos os runbooks do projeto capstone", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "GitHub: organizar portfolio — README profissional em cada repo", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Revisão final — integração completa Zabbix no ecossistema", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Milestone Fase 4: checklist completo", "h": 2, "tag": None},
                {"name": "Planejamento Fase 5 — capstone e carreira", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Revisão 8 meses: o que aprendi, o que ainda falta", "h": 2, "tag": None},
                {"name": "Atualizar painel + exportar progresso completo", "h": 1, "tag": None},
            ],
        },
    },
    28: {
        "label": "Semana 28",
        "focus": "Capstone Parte 1: Infraestrutura",
        "days": {
            "seg": [
                {"name": "Capstone: diagrama de arquitetura + decisões técnicas documentadas", "h": 2, "tag": None},
                {"name": "Capstone: Terraform — infraestrutura base (VPC, EC2/EKS, RDS)", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Capstone: Ansible — configuração de servidores + roles", "h": 2, "tag": None},
                {"name": "Capstone: K8s manifests — namespace, deployment, service, ingress", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Capstone: Flask API com métricas Prometheus nativas", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Capstone integra Zabbix como monitoring primário", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Capstone: GitHub Actions pipeline completo end-to-end", "h": 2, "tag": None},
                {"name": "Capstone: deploy em produção — smoke tests pós-deploy", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Capstone: Prometheus + Grafana + dashboards SLO", "h": 2, "tag": None},
                {"name": "Capstone: SLOs definidos com alertas e error budget dashboard", "h": 2, "tag": None},
            ],
        },
    },
    29: {
        "label": "Semana 29",
        "focus": "Capstone Parte 2: Observabilidade + Demo",
        "days": {
            "seg": [
                {"name": "Capstone: testes de carga com k6 + análise de resultados", "h": 2, "tag": None},
                {"name": "Capstone: chaos engineering — simular falhas e medir resiliência", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Capstone: documentação completa — README + arquitetura + runbooks", "h": 2, "tag": None},
                {"name": "Capstone: revisão final técnica — o que mudaria com mais tempo?", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Capstone: mock incident + postmortem documentado", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Validação final — Zabbix no ambiente de produção", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Publicar no GitHub com README profissional + badges CI/CD", "h": 2, "tag": None},
                {"name": "Escrever blog post sobre o projeto (dev.to ou LinkedIn)", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Demo gravada: apresente como faria em entrevista (10 min)", "h": 2, "tag": None},
                {"name": "Revisão completa 8 meses — retrospectiva de aprendizado", "h": 2, "tag": None},
            ],
        },
    },
    30: {
        "label": "Semana 30",
        "focus": "Preparação de Carreira",
        "days": {
            "seg": [
                {"name": "Certificações próximas: CKA (K8s Admin) — plano de estudo", "h": 2, "tag": None},
                {"name": "Soft skills: escrita técnica — RCA, runbooks, proposta de projeto", "h": 2, "tag": None},
            ],
            "ter": [
                {"name": "Soft skills: como apresentar postmortems para liderança", "h": 2, "tag": None},
                {"name": "LinkedIn: perfil SRE — keywords, projetos, certificações", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Resume: destacar automação, SRE mindset, Zabbix expertise, AWS", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Último lab exploratório — algo novo e desafiador", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Entrevista prep: system design SRE — disponibilidade, escalabilidade", "h": 2, "tag": None},
                {"name": "Entrevista prep: troubleshooting SRE — root cause analysis ao vivo", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "Entrevista prep: falar sobre SLOs, Error Budget, Toil com exemplos reais", "h": 2, "tag": None},
                {"name": "Mock interview gravada: 30 min + análise de pontos fracos", "h": 2, "tag": None},
            ],
        },
    },
    31: {
        "label": "Semana 31",
        "focus": "Finalização + Próximos 6 Meses",
        "days": {
            "seg": [
                {"name": "Recursos futuros: CNCF, SREcon (YouTube), Google SRE Book II", "h": 2, "tag": "book"},
                {"name": "Comunidade: r/sre, CNCF Slack, SRE Weekly newsletter", "h": 2, "tag": "free"},
            ],
            "ter": [
                {"name": "Planejamento pós-cronograma: CKA (mês 9–10), Terraform Associate", "h": 2, "tag": None},
                {"name": "Retrospectiva: o que mudaria no cronograma? O que foi mais difícil?", "h": 2, "tag": None},
            ],
            "qua": [
                {"name": "Revisão: o que cada fase ensinou — documento final de learnings", "h": 2, "tag": None},
                {"name": "LAB ZABBIX: Lab especial — algo que sempre quis fazer mas adiou", "h": 1, "tag": "lab"},
            ],
            "qui": [
                {"name": "Posição SRE: busca ativa — JDs, keywords, onde olhar (LinkedIn, CNCF)", "h": 2, "tag": None},
                {"name": "Celebrar: 8 meses de esforço consistente com 12x36!", "h": 2, "tag": None},
            ],
            "sex": [
                {"name": "🎉 FORMAÇÃO SRE CONCLUÍDA — Você é SRE Engineer", "h": 2, "tag": None},
                {"name": "Próximo capítulo começa. Bora! 🚀", "h": 1, "tag": None},
            ],
        },
    },
}


def get_phase_for_week(week_num: int) -> int:
    """Retorna o número da fase para uma semana."""
    for phase_num, phase in PHASES.items():
        if week_num in phase["weeks"]:
            return phase_num
    return 0


def get_all_lesson_ids() -> list[str]:
    """Retorna todos os IDs de lição no formato 'wN-dia-index'."""
    days_order = ["seg", "ter", "qua", "qui", "sex"]
    ids = []
    for week_num, week_data in WEEKS.items():
        for day in days_order:
            lessons = week_data["days"].get(day, [])
            for i in range(len(lessons)):
                ids.append(f"w{week_num}-{day}-{i}")
    return ids


def get_lesson_by_id(lesson_id: str):
    """Retorna os dados de uma lição a partir do seu ID."""
    parts = lesson_id.split("-")
    if len(parts) < 3:
        return None
    week_num = int(parts[0][1:])
    day = parts[1]
    idx = int(parts[2])
    week_data = WEEKS.get(week_num)
    if not week_data:
        return None
    lessons = week_data["days"].get(day, [])
    if idx >= len(lessons):
        return None
    return lessons[idx]
