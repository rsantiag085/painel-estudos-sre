# CRONOGRAMA SRE v2.0 — COM INTEGRAÇÃO CLAUDE + IA
**Robson Santiago | NOC Sênior → SRE Mid-Level**
**INÍCIO: 02/06/2026 (IMUTÁVEL) | FIM ESTIMADO: ~Fev/2027 | 36 semanas**

---

## 📌 INSTRUÇÕES PARA CLAUDE CODE

**Arquivo:** `docs_planejamento/CRONOGRAMA_v2.0_COM_CLAUDE_IA.md`

**Leia antes de executar:**
1. `docs_planejamento/00_LEIA_PRIMEIRO.md`
2. `docs_planejamento/PROMPT_ATUALIZAR_PAINEL.md`
3. `COURSES.md`
4. `data/curriculum.py`
5. Este arquivo

**Regra crítica:** Data de início = **02/06/2026**. Não alterar por nenhum motivo.

---

## 🗓️ ESCALA 12x36 — REGRA POR MÊS (VALIDADA)

```
Mês            Folga       Trabalho    Último dia   Obs
──────────────────────────────────────────────────────────────
Jun/2026       PARES       ímpares     30/06 [F]
Jul/2026       PARES       ímpares     31/07 [T]    → inverte ago
Ago/2026       ÍMPARES     pares       31/08 [F]
Set/2026       PARES       ímpares     30/09 [F]
Out/2026       PARES       ímpares     31/10 [T]    → inverte nov
Nov/2026       ÍMPARES     pares       30/11 [T]
Dez/2026       ÍMPARES     pares       31/12 [F]
Jan/2027       PARES       ímpares     31/01 [T]    → inverte fev
Fev/2027       ÍMPARES     pares       28/02 [T]

Horas por dia:  FOLGA = 4h (manhã 2h + tarde 2h)
                TRABALHO = 0.5h (passivo: podcast, revisão)
```

---

## 📅 CALENDÁRIO COMPLETO — 02/06/2026 A FEV/2027

### JUNHO 2026 — Fases 1-2 (S01–S04)

```
S01 (17.5h) — INÍCIO OFICIAL
  Seg 02/06[F]  Ter 03/06[T]  Qua 04/06[F]  Qui 05/06[T]
  Sex 06/06[F]  Sáb 07/06[T]  Dom 08/06[F]
  Foco: SRE Mindset + GNU/Linux início
  🆕 Udemy English: 0.5h passivo (dias de trabalho)

S02 (17.5h)
  Seg 09/06[F]  Ter 10/06[T]  Qua 11/06[F]  Qui 12/06[T]
  Sex 13/06[F]  Sáb 14/06[T]  Dom 15/06[F]
  Foco: GNU/Linux Fundamentos + Python início
  🆕 Prompt Engineering Deeplearning.AI (2h — Seg 09/06 manhã)
  🆕 Udemy English: 0.5h passivo

S03 (14.0h)
  Seg 16/06[T]  Ter 17/06[F]  Qua 18/06[T]  Qui 19/06[F]
  Sex 20/06[T]  Sáb 21/06[F]  Dom 22/06[T]
  Foco: Python para DevOps + Prompt Engineering cont.
  🆕 Prompt Engineering (2h — Ter 17/06 manhã)
  🆕 Udemy English: 0.5h passivo
  Lab Zabbix #1: Ter 17/06[F] tarde

S04 (17.5h)
  Seg 23/06[F]  Ter 24/06[T]  Qua 25/06[F]  Qui 26/06[T]
  Sex 27/06[F]  Sáb 28/06[T]  Dom 29/06[F]
  Foco: Python + SQL + Git
  🆕 Prompt Engineering (2h — Seg 23/06 manhã) — CONCLUÍDO
  🆕 Udemy English: 0.5h passivo
  Lab Zabbix #2: Seg 23/06[F] tarde
```

### JULHO 2026 — Fase 3 Infrastructure (S05–S09)

```
S05 (14.0h)
  Seg 30/06[T]  Ter 01/07[F]  Qua 02/07[T]  Qui 03/07[F]
  Sex 04/07[T]  Sáb 05/07[F]  Dom 06/07[T]
  Foco: AWS SAA-C03 início
  🆕 Udemy English: 0.5h passivo
  Lab Zabbix #3: Ter 01/07[F] tarde

S06 (17.5h)
  Seg 07/07[F]  Ter 08/07[T]  Qua 09/07[F]  Qui 10/07[T]
  Sex 11/07[F]  Sáb 12/07[T]  Dom 13/07[F]
  Foco: AWS SAA-C03 (IAM, EC2, VPC, S3)
  🆕 Udemy English: 0.5h passivo
  Lab Zabbix #4: Seg 07/07[F] tarde

S07 (14.0h)
  Seg 14/07[T]  Ter 15/07[F]  Qua 16/07[T]  Qui 17/07[F]
  Sex 18/07[T]  Sáb 19/07[F]  Dom 20/07[T]
  Foco: AWS SAA-C03 (RDS, ELB, CloudWatch)
  🆕 Udemy English: 0.5h passivo
  Lab Zabbix #5: Ter 15/07[F] tarde

S08 (17.5h)
  Seg 21/07[F]  Ter 22/07[T]  Qua 23/07[F]  Qui 24/07[T]
  Sex 25/07[F]  Sáb 26/07[T]  Dom 27/07[F]
  Foco: AWS SAA-C03 (Lambda, Route53, Security)
  🆕 Udemy English: 0.5h passivo
  Lab Zabbix #6: Seg 21/07[F] tarde

S09 (14.0h)
  Seg 28/07[T]  Ter 29/07[F]  Qua 30/07[T]  Qui 31/07[F]
  Foco: AWS SAA-C03 revisão + simulado
  🆕 Udemy English: 0.5h passivo
  Lab Zabbix #7: Ter 29/07[F] tarde
```

### AGOSTO 2026 — Fase 3 continuação (S10–S14)

```
AGOSTO: ÍMPARES = FOLGA | PARES = TRABALHO

S10 (17.5h)
  Sex 01/08[F]  Sáb 02/08[T]  Dom 03/08[F]
  Seg 04/08[T]  Ter 05/08[F]  Qua 06/08[T]  Qui 07/08[F]
  Foco: AWS simulado final + agendar prova SAA-C03
  🆕 Udemy English: 1h/dia (intensifica a partir de ago)
  Lab Zabbix #8: Sex 01/08[F] tarde

S11 (14.0h)
  Sex 08/08[T]  Sáb 09/08[F]  Dom 10/08[T]
  Seg 11/08[F]  Ter 12/08[T]  Qua 13/08[F]  Qui 14/08[T]
  Foco: Terraform Essentials (5h)
  🆕 Udemy English: 1h/dia
  Lab Zabbix #9: Sáb 09/08[F] tarde

S12 (17.5h)
  Sex 15/08[F]  Sáb 16/08[T]  Dom 17/08[F]
  Seg 18/08[T]  Ter 19/08[F]  Qua 20/08[T]  Qui 21/08[F]
  Foco: Ansible para SysAdmin início (19h total)
  🆕 Udemy English: 1h/dia
  Lab Zabbix #10: Sex 15/08[F] tarde

S13 (14.0h)
  Sex 22/08[T]  Sáb 23/08[F]  Dom 24/08[T]
  Seg 25/08[F]  Ter 26/08[T]  Qua 27/08[F]  Qui 28/08[T]
  Foco: Ansible (roles, vault, templates)
  🆕 Udemy English: 1h/dia
  Lab Zabbix #11: Sáb 23/08[F] tarde

S14 (17.5h)
  Sex 29/08[F]  Sáb 30/08[T]  Dom 31/08[F]
  Seg 01/09[T]  Ter 02/09[F]  Qua 03/09[T]  Qui 04/09[F]
  Foco: Ansible avançado + AWX início (8h)
  🆕 Udemy English: 1h/dia
  Lab Zabbix #12: Sex 29/08[F] tarde
```

### SETEMBRO 2026 — Fases 3-4 (S15–S18)

```
SETEMBRO: PARES = FOLGA | ÍMPARES = TRABALHO

S15 (17.5h)
  Sex 05/09[T]  Sáb 06/09[F]  Dom 07/09[T]
  Seg 08/09[F]  Ter 09/09[T]  Qua 10/09[F]  Qui 11/09[T]
  Foco: AWX (webhooks, RBAC, workflows)
  🆕 Udemy English: 1h/dia
  Lab Zabbix #13: Sáb 06/09[F] tarde

S16 (14.0h)
  Sex 12/09[F]  Sáb 13/09[T]  Dom 14/09[F]
  Seg 15/09[T]  Ter 16/09[F]  Qua 17/09[T]  Qui 18/09[F]
  Foco: GitHub Actions (7h) — CI/CD pipelines
  🆕 Udemy English: 1h/dia
  Lab Zabbix #14: Sex 12/09[F] tarde

S17 (17.5h)
  Sex 19/09[T]  Sáb 20/09[F]  Dom 21/09[T]
  Seg 22/09[F]  Ter 23/09[T]  Qua 24/09[F]  Qui 25/09[T]
  Foco: Flask Projeto DevOps (14h) — Docker, testes
  🆕 Udemy English: 1h/dia
  Lab Zabbix #15: Sáb 20/09[F] tarde

S18 (14.0h)
  Sex 26/09[F]  Sáb 27/09[T]  Dom 28/09[F]
  Seg 29/09[T]  Ter 30/09[F]
  Foco: Flask Projeto — deploy K8s, observabilidade
  🆕 Udemy English: 1h/dia
  Lab Zabbix #16: Sex 26/09[F] tarde
```

### OUTUBRO 2026 — Fase 4 Advanced SRE (S19–S23)

```
OUTUBRO: PARES = FOLGA | ÍMPARES = TRABALHO

S19 (17.5h)
  Qua 01/10[T]  Qui 02/10[F]  Sex 03/10[T]
  Sáb 04/10[F]  Dom 05/10[T]  Seg 06/10[F]  Ter 07/10[T]
  Foco: Kubernetes Completo (19h) — arquitetura, kubectl, pods
  🆕 Build with Claude API Lesson 1-2 (2h — Qui 02/10[F] tarde)
  🆕 Udemy English: 1h/dia
  Lab Zabbix #17: Qui 02/10[F] tarde (após Claude API)

S20 (14.0h)
  Qua 08/10[F]  Qui 09/10[T]  Sex 10/10[F]
  Sáb 11/10[T]  Dom 12/10[F]  Seg 13/10[T]  Ter 14/10[F]
  Foco: Kubernetes (services, configmaps, volumes, ingress)
  🆕 Build with Claude API Lesson 3-4 (2h — Qua 08/10[F] tarde)
  🆕 Udemy English: 1h/dia
  Lab Zabbix #18: Qua 08/10[F] tarde (após Claude API)

S21 (17.5h)
  Qua 15/10[T]  Qui 16/10[F]  Sex 17/10[T]
  Sáb 18/10[F]  Dom 19/10[T]  Seg 20/10[F]  Ter 21/10[T]
  Foco: Kubernetes (RBAC, HPA, Helm) + Prometheus início
  🆕 Build with Claude API Lesson 5 (2h — Qui 16/10[F] tarde)
  🆕 LangChain RAG Lesson 1-2 (2h — Sáb 18/10[F] manhã)
  🆕 Udemy English: 1h/dia
  Lab Zabbix #19: Qui 16/10[F] tarde

S22 (14.0h)
  Qua 22/10[F]  Qui 23/10[T]  Sex 24/10[F]
  Sáb 25/10[T]  Dom 26/10[F]  Seg 27/10[T]  Ter 28/10[F]
  Foco: Prometheus + Grafana (7h)
  🆕 Build with Claude API Projeto: "SRE Agent v1" (2h — Qua 22/10[F] tarde)
  🆕 LangChain RAG Lesson 3-4 (2h — Sex 24/10[F] tarde)
  🆕 Udemy English: 1h/dia
  Lab Zabbix #20: Qua 22/10[F] tarde

S23 (17.5h)
  Qua 29/10[F]  Qui 30/10[T]  Sex 31/10[F]
  Sáb 01/11[T]  Dom 02/11[F]  Seg 03/11[T]  Ter 04/11[F]
  Foco: SRE Book (Monitoring, Incident Response)
  🆕 LangChain RAG Projeto: "Runbook Vector Store" (2h — Sex 31/10[F] tarde)
  🆕 Udemy English: 1h/dia
  Lab Zabbix #21: Qua 29/10[F] tarde
```

### NOVEMBRO 2026 — Fase 4 + Capstone Prep (S24–S27)

```
NOVEMBRO: ÍMPARES = FOLGA | PARES = TRABALHO

S24 (14.0h)
  Qua 05/11[F]  Qui 06/11[T]  Sex 07/11[F]
  Sáb 08/11[T]  Dom 09/11[F]  Seg 10/11[T]  Ter 11/11[F]
  Foco: Incident Management + SLOs + Chaos Engineering
  🆕 Claude Agent v2 Completo (2h — Qua 05/11[F] tarde)
  🆕 Udemy English: 1h/dia
  Lab Zabbix #22: Qua 05/11[F] tarde

S25 (17.5h)
  Qua 12/11[T]  Qui 13/11[F]  Sex 14/11[T]
  Sáb 15/11[F]  Dom 16/11[T]  Seg 17/11[F]  Ter 18/11[T]
  Foco: Mock incident drill + Runbooks + Postmortem
  🆕 Integração Completa: Zabbix→Webhook→Claude→Postmortem (2h)
  🆕 Udemy English: 1h/dia
  Lab Zabbix #23: Qui 13/11[F] tarde

S26 (14.0h)
  Qua 19/11[F]  Qui 20/11[T]  Sex 21/11[F]
  Sáb 22/11[T]  Dom 23/11[F]  Seg 24/11[T]  Ter 25/11[F]
  Foco: Capstone prep — arquitetura + decisões + IaC base
  🆕 Udemy English: 1.5h/dia (sprint final)
  Lab Zabbix #24: Qua 19/11[F] tarde

S27 (17.5h)
  Qua 26/11[T]  Qui 27/11[F]  Sex 28/11[T]
  Sáb 29/11[F]  Dom 30/11[T]
  Foco: Capstone — Terraform AWS (VPC, EC2, RDS, EKS)
  🆕 Udemy English: 1.5h/dia
  Lab Zabbix #25: Qui 27/11[F] tarde
```

### DEZEMBRO 2026 — Fase 5 Capstone (S28–S32)

```
DEZEMBRO: ÍMPARES = FOLGA | PARES = TRABALHO

S28 (17.5h)
  Seg 01/12[F]  Ter 02/12[T]  Qua 03/12[F]  Qui 04/12[T]
  Sex 05/12[F]  Sáb 06/12[T]  Dom 07/12[F]
  Foco: Capstone — Aplicação Flask + Docker + testes
  🆕 Udemy English: 1.5h/dia
  Lab Zabbix #26: Seg 01/12[F] tarde

S29 (14.0h)
  Seg 08/12[T]  Ter 09/12[F]  Qua 10/12[T]  Qui 11/12[F]
  Sex 12/12[T]  Sáb 13/12[F]  Dom 14/12[T]
  Foco: Capstone — Kubernetes + Helm + deploy EKS
  🆕 Udemy English: 1.5h/dia
  Lab Zabbix #27: Ter 09/12[F] tarde

S30 (17.5h)
  Seg 15/12[F]  Ter 16/12[T]  Qua 17/12[F]  Qui 18/12[T]
  Sex 19/12[F]  Sáb 20/12[T]  Dom 21/12[F]
  Foco: Capstone — CI/CD GitHub Actions + Observabilidade
  🆕 Udemy English: 1.5h/dia
  Lab Zabbix #28: Seg 15/12[F] tarde

S31 (14.0h)
  Seg 22/12[T]  Ter 23/12[F]  Qua 24/12[T]  Qui 25/12[F]
  Sex 26/12[T]  Sáb 27/12[F]  Dom 28/12[T]
  Foco: Capstone — SRE Agent Claude integrado + SLOs
  🆕 Udemy English: 1.5h/dia
  Lab Zabbix #29: Ter 23/12[F] tarde

S32 (17.5h)
  Seg 29/12[F]  Ter 30/12[T]  Qua 31/12[F]
  Qui 01/01[T]  Sex 02/01[F]  Sáb 03/01[T]  Dom 04/01[F]
  Foco: Capstone — Video demo + documentação final
  🆕 Udemy English: 1.5h/dia
  Lab Zabbix #30: Seg 29/12[F] tarde — ÚLTIMO LAB
```

### JANEIRO–FEVEREIRO 2027 — Portfolio + Carreira (S33–S36)

```
JANEIRO: PARES = FOLGA | ÍMPARES = TRABALHO

S33 (14.0h)
  Seg 05/01[T]  Ter 06/01[F]  Qua 07/01[T]  Qui 08/01[F]
  Sex 09/01[T]  Sáb 10/01[F]  Dom 11/01[T]
  Foco: Portfolio polish — GitHub, LinkedIn, README profissional
  🆕 Udemy English: 1.5h/dia

S34 (17.5h)
  Seg 12/01[F]  Ter 13/01[T]  Qua 14/01[F]  Qui 15/01[T]
  Sex 16/01[F]  Sáb 17/01[T]  Dom 18/01[F]
  Foco: Interview prep — System Design + Troubleshooting
  🆕 Udemy English: 1.5h/dia

FEVEREIRO: ÍMPARES = FOLGA | PARES = TRABALHO

S35 (14.0h)
  Seg 19/01[T]  Ter 20/01[F]  Qua 21/01[T]  Qui 22/01[F]
  Sex 23/01[T]  Sáb 24/01[F]  Dom 25/01[T]
  Foco: Mock interviews PT-BR + EN + Behavioral questions
  🆕 Udemy English: 1.5h/dia

S36 (17.5h) — SEMANA FINAL
  Seg 26/01[T]  Ter 27/01[F]  Qua 28/01[T]  Qui 29/01[F]
  Sex 30/01[T]  Sáb 31/01[F]
  Foco: Revisão final + Celebração + Próximos passos
  🆕 Udemy English: 1.5h/dia
```

---

## 🆕 NOVOS CURSOS IA — DETALHAMENTO

### Curso A: Prompt Engineering Avançado
```
Provedor: Deeplearning.AI (gratuito)
Carga:    6h
Quando:   S02-S04 (09/06 a 29/06)
Blocos:
  Seg 09/06[F] manhã 2h — Lessons 1-2 (básico + chain-of-thought)
  Ter 17/06[F] manhã 2h — Lessons 3-4 (few-shot, system prompts)
  Seg 23/06[F] manhã 2h — Lessons 5-6 (SRE troubleshooting prompts)
Entrega: prompt-templates-troubleshooting.md
```

### Curso B: Build with Claude API (Anthropic Academy)
```
Provedor: Anthropic Academy (gratuito)
Carga:    10h
Quando:   S19-S22 (02/10 a 28/10)
Blocos:
  Qui 02/10[F] tarde 2h — Tool definition, agent loop
  Qua 08/10[F] tarde 2h — Error handling, streaming
  Qui 16/10[F] tarde 2h — Context management, advanced
  Qua 22/10[F] tarde 2h — Projeto: SRE Agent v1
  Sex 24/10[F] tarde 2h — Refinamento + testes
Entrega: repo "sre-agent-v1" no GitHub
```

### Curso C: LangChain RAG + Memory
```
Provedor: LangChain Academy (gratuito)
Carga:    8h
Quando:   S21-S23 (16/10 a 04/11)
Blocos:
  Sáb 18/10[F] manhã 2h — Embeddings, vector stores
  Sex 24/10[F] manhã 2h — Memory, chains, retrieval
  Dom 26/10[F] manhã 2h — RAG completo
  Sex 31/10[F] tarde 2h — Projeto: Runbook Vector Store
Entrega: runbook_vectorstore.pkl + CLI de busca semântica
```

### Curso D: Udemy English "Inglês Extremo" (paralelo)
```
Provedor: Udemy — https://www.udemy.com/course/inglesextremo/
Carga:    17h total
Modo:     PARALELO — não adiciona carga, usa tempo passivo
Distribuição:
  S01-S09 (jun-jul): 0.5h/dia passivo = ~13h
  S10-S18 (ago-set): 1h/dia          = ~25h
  S19-S36 (out-fev): 1.5h/dia        = ~76h
  [Total disponível > 17h — concluído antes do fim]
```

---

## 🔧 REGRAS PARA CLAUDE CODE IMPLEMENTAR

```python
# Função de tipo de dia — usar em data/curriculum.py
SCALE_RULES = {
    (2026, 6):  "even_off",   # jun: pares = folga
    (2026, 7):  "even_off",   # jul: pares = folga
    (2026, 8):  "odd_off",    # ago: ímpares = folga
    (2026, 9):  "even_off",   # set: pares = folga
    (2026, 10): "even_off",   # out: pares = folga
    (2026, 11): "odd_off",    # nov: ímpares = folga
    (2026, 12): "odd_off",    # dez: ímpares = folga
    (2027, 1):  "even_off",   # jan: pares = folga
    (2027, 2):  "odd_off",    # fev: ímpares = folga
}

def get_day_type(date):
    rule = SCALE_RULES.get((date.year, date.month))
    is_odd = date.day % 2 != 0
    is_off = (rule == "odd_off" and is_odd) or \
             (rule == "even_off" and not is_odd)
    return "FOLGA" if is_off else "TRABALHO"

def get_hours(date):
    return 4.0 if get_day_type(date) == "FOLGA" else 0.5

# START_DATE — NUNCA ALTERAR
START_DATE = date(2026, 6, 2)   # 02/06/2026 — IMUTÁVEL
```

### Novos campos no curriculum.py
```python
{
    "name": "...",
    "h": 2.0,
    "week": 1,           # Semana 1-36 (S01=semana de 02/06)
    "phase": 1,          # Fase 1-5
    "tag": "ia",         # None | "ia" | "aws" | "lab" | "free" | "book"
    "block": "manha",    # "manha" | "tarde" | "passivo"
    "type": "aula",      # "aula" | "lab" | "projeto" | "leitura"
    "provider": "...",   # "Udemy" | "Anthropic" | "Deeplearning.AI" etc
    "url": "https://...",
}
```

### Cursos a ADICIONAR (não substituir)
```
1. Prompt Engineering  → tag: "ia", phase: 1-2, weeks: 2-4
2. Claude API Build    → tag: "ia", phase: 4, weeks: 19-22
3. LangChain RAG       → tag: "ia", phase: 4, weeks: 21-23
4. Udemy English       → tag: "book", phase: all, block: "passivo"
```

---

## 📊 TOTAIS v2.0

```
Data início:         02/06/2026 (IMUTÁVEL)
Data fim estimada:   ~31/01/2027
Semanas:             36
Horas disponíveis:   ~540h

Cursos pagos:        123h (11 cursos existentes)
Cursos IA novos:      24h (Prompt Eng + Claude API + LangChain)
Inglês Udemy:         17h (paralelo)
Total conteúdo:      ~147h

Labs Zabbix:          30 labs × 1h = 30h
Projetos/Capstone:   ~363h restantes

STATUS: ✅ Encaixa com margem ampla para prática
```

---

*Versão: 2.0 | Gerado: 29/05/2026*
*Data início: 02/06/2026 — NÃO ALTERAR*
*Arquivo: docs_planejamento/CRONOGRAMA_v2.0_COM_CLAUDE_IA.md*
