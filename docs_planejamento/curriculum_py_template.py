# data/curriculum.py — Cronograma Final SRE (36 semanas)
# Robson Santiago | NOC Sênior → SRE | Mai–Dez 2026

"""
Estrutura do currículo:
- 36 semanas (S01–S36)
- 5 fases (Foundation, Core Skills, Cloud & IaC, Advanced SRE, Capstone)
- 12 cursos pagos + 13 gratuitos
- 30 labs Zabbix (1/semana, S02–S31)
- Incident Management em S26–S27
"""

PHASES = [
    {
        "id": 1,
        "name": "Foundation",
        "weeks": list(range(1, 6)),  # S01–S05
        "color": "#FF6B6B",
        "description": "Linux Fundamentals, Networking, Bash Scripting",
        "skills": ["Linux", "Networking", "Bash", "SRE Mindset"]
    },
    {
        "id": 2,
        "name": "Core Skills",
        "weeks": list(range(6, 10)),  # S06–S09
        "color": "#4ECDC4",
        "description": "Git, Python, SQL Databases",
        "skills": ["Git/GitHub", "Python", "SQL", "Flask"]
    },
    {
        "id": 3,
        "name": "Cloud & IaC",
        "weeks": list(range(10, 19)),  # S10–S18
        "color": "#45B7D1",
        "description": "AWS, Terraform, Ansible, AWX, Docker",
        "skills": ["AWS", "Terraform", "Ansible", "IaC", "Docker"]
    },
    {
        "id": 4,
        "name": "Advanced SRE",
        "weeks": list(range(19, 28)),  # S19–S27
        "color": "#FFA07A",
        "description": "CI/CD, Kubernetes, Monitoring, Incident Management",
        "skills": ["GitHub Actions", "Kubernetes", "Prometheus", "Incident Management"]
    },
    {
        "id": 5,
        "name": "Capstone & Carreira",
        "weeks": list(range(28, 37)),  # S28–S36
        "color": "#98D8C8",
        "description": "Projeto Final, Portfolio, Preparação Carreira",
        "skills": ["Production System", "Portfolio", "Career Readiness"]
    }
]

MILESTONES = [
    # Fase 1
    {"id": "s05_phase1", "phase": 1, "week": 5, "title": "Fase 1 Completa: Linux + Networking + Bash", "description": "Foundation sólida"},
    
    # Fase 2
    {"id": "s09_phase2", "phase": 2, "week": 9, "title": "Fase 2 Completa: Git + Python + SQL", "description": "Core skills dominados"},
    
    # Fase 3
    {"id": "s18_phase3", "phase": 3, "week": 18, "title": "Fase 3 Completa: AWS + IaC + Ansible", "description": "Infrastructure as code proficiente"},
    
    # Fase 4
    {"id": "s27_phase4", "phase": 4, "week": 27, "title": "Fase 4 Completa: K8s + Monitoring + Incidents", "description": "Advanced SRE ready"},
    
    # Fase 5
    {"id": "s36_capstone", "phase": 5, "week": 36, "title": "Capstone Concluído", "description": "Projeto production-ready + carreira preparada"},
    
    # Special milestones
    {"id": "aws_certified", "phase": 3, "week": 12, "title": "AWS SAA-C03 Certificado", "description": "Prova agendada/concluída"},
    {"id": "all_labs_done", "phase": 4, "week": 31, "title": "30 Labs Zabbix Completos", "description": "Expertise Zabbix consolidada"},
]

# Semanas com horas disponíveis e lições
WEEKS = {
    1: {
        "phase": 1,
        "title": "SRE Intro & Linux Begin",
        "days_available": 8.5,
        "description": "Semana parcial (começa mai 01). SRE mindset + primeiras lições Linux",
        "lessons": [
            {
                "id": "s01_l01",
                "week": 1,
                "day": "Friday",
                "date": "2026-05-01",
                "title": "SRE DevOps: Jornada — Módulo 1–2",
                "hours": 4,
                "course": "SRE DevOps Jornada",
                "type": "aula",
                "tag": None,
                "block": "manha",
                "url": "https://www.udemy.com/course/jornada-devops-sre-do-inicio-ao-fim/",
                "status": "pending",
                "note": "Intro SRE, SLOs, Toil"
            },
            {
                "id": "s01_l02",
                "week": 1,
                "day": "Sunday",
                "date": "2026-05-03",
                "title": "SRE DevOps: Jornada — Módulo 3–4",
                "hours": 4,
                "course": "SRE DevOps Jornada",
                "type": "aula",
                "tag": None,
                "block": "manha_tarde",
                "url": "https://www.udemy.com/course/jornada-devops-sre-do-inicio-ao-fim/",
                "status": "pending",
                "note": "Error budgets, Automation"
            }
        ]
    },
    
    2: {
        "phase": 1,
        "title": "GNU/Linux Fundamentos + Redes Início",
        "days_available": 14.0,
        "description": "Semana completa. Linux admin basics + rede OSI/TCP-IP",
        "lessons": [
            {
                "id": "s02_l01",
                "week": 2,
                "day": "Tuesday",
                "date": "2026-05-05",
                "title": "GNU/Linux Admin — Módulo 1–2 (Estrutura, CLI, Permissions)",
                "hours": 4,
                "course": "GNU/Linux Admin",
                "type": "aula",
                "tag": None,
                "block": "manha_tarde",
                "url": "https://www.udemy.com/course/adm-so-gnulinux/",
                "status": "pending",
                "note": "File operations, permissions (chmod, chown)"
            },
            {
                "id": "s02_l02",
                "week": 2,
                "day": "Thursday",
                "date": "2026-05-07",
                "title": "GNU/Linux Admin — Módulo 3–4 (Processos, Systemctl)",
                "hours": 4,
                "course": "GNU/Linux Admin",
                "type": "aula",
                "tag": None,
                "block": "manha_tarde",
                "url": "https://www.udemy.com/course/adm-so-gnulinux/",
                "status": "pending",
                "note": "ps, top, kill, systemctl"
            },
            {
                "id": "s02_l03",
                "week": 2,
                "day": "Saturday",
                "date": "2026-05-09",
                "title": "GNU/Linux Admin — Módulo 5–6 (Pacotes, SSH)",
                "hours": 4,
                "course": "GNU/Linux Admin",
                "type": "aula",
                "tag": None,
                "block": "manha_tarde",
                "url": "https://www.udemy.com/course/adm-so-gnulinux/",
                "status": "pending",
                "note": "apt, yum, SSH keys"
            },
            {
                "id": "s02_lab_zabbix_01",
                "week": 2,
                "day": "Wednesday",
                "date": "2026-05-06",
                "title": "🧪 LAB ZABBIX #1: Instalar Agent em VM Ubuntu",
                "hours": 1,
                "course": "Zabbix Lab",
                "type": "lab",
                "tag": "lab",
                "block": "zabbix_weekly",
                "url": None,
                "status": "pending",
                "note": "Zabbix agent install, verify connectivity"
            }
        ]
    },
    
    # ... (semanas 3–36 — truncado para brevidade, mas segue padrão similar)
    # Cada semana tem:
    # - Lições normais (aula, leitura, projeto)
    # - 1 LAB ZABBIX (tipo: "lab", tag: "lab")
    # - Conteúdo gratuito integrado
    
    3: {
        "phase": 1,
        "title": "Networking + Bash Scripting",
        "days_available": 17.5,
        "lessons": [
            {
                "id": "s03_l01",
                "week": 3,
                "day": "Wednesday",
                "date": "2026-05-13",
                "title": "Redes para DevOps — Módulo 1–2 (OSI, TCP/IP)",
                "hours": 4,
                "course": "Redes para DevOps",
                "type": "aula",
                "tag": None,
                "block": "manha_tarde",
                "url": "https://www.udemy.com/course/fundamentos-de-redes-para-devops/",
                "status": "pending",
                "note": "OSI layers, TCP/IP model"
            },
            {
                "id": "s03_lab_zabbix_02",
                "week": 3,
                "day": "Thursday",
                "date": "2026-05-14",
                "title": "🧪 LAB ZABBIX #2: Custom Network Monitoring Items",
                "hours": 1,
                "course": "Zabbix Lab",
                "type": "lab",
                "tag": "lab",
                "block": "zabbix_weekly",
                "url": None,
                "status": "pending",
                "note": "Create custom item for interface monitoring"
            }
        ]
    },
    
    # ... Padrão continua para S04–S36
    # Cada semana segue estrutura similar com cursos pagos + 1 lab Zabbix
}

# Resumo estatístico
STATISTICS = {
    "total_weeks": 36,
    "total_phases": 5,
    "total_courses_paid": 12,
    "total_resources_free": 13,
    "total_zabbix_labs": 30,
    "total_hours_content": 213,
    "total_hours_available": 560,
    "period_start": "2026-05-01",
    "period_end": "2026-12-31",
    "expected_completion": "2026-12-31"
}

def get_week_data(week_num):
    """Retorna dados da semana especificada"""
    return WEEKS.get(week_num, None)

def get_phase_data(phase_id):
    """Retorna dados da fase especificada"""
    return next((p for p in PHASES if p["id"] == phase_id), None)

def get_all_lessons():
    """Retorna todas as lições de todas as semanas"""
    lessons = []
    for week_num, week_data in WEEKS.items():
        lessons.extend(week_data.get("lessons", []))
    return lessons

def get_zabbix_labs():
    """Retorna só os labs Zabbix"""
    return [l for l in get_all_lessons() if l.get("type") == "lab" and l.get("tag") == "lab"]

def get_lessons_by_course(course_name):
    """Retorna lições de um curso específico"""
    return [l for l in get_all_lessons() if l.get("course") == course_name]

# ============================================================================
# NOTA: Este é um TEMPLATE simplificado
# A versão COMPLETA precisa incluir S04–S36 com todas as lições
# Use cronograma_final_sre_robson.md como referência para preencher
# ============================================================================

if __name__ == "__main__":
    # Test
    print(f"Total semanas: {STATISTICS['total_weeks']}")
    print(f"Total fases: {STATISTICS['total_phases']}")
    print(f"Labs Zabbix: {len(get_zabbix_labs())}")
    print(f"Períodos: {STATISTICS['period_start']} → {STATISTICS['period_end']}")
