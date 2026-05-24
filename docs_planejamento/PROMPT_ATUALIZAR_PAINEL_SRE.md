# PROMPT: Atualizar Painel SRE com Novo Cronograma (36 semanas)

## 📋 CONTEXTO

Robson Santiago está atualizando seu cronograma de estudos SRE de **31 semanas (antigo)** para **36 semanas (novo — mai–dez 2026)**.

O repositório `painel-estudos-sre` é uma aplicação web (FastAPI + SQLite + HTML/JS) que rastreia progresso de estudos.

**Você precisa:**
1. Atualizar dados do currículo (36 semanas, 5 fases, 12 cursos + 13 gratuitos)
2. Integrar 30 labs Zabbix (1/semana)
3. Adicionar Incident Management em Fase 4
4. Manter toda a funcionalidade existente (dashboard, stats, export)
5. Atualizar README com novas informações

---

## 🎯 TAREFAS ESPECÍFICAS

### TAREFA 1: Atualizar `data/curriculum.py`

**O que mudar:**
- Aumentar de 31 para 36 semanas
- Adicionar 5 semanas de Capstone (Fase 5)
- Integrar os 12 cursos finais (Redes, SQL, Prometheus, etc)
- Adicionar 30 labs Zabbix (1 por semana, começando S02)
- Adicionar Incident Management (S26–S27, gratuito)

**Estrutura esperada:**
```python
# data/curriculum.py

CURRICULUM = {
    "phases": [
        {
            "id": 1,
            "name": "Foundation",
            "weeks": [1, 2, 3, 4, 5],
            "color": "#FF6B6B",
            "description": "Linux, Networking, Bash"
        },
        # ... fases 2–5
    ],
    
    "weeks": {
        1: {
            "phase": 1,
            "title": "SRE Intro & Linux Begin",
            "days_available": 8.5,  # S01 é parcial
            "lessons": [
                {
                    "id": "s01_sre_devops_01",
                    "week": 1,
                    "day": "Friday",
                    "title": "SRE DevOps: Jornada — Módulo 1–2",
                    "hours": 4,
                    "course": "SRE DevOps Jornada",
                    "type": "aula",
                    "tag": None,
                    "block": "manha",
                    "url": "https://www.udemy.com/course/...",
                    "status": "pending",
                    "note": ""
                },
                # ... mais aulas
                {
                    "id": "s02_zabbix_lab_01",
                    "week": 2,
                    "day": "Wednesday",
                    "title": "LAB ZABBIX #1: Install Agent",
                    "hours": 1,
                    "course": "Zabbix Lab",
                    "type": "lab",
                    "tag": "lab",
                    "block": "zabbix_weekly",
                    "url": None,
                    "status": "pending",
                    "note": "Instalar Zabbix agent em VM Ubuntu"
                }
            ]
        },
        # ... semanas 2–36
    },
    
    "milestones": [
        # Milestones por fase
        {
            "id": "phase1_complete",
            "phase": 1,
            "title": "Fase 1: Foundation Completa",
            "description": "Linux, Networking, Bash fluentes",
            "week_target": 5,
            "status": "pending"
        },
        # ... mais milestones
    ]
}
```

**Dados a usar:**
- Use `cronograma_final_sre_robson.md` para mapear semana-a-semana
- Cursos: 12 pagos (conforme listado no cronograma)
- Gratuitos: 13 recursos (Google SRE Book, YouTube, docs, etc)
- Labs Zabbix: S02–S31 (30 total)
  - S01: skip (semana parcial)
  - S02: "Zabbix agent install"
  - S03: "Custom network items"
  - ... continua até S31

---

### TAREFA 2: Atualizar `models.py`

**O que mudar:**
- Adicionar campo `week_num` à tabela `LessonProgress` (se não existir)
- Adicionar campo `lab_type` (para distinguir "aula", "lab", "leitura", "projeto")
- Adicionar campo `course_url` (URL do curso — novo)

**Nova migração (pseudo-SQL):**
```python
# models.py

class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    
    id = Column(Integer, primary_key=True)
    lesson_id = Column(String, unique=True, index=True)
    week_num = Column(Integer)  # NOVO: que semana (1–36)
    status = Column(String, default="pending")  # pending, done, skipped
    note = Column(String, nullable=True)
    lab_type = Column(String, nullable=True)  # "aula", "lab", "leitura", "projeto"
    course_url = Column(String, nullable=True)  # URL do curso (NOVO)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

---

### TAREFA 3: Atualizar `routers/progress.py`

**O que mudar:**
- Manter CRUD existente (GET, POST por lesson_id)
- Adicionar filtro por `week_num` (para próximas semanas)
- Adicionar filtro por `lab_type` (mostrar só labs, só aulas, etc)
- Adicionar endpoint para "próximas 3 lições não iniciadas"

**Novos endpoints (se quiser):**
```python
# Exemplo de novo endpoint útil

GET /api/progress/week/{week_num}
  → Retorna todas as lições de uma semana específica

GET /api/progress/labs
  → Retorna só os labs Zabbix

GET /api/progress/next
  → Retorna próximas 3 lições não iniciadas (útil para dashboard)
```

---

### TAREFA 4: Atualizar `routers/stats.py`

**O que mudar:**
- Estatísticas por fase (mantém)
- Adicionar: "% de labs Zabbix concluídos" (novo)
- Adicionar: "% de progresso por tipo" (aula vs lab vs leitura)
- Adicionar: "Dias até conclusão esperada" (35 semanas = 245 dias)

**Novos KPIs:**
```python
{
    "total_lessons": 450,  # aumentou de 180
    "total_labs_zabbix": 30,
    "labs_completed": 5,
    "labs_percentage": 16.7,
    "expected_completion": "2026-12-31",
    "days_remaining": 220,
    "weeks_remaining": 31,
    "completion_rate": 42.3,
    "by_type": {
        "aula": 45,
        "lab": 30,
        "leitura": 20,
        "projeto": 10
    }
}
```

---

### TAREFA 5: Atualizar `static/app.js`

**O que mudar:**
- Aumentar visualização para 36 semanas (não mais 31)
- Adicionar badge "🧪 LAB ZABBIX" em lições do tipo "lab"
- Adicionar indicador "✅ S01–S36" (progresso por semana)
- Adicionar botão "Ver próxima semana" / "Ver semana anterior"

**Novos elementos visuais:**
```javascript
// Exemplo: renderizar badge de lab Zabbix

if (lesson.lab_type === "lab" && lesson.course === "Zabbix Lab") {
    badgeHTML = `<span class="badge badge-zabbix">🧪 ZABBIX LAB</span>`;
}

// Exemplo: renderizar semana

function renderWeekSummary(weekNum) {
    const week = curriculum.weeks[weekNum];
    return `
        <div class="week-summary">
            <h3>Semana ${weekNum}: ${week.title}</h3>
            <p class="available-hours">⏱️ ${week.days_available}h disponíveis</p>
            <div class="lesson-list">
                ${week.lessons.map(lesson => renderLesson(lesson)).join('')}
            </div>
        </div>
    `;
}
```

---

### TAREFA 6: Atualizar `static/style.css`

**O que mudar:**
- Adicionar estilos para badge `.badge-zabbix` (cor especial para labs)
- Adicionar estilos para semanas numeradas (S01–S36)
- Melhorar contraste dark terminal (mantém estética atual)

**Novos estilos:**
```css
.badge-zabbix {
    background-color: #FF9F1C;  /* Laranja Zabbix */
    color: #fff;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8em;
    margin-left: 8px;
}

.week-label {
    font-weight: bold;
    color: #00D9FF;  /* Cyan para semanas */
    font-family: 'JetBrains Mono', monospace;
}

.lab-lesson {
    border-left: 4px solid #FF9F1C;  /* Indicador visual de lab */
}
```

---

### TAREFA 7: Atualizar `templates/index.html`

**O que mudar:**
- Aumentar timeline de 31 para 36 semanas
- Adicionar seção "Próximos 30 Labs Zabbix" na sidebar
- Adicionar calendário com escala 12x36 integrada
- Manter dark terminal theme (atual)

**Nova seção (exemplo):**
```html
<section class="zabbix-labs">
    <h3>🧪 Labs Zabbix (30 total)</h3>
    <div class="lab-progress">
        <div class="progress-bar">
            <div class="progress-fill" style="width: 20%;"></div>
        </div>
        <p>6/30 concluídos (20%)</p>
    </div>
    <ul class="lab-list">
        <li>✅ S02: Install agent</li>
        <li>⏳ S03: Network items</li>
        <li>○ S04: Bash integration</li>
        <!-- ... mais labs -->
    </ul>
</section>
```

---

### TAREFA 8: Atualizar `README.md`

**O que mudar:**
- Mudar de "31 semanas" para "36 semanas"
- Atualizar "Fases do Cronograma" (adicionar Fase 5)
- Adicionar seção "Labs Zabbix"
- Adicionar seção "Cursos Pagos vs Gratuitos"
- Atualizar período: "Maio–Dezembro 2026"

**Novo conteúdo do README:**
```markdown
# SRE Tracker — Robson Santiago

Sistema de acompanhamento de estudos SRE com **36 semanas**, **5 fases** e ~213h de conteúdo.
Cronograma: **Maio 01–Dezembro 31, 2026** | **NOC SR → SRE** | **30 Labs Zabbix**

## 🎯 Objetivo

Transformar de NOC Sênior em SRE Engineer seguindo o roadmap SRE Medium completo (15/15 hard skills).

## 📊 Estrutura

- **36 semanas** (mei–dez 2026)
- **5 fases** (Foundation, Core, Cloud, Advanced, Capstone)
- **12 cursos pagos** (~163h)
- **13 recursos gratuitos** (~50h)
- **30 labs Zabbix** (1/semana — sua expertise!)
- **Escala 12x36** integrada (4h folga, 0.5h plantão/dia)

## 📅 Fases

| Fase | Semanas | Tema | Cursos |
|------|---------|------|--------|
| 1 | 1–5 | Foundation | Linux, Networking, Bash |
| 2 | 6–9 | Core Skills | Git, Python, SQL |
| 3 | 10–18 | Cloud & IaC | AWS, Terraform, Ansible |
| 4 | 19–27 | Advanced SRE | K8s, Monitoring, Incidents |
| 5 | 28–36 | Capstone | Projeto final + preparação carreira |

## 🧪 Labs Zabbix

Cronograma inclui **30 labs Zabbix** (1 por semana) para consolidar expertise:

- S02: Zabbix agent install
- S03: Custom network items
- ...
- S31: End-to-end automation

Cada lab integra com o conteúdo semanal da aula.

## 🚀 Como rodar

\`\`\`bash
python main.py
\`\`\`

Abre automaticamente em `http://localhost:8000`

## 📈 Progresso Esperado

Jan 2027: **SRE Engineer Junior/Mid-level** com expertise em:
- Linux + Networking + Bash
- Python + SQL + Git
- AWS + Terraform + Ansible
- Kubernetes + Monitoring
- Incident Management
- **Zabbix (diferencial!)**

---

*Atualizado: Maio 2026 | 36 semanas | 100% roadmap SRE Medium*
```

---

### TAREFA 9: Criar/Atualizar `COURSES.md`

**O que mudar:**
- Listar todos os 12 cursos pagos com URLs
- Listar todos os 13 recursos gratuitos com URLs
- Mapear qual semana cada curso começa

**Estrutura:**
```markdown
# Cursos SRE — Cronograma Completo

## Cursos Pagos (12 | ~163h)

### Fase 1: Foundation

1. **SRE DevOps: Jornada do Início ao Fim** (4h)
   - Plataforma: Udemy
   - URL: https://www.udemy.com/course/...
   - Semana: S01
   - Conteúdo: SRE mindset, SLOs, error budgets

2. **GNU/Linux Admin** (9h)
   - Plataforma: Udemy
   - URL: https://www.udemy.com/course/...
   - Semana: S02–S04
   - Conteúdo: CLI, permissions, processes, packages

... (mais cursos)

## Conteúdo Gratuito (13 | ~50h)

### Fase 1: Foundation

1. **Linux Journey**
   - URL: https://linuxjourney.com
   - Semana: S02–S03
   - Tipo: Interativo
   - Horas: 3h

... (mais gratuitos)

## Resumo

Total: 25 recursos
Horas: ~213h conteúdo
Labs: 30 Zabbix (1/semana)
```

---

### TAREFA 10: Git Commit & Push

**O que fazer:**
1. Commitar todas as mudanças com mensagem descritiva:
   ```
   git add .
   git commit -m "Atualizar cronograma: 31→36 semanas, integrar 30 labs Zabbix, incident management"
   git push origin main
   ```

2. Criar tag para versão:
   ```
   git tag -a v2.0.0 -m "36 semanas, 30 labs Zabbix, 5 fases, capstone"
   git push origin v2.0.0
   ```

---

## 📁 ARQUIVOS DE REFERÊNCIA

Você tem os seguintes arquivos para usar como referência:

1. **`cronograma_final_sre_robson.md`** (Principal)
   - Semana-a-semana S01–S36
   - Todos os cursos + labs mapeados
   - Use para popular `curriculum.py`

2. **`SUMARIO_EXECUTIVO_FINAL.md`**
   - Validação de 15/15 skills
   - Números finais
   - Para README

3. **`cursos_cronograma_escala.md`**
   - Catálogo de cursos
   - URLs dos cursos
   - Para `COURSES.md`

4. **`gap_analysis_roadmap_vs_cursos.md`**
   - Análise detalhada
   - Para contexto/documentação

---

## 🎯 CHECKLIST DE IMPLEMENTAÇÃO

- [ ] Atualizar `data/curriculum.py` (36 semanas, 30 labs)
- [ ] Atualizar `models.py` (novos campos)
- [ ] Atualizar `routers/progress.py` (novos endpoints)
- [ ] Atualizar `routers/stats.py` (novas métricas)
- [ ] Atualizar `static/app.js` (visualização 36 semanas)
- [ ] Atualizar `static/style.css` (estilos labs Zabbix)
- [ ] Atualizar `templates/index.html` (seção labs)
- [ ] Atualizar `README.md` (nova estrutura)
- [ ] Criar/atualizar `COURSES.md` (catálogo)
- [ ] Testar localmente (`python main.py`)
- [ ] Git commit + push
- [ ] Git tag v2.0.0

---

## ⚠️ NOTAS IMPORTANTES

1. **Migração de Dados:** Se o banco já existe com 31 semanas, precisa de migração
   - Opção A: Delete `sre_tracker.db` (recomeça do zero)
   - Opção B: Script de migração (mais complexo, mantém dados)
   - **Recomendação:** Opção A (é novo cronograma, começa fresco)

2. **Escala 12x36:** Não precisa de visualização especial no código
   - Só use em documentação
   - Backend calcula horas disponíveis automaticamente

3. **Labs Zabbix:** Coloque como lições normais com `type: "lab"`
   - Badge especial no frontend
   - Contam para estatísticas

4. **Incident Management:** Adicione como lições normais em S26–S27
   - Tipo: "aula" (Google SRE Book) + "prático"
   - Use como marker de fase 4 final

5. **Testes:** Após atualizar, testear:
   - Dashboard carrega 36 semanas
   - Labs Zabbix aparecem com badge
   - Stats mostram "30 labs" + "36 semanas"
   - Export JSON completo funciona
   - Browser abre automaticamente

---

## 📞 DÚVIDAS?

Se encontrar dúvidas durante implementação:
1. Consulte `cronograma_final_sre_robson.md` para detalhes semana-a-semana
2. Consulte `COURSES.md` para URLs dos cursos
3. Consulte `gap_analysis_roadmap_vs_cursos.md` para contexto das habilidades

---

**Status:** ✅ Pronto para implementar
**Data:** Maio 2026
**Versão Final:** v2.0.0 (36 semanas + 30 labs Zabbix)

