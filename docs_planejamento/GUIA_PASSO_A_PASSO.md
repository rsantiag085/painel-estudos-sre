# 📖 GUIA PASSO-A-PASSO: Atualizar Painel SRE

## Visão Geral

Você vai atualizar seu repositório `painel-estudos-sre` de 31 para 36 semanas, integrando:
- ✅ 12 cursos pagos + 13 gratuitos
- ✅ 30 labs Zabbix (1/semana)
- ✅ Incident Management em S26–S27
- ✅ Nova estrutura de 5 fases (adicionando Capstone)

**Tempo estimado:** 4–6 horas (implementação + testes)

---

## 🚀 PASSO 1: Clonar/Atualizar o Repo Localmente

```bash
# Se não tiver ainda
git clone https://github.com/rsantiag085/painel-estudos-sre.git
cd painel-estudos-sre

# Se já tem, atualizar
git pull origin main

# Criar branch para as mudanças
git checkout -b update/36-weeks-cronograma
```

---

## 📋 PASSO 2: Deletar Banco de Dados Antigo (Recomendado)

Como é novo cronograma, não precisa de migração:

```bash
# Se o arquivo existe, deletar
rm -f sre_tracker.db

# Ou renomear para backup
mv sre_tracker.db sre_tracker_backup.db
```

---

## 🔄 PASSO 3: Atualizar `data/curriculum.py`

### A. Verificar estrutura atual

```bash
cat data/curriculum.py | head -50
```

### B. Usar o template fornecido

Use o arquivo `curriculum_py_template.py` como base. **Você tem 2 opções:**

**OPÇÃO 1 (Rápida — Claude Code/Antigravity):**
1. Abra prompt `PROMPT_ATUALIZAR_PAINEL_SRE.md` no Claude Code
2. Cole o arquivo `cronograma_final_sre_robson.md` como contexto
3. Deixa Claude gerar o `curriculum.py` completo

**OPÇÃO 2 (Manual — se quiser controle):**
1. Abra `cronograma_final_sre_robson.md`
2. Copie seção "DISTRIBUIÇÃO DE CURSOS POR SEMANA" (S01–S36)
3. Preencha manualmente `WEEKS` dict em `curriculum.py`
4. Adicione 30 labs Zabbix seguindo padrão do template

### C. Estrutura que deve ficar

```python
# data/curriculum.py

PHASES = [
    {"id": 1, "name": "Foundation", "weeks": [1,2,3,4,5], ...},
    {"id": 2, "name": "Core Skills", "weeks": [6,7,8,9], ...},
    {"id": 3, "name": "Cloud & IaC", "weeks": [10,11,...,18], ...},
    {"id": 4, "name": "Advanced SRE", "weeks": [19,20,...,27], ...},
    {"id": 5, "name": "Capstone", "weeks": [28,29,...,36], ...},
]

WEEKS = {
    1: {...},
    2: {...},
    ...
    36: {...}
}

MILESTONES = [
    {"id": "s05_phase1", "phase": 1, "week": 5, "title": "Fase 1 Completa", ...},
    {"id": "s09_phase2", "phase": 2, "week": 9, "title": "Fase 2 Completa", ...},
    {"id": "s18_phase3", "phase": 3, "week": 18, "title": "Fase 3 Completa", ...},
    {"id": "s27_phase4", "phase": 4, "week": 27, "title": "Fase 4 Completa", ...},
    {"id": "s36_capstone", "phase": 5, "week": 36, "title": "Capstone Concluído", ...},
    {"id": "all_labs_done", "phase": 4, "week": 31, "title": "30 Labs Zabbix Completos", ...},
]
```

---

## 🛢️ PASSO 4: Atualizar `models.py`

### A. Verificar campos atuais

```bash
cat models.py | grep "class LessonProgress" -A 20
```

### B. Adicionar novos campos (se não existirem)

Procure a classe `LessonProgress` e adicione:

```python
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime

class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    
    id = Column(Integer, primary_key=True)
    lesson_id = Column(String, unique=True, index=True)
    
    # NOVOS CAMPOS (adicione isto):
    week_num = Column(Integer, nullable=True)          # Que semana (1-36)
    lab_type = Column(String, nullable=True)           # "aula", "lab", "leitura", "projeto"
    course_url = Column(String, nullable=True)         # URL do curso
    
    # Campos existentes (mantém):
    status = Column(String, default="pending")
    note = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### C. Testar

```bash
python main.py
# Se der erro de tabela, delete o DB e deixe criar novamente
```

---

## 🔌 PASSO 5: Atualizar `routers/progress.py`

### A. Manter endpoints atuais

Mantenha os GET/POST existentes para `/api/progress`.

### B. Adicionar novos endpoints (opcional, mas útil)

```python
# routers/progress.py

from fastapi import APIRouter, Query

router = APIRouter()

# Endpoints existentes (mantém)
@router.get("/api/progress")
async def get_all_progress():
    ...

@router.post("/api/progress/{lesson_id}")
async def save_lesson_progress(lesson_id: str, ...):
    ...

# NOVOS endpoints (adicione):

@router.get("/api/progress/week/{week_num}")
async def get_week_progress(week_num: int):
    """Retorna todas as lições de uma semana"""
    ...

@router.get("/api/progress/labs")
async def get_zabbix_labs():
    """Retorna só os labs Zabbix"""
    ...

@router.get("/api/progress/next")
async def get_next_lessons(limit: int = Query(3)):
    """Retorna próximas N lições não iniciadas"""
    ...
```

---

## 📊 PASSO 6: Atualizar `routers/stats.py`

### A. Adicionar novos KPIs

```python
# routers/stats.py

@router.get("/api/stats")
async def get_stats():
    return {
        # Estatísticas anteriores (mantém)
        "total_lessons": 450,
        "completed": 0,
        "percentage": 0,
        
        # NOVOS (adicione):
        "total_labs_zabbix": 30,
        "labs_completed": 0,
        "labs_percentage": 0,
        "by_type": {
            "aula": 0,
            "lab": 0,
            "leitura": 0,
            "projeto": 0
        },
        "weeks_total": 36,
        "weeks_completed": 0,
        "expected_completion": "2026-12-31",
        
        # Por fase
        "by_phase": {
            1: {"completed": 0, "total": 50, "percentage": 0},
            2: {"completed": 0, "total": 60, "percentage": 0},
            3: {"completed": 0, "total": 120, "percentage": 0},
            4: {"completed": 0, "total": 150, "percentage": 0},
            5: {"completed": 0, "total": 70, "percentage": 0},
        }
    }
```

---

## 🎨 PASSO 7: Atualizar `static/app.js`

### A. Adicionar funções para labs Zabbix

```javascript
// static/app.js

// Renderizar badge para labs Zabbix
function getLessonBadge(lesson) {
    if (lesson.lab_type === "lab" && lesson.course === "Zabbix Lab") {
        return `<span class="badge badge-zabbix">🧪 LAB ZABBIX</span>`;
    }
    if (lesson.tag === "aws") return `<span class="badge badge-aws">☁️ AWS</span>`;
    if (lesson.tag === "book") return `<span class="badge badge-book">📖 LEITURA</span>`;
    if (lesson.tag === "free") return `<span class="badge badge-free">💚 GRÁTIS</span>`;
    return "";
}

// Renderizar progresso por semana
function renderWeekSummary(weekNum) {
    const week = curriculum.weeks[weekNum];
    if (!week) return "";
    
    return `
        <div class="week-card">
            <h4>Semana ${weekNum}</h4>
            <p>${week.title}</p>
            <div class="week-lessons">
                ${week.lessons.map(lesson => `
                    <div class="lesson-item ${lesson.status}">
                        <input type="checkbox" id="lesson-${lesson.id}" 
                               onchange="saveLessonProgress('${lesson.id}', this.checked)">
                        <label for="lesson-${lesson.id}">
                            ${lesson.title}
                            ${getLessonBadge(lesson)}
                            <small>(${lesson.hours}h)</small>
                        </label>
                    </div>
                `).join('')}
            </div>
        </div>
    `;
}

// Adicionar seção de labs Zabbix no dashboard
function renderZabbixLabsSection() {
    fetch('/api/progress/labs')
        .then(r => r.json())
        .then(labs => {
            const completed = labs.filter(l => l.status === 'done').length;
            const total = labs.length;
            const percent = Math.round((completed / total) * 100);
            
            document.getElementById('zabbix-section').innerHTML = `
                <h3>🧪 Labs Zabbix (${completed}/${total})</h3>
                <div class="progress">
                    <div class="progress-bar" style="width: ${percent}%"></div>
                </div>
                <p>${percent}% concluído</p>
            `;
        });
}
```

---

## 🎨 PASSO 8: Atualizar `static/style.css`

### A. Adicionar estilos para labs Zabbix

```css
/* static/style.css */

/* Badge Zabbix */
.badge-zabbix {
    background-color: #FF9F1C;
    color: #fff;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 0.75em;
    margin-left: 8px;
    font-weight: bold;
}

.badge-aws {
    background-color: #FF9900;
    color: #fff;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 0.75em;
    margin-left: 8px;
}

.badge-book {
    background-color: #4A90E2;
    color: #fff;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 0.75em;
    margin-left: 8px;
}

.badge-free {
    background-color: #7ED321;
    color: #fff;
    padding: 3px 8px;
    border-radius: 3px;
    font-size: 0.75em;
    margin-left: 8px;
}

/* Destaque para lab lessons */
.lesson-item.lab {
    border-left: 4px solid #FF9F1C;
    padding-left: 12px;
}

/* Week card */
.week-card {
    background: #1e1e1e;
    border: 1px solid #333;
    border-radius: 8px;
    padding: 16px;
    margin: 12px 0;
}

.week-card h4 {
    color: #00D9FF;
    margin: 0 0 8px 0;
    font-family: 'JetBrains Mono', monospace;
}

/* Labs section */
#zabbix-section {
    background: #1a1a2e;
    border: 2px solid #FF9F1C;
    border-radius: 8px;
    padding: 16px;
    margin: 12px 0;
}

#zabbix-section h3 {
    color: #FF9F1C;
    margin-top: 0;
}

.progress {
    background: #333;
    height: 24px;
    border-radius: 4px;
    overflow: hidden;
    margin: 8px 0;
}

.progress-bar {
    background: linear-gradient(90deg, #FF9F1C, #FFB84D);
    height: 100%;
    transition: width 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #fff;
    font-size: 0.8em;
    font-weight: bold;
}
```

---

## 📄 PASSO 9: Atualizar `templates/index.html`

### A. Adicionar seção para labs Zabbix

Encontre a seção de navegação e adicione novo item:

```html
<!-- templates/index.html -->

<nav class="sidebar">
    <h2>SRE Tracker</h2>
    <ul>
        <li><a href="#" onclick="showDashboard()">⬡ Dashboard</a></li>
        <li><a href="#" onclick="showCronograma()">📅 Cronograma</a></li>
        <li><a href="#" onclick="showMilestones()">✓ Milestones</a></li>
        <li><a href="#" onclick="showZabbixLabs()">🧪 Labs Zabbix</a></li>
        <li><a href="#" onclick="showStats()">📊 Estatísticas</a></li>
        <li><a href="#" onclick="exportData()">📤 Exportar</a></li>
    </ul>
</nav>

<!-- Seção de Labs Zabbix (nova) -->
<section id="zabbix-section" style="display: none;">
    <h3>🧪 Labs Zabbix (30 total)</h3>
    <div class="progress">
        <div class="progress-bar" style="width: 0%"></div>
    </div>
    <p id="zabbix-count">0/30 concluídos (0%)</p>
    <ul id="zabbix-list"></ul>
</section>
```

---

## 📝 PASSO 10: Atualizar `README.md`

### A. Substituir conteúdo antigo

```markdown
# SRE Tracker — Robson Santiago

Sistema de acompanhamento de estudos SRE com **36 semanas**, **5 fases** e ~213h de conteúdo.
Cronograma: **Maio 01–Dezembro 31, 2026** | **NOC SR → SRE** | **30 Labs Zabbix**

## 🎯 Objetivo

Transformar de NOC Sênior em SRE Engineer seguindo o roadmap SRE Medium (15/15 hard skills).

## 📊 Resumo

- **36 semanas** (mai–dez 2026)
- **5 fases** (Foundation, Core, Cloud, Advanced, Capstone)
- **12 cursos pagos** (~163h)
- **13 recursos gratuitos** (~50h)
- **30 labs Zabbix** (1/semana — sua expertise!)
- **~560h disponíveis** (escala 12x36)

## 🚀 Como Rodar

\`\`\`bash
python main.py
\`\`\`

Abre automaticamente em `http://localhost:8000`

## 📅 Fases

| Fase | Semanas | Conteúdo |
|------|---------|----------|
| 1 | S01–S05 | Foundation: Linux, Networking, Bash |
| 2 | S06–S09 | Core Skills: Git, Python, SQL |
| 3 | S10–S18 | Cloud & IaC: AWS, Terraform, Ansible |
| 4 | S19–S27 | Advanced SRE: K8s, Monitoring, Incidents |
| 5 | S28–S36 | Capstone: Projeto + Carreira |

## 🧪 Labs Zabbix

30 labs práticos (1/semana) para consolidar expertise em Zabbix:

- S02: Install agent
- S03: Custom items
- ...
- S31: End-to-end automation

---

*Atualizado: Maio 2026 | Versão 2.0.0*
```

---

## 📚 PASSO 11: Criar/Atualizar `COURSES.md`

```bash
# Se não existe
touch COURSES.md

# Copiar conteúdo de cursos_cronograma_escala.md
cat cursos_cronograma_escala.md > COURSES.md
```

---

## ✅ PASSO 12: Testar Localmente

### A. Instalar dependências

```bash
pip install -r requirements.txt
```

### B. Rodar aplicação

```bash
python main.py
```

### C. Verificar no browser

```
http://localhost:8000
```

**Checklist de testes:**
- [ ] Dashboard carrega (36 semanas)
- [ ] Semanas aparecem S01–S36
- [ ] Labs Zabbix têm badge 🧪
- [ ] Estatísticas mostram "30 labs"
- [ ] Milestones incluem "30 Labs Zabbix Completos"
- [ ] Export JSON funciona
- [ ] Salvar progresso funciona
- [ ] Dados salvam no banco

---

## 🔀 PASSO 13: Git Commit & Push

### A. Verificar mudanças

```bash
git status
```

### B. Adicionar arquivo

```bash
git add .
```

### C. Commit com mensagem

```bash
git commit -m "Atualizar cronograma: 31→36 semanas, 30 labs Zabbix, 5 fases, capstone

- Aumentar de 31 para 36 semanas (mai-dez 2026)
- Adicionar 30 labs Zabbix (1/semana, S02-S31)
- Integrar Incident Management (S26-S27, gratuito)
- Adicionar Fase 5: Capstone (S28-S36)
- Atualizar cursos pagos (12 total) + gratuitos (13 total)
- Melhorar UI: badges para labs, seção Zabbix
- Atualizar README e documentação"
```

### D. Push para main

```bash
git push origin update/36-weeks-cronograma
```

### E. Criar Pull Request (no GitHub UI)

1. Vá em https://github.com/rsantiag085/painel-estudos-sre
2. Clique em "Compare & pull request"
3. Escreva descrição
4. Merge

### F. Criar tag v2.0.0

```bash
git checkout main
git pull
git tag -a v2.0.0 -m "Release v2.0.0: 36 semanas, 30 labs Zabbix, capstone"
git push origin v2.0.0
```

---

## 📞 TROUBLESHOOTING

### Erro: "database is locked"

```bash
# Delete e recrie
rm sre_tracker.db
python main.py
```

### Erro: "No module named X"

```bash
pip install -r requirements.txt
```

### Browser não abre automaticamente

```bash
# Rodar manualmente
python main.py
# Abrir manualmente em http://localhost:8000
```

### Banco não criou as tabelas

```bash
# Delete e deixe criar novamente
rm sre_tracker.db
python main.py
```

---

## ✨ RESULTADO FINAL

Após completar todos os passos:

✅ Repositório atualizado para 36 semanas
✅ 30 labs Zabbix integrados
✅ UI melhorada com badges e seções
✅ Documentação completa
✅ v2.0.0 publicada
✅ Pronto para começar mai 01!

---

*Guia completo | 13 passos | ~4–6 horas de trabalho*
*Robson Santiago | Maio 2026*
