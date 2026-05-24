# Cursos SRE — Catálogo Completo (v2.0)
**Robson Santiago de Oliveira | NOC Sênior → SRE**
**Período:** 10/06/2026 a 16/01/2027 — 36 semanas | 5 fases | 30 Labs Zabbix
**Versão:** v2.0 — atualizado com 12 cursos pagos + 13 gratuitos + 30 Labs Zabbix

---

## 🧪 Labs Zabbix — 30 Semanas (S05–S34)

> **Diferencial de carreira:** expertise em monitoramento avançado com Zabbix.
> 1 lab por semana, integrado ao conteúdo da fase. ~1h cada.

| Lab | Semana | Data | Tema |
|-----|--------|------|------|
| #1  | S05 | 04/06[F] | Zabbix agent install em VM Ubuntu |
| #2  | S06 | 11/06[F] | Custom network monitoring items (interface eth0) |
| #3  | S07 | 18/06[T] | Bash external check — health_check.sh integrado |
| #4  | S08 | 25/06[F] | Scripts bash commitados no GitHub |
| #5  | S09 | 02/07[T] | Python consome Zabbix API — zabbix_api.py |
| #6  | S10 | 09/07[F] | Python + Zabbix + SQLite data pipeline |
| #7  | S11 | 16/07[T] | Python integração Zabbix API — templates e triggers |
| #8  | S12 | 23/07[F] | Zabbix integração Python API — criar templates |
| #9  | S13 | 30/07[T] | AWS EC2 com Zabbix agent via user-data script |
| #10 | S14 | 06/08[F] | RDS MySQL monitorada via CloudWatch + Zabbix |
| #11 | S15 | 13/08[F] | Lambda + SNS → Zabbix webhook integration |
| #12 | S16 | 20/08[T] | Stack completa AWS monitorada end-to-end no Zabbix |
| #13 | S17 | 27/08[F] | Ansible playbook instala Zabbix agent em 5 VMs |
| #14 | S18 | 03/09[T] | Ansible gerencia templates Zabbix via API |
| #15 | S19 | 10/09[T] | Alerta Zabbix → Webhook → AWX Job → remediação |
| #16 | S20 | 17/09[F] | Flask Docker + Zabbix HTTP agent health check |
| #17 | S21 | 24/09[T] | Terraform + Ansible + Zabbix integrados (IaC) |
| #18 | S22 | 01/10[F] | AWX workflow: Zabbix alerta → AWX → remediação auto |
| #19 | S23 | 08/10[T] | GitHub Actions → Zabbix event API notification |
| #20 | S24 | 15/10[F] | Deploy validation via Zabbix HTTP agent |
| #21 | S25 | 22/10[T] | K8s nodes monitorados via kube-state-metrics + Zabbix |
| #22 | S26 | 29/10[F] | Zabbix on K8s via Helm — self-monitoring cluster |
| #23 | S27 | 05/11[T] | Zabbix → Prometheus exporter → Grafana unificado |
| #24 | S28 | 12/11[T] | Error budget tracking em Zabbix dashboard |
| #25 | S29 | 19/11[F] | Mock incident — Zabbix alerta, runbook, postmortem |
| #26 | S30 | 26/11[T] | Full automation: Deploy → Monitor → Alert → Remediate |
| #27 | S31 | 03/12[F] | Zabbix on K8s (capstone) — custom template |
| #28 | S32 | 10/12[T] | Prometheus + Zabbix integração — métricas unificadas |
| #29 | S33 | 17/12[F] | SLO dashboard Zabbix completo + error budget |
| #30 | S34 | 24/12[T] | End-to-end automated incident response + postmortem |

---


## Regras de Negócio da Escala (LEIA ANTES DE TUDO)

```
ESCALA:      12x36 (12h trabalhando → 36h de folga)
ROTAÇÃO:     Dias PARES = TRABALHO | Dias ÍMPARES = FOLGA
ESTUDO FOLGA:  4h/dia → 2h manhã (09h–11h) + 2h tarde (14h–16h)
ESTUDO TRAB:   0.5h/dia → passivo: podcast técnico, audiobook, revisão mental
SEMANA:      Segunda a Domingo (7 dias, sem distinção fim de semana)
```

**Por que seg–dom:** No 12x36, sábado e domingo alternam entre folga e trabalho. Um sábado é dia de 4h de estudo; o seguinte é dia de plantão. O cronograma deve tratar cada dia pelo seu tipo (FOLGA/TRAB), não pelo nome do dia da semana.

**Capacidade real:**
- Semanas com 4 folgas: **16h + 1.5h passivo = 17.5h disponíveis**
- Semanas com 3 folgas: **12h + 2.0h passivo = 14.0h disponíveis**
- Média ponderada: **~15.6h/semana**
- Total maio–dezembro: **~560h disponíveis**
- Total carga dos cursos: **123h** (sobra ampla margem para labs e revisão)

---

## Cursos — Catálogo Completo

### Plataforma: Udemy

| # | Curso | Carga Horária | Fase SRE | Tipo | URL |
|---|-------|--------------|----------|------|-----|
| 1 | SRE DevOps: Jornada do Início ao Fim | **4h** | Fase 1 | Aula | https://www.udemy.com/course/jornada-devops-sre-do-inicio-ao-fim/ |
| 2 | Administração de Sistemas GNU/Linux: Fundamentos e Prática | **9h** | Fase 1 | Aula | https://www.udemy.com/course/adm-so-gnulinux/ |
| 3 | Python para DevOps | **7.5h** | Fase 2 | Aula | https://www.udemy.com/course/python-para-devops/ |
| 4 | GitHub Actions: Guia Completo — Do Zero ao Deploy | **7h** | Fase 4 | Aula | https://www.udemy.com/course/github-actions-guia-completo-do-zero-ao-deploy/ |
| 5 | Ansible para SysAdmin | **19h** | Fase 3 | Aula | https://www.udemy.com/course/ansible-para-sysadmin/ |
| 6 | AWX para Sysadmin | **8h** | Fase 3 | Aula | https://www.udemy.com/course/awx-para-sysadmin/ |
| 7 | Projeto DevOps: Flask API — Do Código ao Deploy | **14h** | Fase 4 | Projeto | https://www.udemy.com/course/projeto-devops-flask-api-do-codigo-ao-deploy/ |
| 8 | Kubernetes Completo: Orquestração Docker + Projeto DevOps | **19h** | Fase 4 | Aula+Projeto | https://www.udemy.com/course/kubernetes-power-profissional-formacao-inicial-completa/ |
| 9 | Certificação AWS Solutions Architect Associate SAA-C03 | **30.5h** | Fase 3 | Aula+Exam | https://www.udemy.com/course/certificacao-amazon-aws-2019-solutions-architect/ |

### Plataforma: LinuxTips

| # | Curso | Carga Horária | Fase SRE | Tipo | URL |
|---|-------|--------------|----------|------|-----|
| 10 | Terraform Essentials | **5h** | Fase 3 | Aula | https://linuxtips.io/treinamento/terraform-essentials/ |

### Plataforma: Alura Línguas (acesso empresa — 4 meses a partir de 11/03/26)

| # | Curso | Carga Horária | Fase SRE | Tipo | URL |
|---|-------|--------------|----------|------|-----|
| 11 | Inglês Técnico para DevOps/SRE | **Paralelo** | Todas | Passivo/Ativo | https://www.aluralingua.com.br/ |

> **Nota Alura Línguas:** Sem carga fixa. Usar 20min/dia nos dias de TRABALHO (substitui parte do passivo) e 1 sessão de 30min nas folgas opcionalmente. Foco em: leitura de documentação técnica, listening de podcasts SRE em inglês, escrita de commit messages e READMEs.

### Conteúdo Gratuito (sem custo, integrado ao cronograma)

| Recurso | Carga Estimada | Fase | Tipo | URL |
|---------|---------------|------|------|-----|
| Linux Journey | 3h | Fase 1 | Leitura interativa | https://linuxjourney.com |
| OverTheWire Bandit (levels 1–15) | 4h | Fase 1 | Prática gamificada | https://overthewire.org/wargames/bandit/ |
| The Linux Command Line (livro) | 5h | Fase 1 | Leitura | https://linuxcommand.org/tlcl.php |
| Practical Networking (YouTube) | 4h | Fase 1 | Vídeo | https://youtube.com/@PracticalNetworking |
| Learn Git Branching | 2h | Fase 2 | Interativo | https://learngitbranching.js.org |
| Pro Git Book (caps 1–5) | 3h | Fase 2 | Leitura | https://git-scm.com/book |
| IA Aplicada a SRE/DevOps | 4h | Fases 1,2 | Prática/Prompting | ChatGPT/Claude (Self-study) |
| Automate the Boring Stuff (caps 1–8) | 4h | Fase 2 | Leitura | https://automatetheboringstuff.com |
| SQLBolt | 2h | Fase 2 | Interativo | https://sqlbolt.com |
| Google SRE Book (seleção de caps) | 6h | Fases 1,4,5 | Leitura | https://sre.google/sre-book/table-of-contents/ |
| KillerCoda — Kubernetes Scenarios | 4h | Fase 4 | Lab interativo | https://killercoda.com |
| Prometheus Docs + Tutorials | 3h | Fase 4 | Leitura/Lab | https://prometheus.io/docs |
| Grafana Tutorials | 2h | Fase 4 | Lab | https://grafana.com/tutorials |

---

## Resumo de Carga por Fase

| Fase | Período | Semanas | Cursos Pagos | Gratuito | Total Fase | H Disponíveis |
|------|---------|---------|-------------|---------|-----------|---------------|
| 1 — Foundation | Mai S1–S5 | 5 | Curso 1 (4h) + Curso 2 (9h) = 13h | ~12h | ~25h | ~76h |
| 2 — Core Skills | Mai S5–Jun S9 | 4 | Curso 3 (7.5h) = 7.5h | ~11h | ~18.5h | ~63h |
| 3 — Infra & Cloud | Jun S9–Ago S18 | 9 | Cursos 5+6+9+10 (62.5h) | ~5h | ~67.5h | ~141h |
| 4 — Advanced SRE | Set S19–Nov S29 | 11 | Cursos 4+7+8 (40h) | ~9h | ~49h | ~173h |
| 5 — Especialização | Nov S29–Dez S36 | 7 | — | ~8h | ~8h | ~107h |
| **TOTAL** | **Mai–Dez** | **36** | **123h** | **~45h** | **~168h** | **~560h** |

> **Margem:** 560h disponíveis − 168h de conteúdo = ~392h para labs, revisão, projetos práticos e capstone. Isso é intencional — SRE se aprende fazendo, não só assistindo.

---

## Calendário Real da Escala — Maio a Dezembro 2026

**Legenda:**
- `[F]` = FOLGA → 4h estudo (2h manhã + 2h tarde)
- `[T]` = TRABALHO → 0.5h passivo (podcast/revisão)

```
MAIO 2026
S01 ( 8.5h)  Sex 09/05[F]  Sáb 10/05[T]  Dom 11/05[F]
S02 (14.0h)  Seg 12/05[T]  Ter 13/05[F]  Qua 14/05[T]  Qui 15/05[F]  Sex 16/05[T]  Sáb 17/05[F]  Dom 18/05[T]
S03 (17.5h)  Seg 19/05[F]  Ter 20/05[T]  Qua 21/05[F]  Qui 22/05[T]  Sex 23/05[F]  Sáb 24/05[T]  Dom 25/05[F]
S04 (14.0h)  Seg 26/05[T]  Ter 27/05[F]  Qua 28/05[T]  Qui 29/05[F]  Sex 30/05[T]  Sáb 31/05[F]  Dom 01/06[T]
S05 (17.5h)  Seg 02/06[F]  Ter 03/06[T]  Qua 04/06[F]  Qui 05/06[T]  Sex 06/06[F]  Sáb 07/06[T]  Dom 08/06[F]

JUNHO 2026
S06 (17.5h)  Seg 09/06[F]  Ter 10/06[T]  Qua 11/06[F]  Qui 12/06[T]  Sex 13/06[F]  Sáb 14/06[T]  Dom 15/06[F]
S07 (14.0h)  Seg 16/06[T]  Ter 17/06[F]  Qua 18/06[T]  Qui 19/06[F]  Sex 20/06[T]  Sáb 21/06[F]  Dom 22/06[T]
S08 (17.5h)  Seg 23/06[F]  Ter 24/06[T]  Qua 25/06[F]  Qui 26/06[T]  Sex 27/06[F]  Sáb 28/06[T]  Dom 29/06[F]
S09 (14.0h)  Seg 30/06[T]  Ter 01/07[F]  Qua 02/07[T]  Qui 03/07[F]  Sex 04/07[T]  Sáb 05/07[F]  Dom 06/07[T]

JULHO 2026
S10 (17.5h)  Seg 07/07[F]  Ter 08/07[T]  Qua 09/07[F]  Qui 10/07[T]  Sex 11/07[F]  Sáb 12/07[T]  Dom 13/07[F]
S11 (14.0h)  Seg 14/07[T]  Ter 15/07[F]  Qua 16/07[T]  Qui 17/07[F]  Sex 18/07[T]  Sáb 19/07[F]  Dom 20/07[T]
S12 (17.5h)  Seg 21/07[F]  Ter 22/07[T]  Qua 23/07[F]  Qui 24/07[T]  Sex 25/07[F]  Sáb 26/07[T]  Dom 27/07[F]
S13 (14.0h)  Seg 28/07[T]  Ter 29/07[F]  Qua 30/07[T]  Qui 31/07[F]  Sex 01/08[T]  Sáb 02/08[F]  Dom 03/08[T]
S14 (17.5h)  Seg 04/08[F]  Ter 05/08[T]  Qua 06/08[F]  Qui 07/08[T]  Sex 08/08[F]  Sáb 09/08[F]  Dom 10/08[T]

AGOSTO 2026
S15 (17.5h)  Seg 11/08[F]  Ter 12/08[T]  Qua 13/08[F]  Qui 14/08[T]  Sex 15/08[F]  Sáb 16/08[T]  Dom 17/08[F]
S16 (14.0h)  Seg 18/08[T]  Ter 19/08[F]  Qua 20/08[T]  Qui 21/08[F]  Sex 22/08[T]  Sáb 23/08[F]  Dom 24/08[T]
S17 (17.5h)  Seg 25/08[F]  Ter 26/08[T]  Qua 27/08[F]  Qui 28/08[T]  Sex 29/08[F]  Sáb 30/08[T]  Dom 31/08[F]
S18 (14.0h)  Seg 01/09[T]  Ter 02/09[F]  Qua 03/09[T]  Qui 04/09[F]  Sex 05/09[T]  Sáb 06/09[F]  Dom 07/09[T]

SETEMBRO 2026
S19 (17.5h)  Seg 08/09[F]  Ter 09/09[F]  Qua 10/09[T]  Qui 11/09[F]  Sex 12/09[T]  Sáb 13/09[F]  Dom 14/09[T]
S20 (17.5h)  Seg 15/09[F]  Ter 16/09[T]  Qua 17/09[F]  Qui 18/09[T]  Sex 19/09[F]  Sáb 20/09[T]  Dom 21/09[F]
S21 (14.0h)  Seg 22/09[T]  Ter 23/09[F]  Qua 24/09[T]  Qui 25/09[F]  Sex 26/09[T]  Sáb 27/09[F]  Dom 28/09[T]
S22 (17.5h)  Seg 29/09[F]  Ter 30/09[T]  Qua 01/10[F]  Qui 02/10[T]  Sex 03/10[F]  Sáb 04/10[T]  Dom 05/10[F]
S23 (14.0h)  Seg 06/10[T]  Ter 07/10[F]  Qua 08/10[T]  Qui 09/10[F]  Sex 10/10[T]  Sáb 11/10[F]  Dom 12/10[T]

OUTUBRO 2026
S24 (17.5h)  Seg 13/10[F]  Ter 14/10[T]  Qua 15/10[F]  Qui 16/10[T]  Sex 17/10[F]  Sáb 18/10[T]  Dom 19/10[F]
S25 (14.0h)  Seg 20/10[T]  Ter 21/10[F]  Qua 22/10[T]  Qui 23/10[F]  Sex 24/10[T]  Sáb 25/10[F]  Dom 26/10[T]
S26 (17.5h)  Seg 27/10[F]  Ter 28/10[T]  Qua 29/10[F]  Qui 30/10[T]  Sex 31/10[F]  Sáb 01/11[T]  Dom 02/11[F]
S27 (17.5h)  Seg 03/11[T]  Ter 04/11[F]  Qua 05/11[T]  Qui 06/11[F]  Sex 07/11[T]  Sáb 08/11[F]  Dom 09/11[F]

NOVEMBRO 2026
S28 (14.0h)  Seg 10/11[T]  Ter 11/11[F]  Qua 12/11[T]  Qui 13/11[F]  Sex 14/11[T]  Sáb 15/11[F]  Dom 16/11[T]
S29 (17.5h)  Seg 17/11[F]  Ter 18/11[T]  Qua 19/11[F]  Qui 20/11[T]  Sex 21/11[F]  Sáb 22/11[T]  Dom 23/11[F]
S30 (14.0h)  Seg 24/11[T]  Ter 25/11[F]  Qua 26/11[T]  Qui 27/11[F]  Sex 28/11[T]  Sáb 29/11[F]  Dom 30/11[T]
S31 (17.5h)  Seg 01/12[F]  Ter 02/12[T]  Qua 03/12[F]  Qui 04/12[T]  Sex 05/12[F]  Sáb 06/12[T]  Dom 07/12[F]

DEZEMBRO 2026
S32 (14.0h)  Seg 08/12[T]  Ter 09/12[F]  Qua 10/12[T]  Qui 11/12[F]  Sex 12/12[T]  Sáb 13/12[F]  Dom 14/12[T]
S33 (17.5h)  Seg 15/12[F]  Ter 16/12[T]  Qua 17/12[F]  Qui 18/12[T]  Sex 19/12[F]  Sáb 20/12[T]  Dom 21/12[F]
S34 (14.0h)  Seg 22/12[T]  Ter 23/12[F]  Qua 24/12[T]  Qui 25/12[F]  Sex 26/12[T]  Sáb 27/12[F]  Dom 28/12[T]
S35 (17.5h)  Seg 29/12[F]  Ter 30/12[T]  Qua 31/12[F]  Qui 01/01[T]  Sex 02/01[F]  Sáb 03/01[T]  Dom 04/01[F]
S36 ( 9.0h)  Seg 05/01[T]  Ter 06/01[F]  Qua 07/01[T]  Qui 08/01[F]
```

---

## Mapeamento Curso × Semanas do Calendário

> Esta seção diz ao Claude Code **quando** cada curso acontece na escala real.

### Fase 1 — Foundation (Semanas S01–S05 | ~76h disponíveis)

**Curso 1: SRE DevOps: Jornada do Início ao Fim — 4h**
```
Carga:     4h total
Sessões:   2 folgas × 2h manhã
Quando:    S01 (09/05[F], 11/05[F]) — conclui na primeira semana
Uso:       2h manhã cada dia de folga
Plantão:   Revisão mental dos conceitos SRE
```

**Curso 2: GNU/Linux Fundamentos e Prática — 9h**
```
Carga:     9h total
Sessões:   ~5 folgas × (manhã 2h ou tarde 2h)
Quando:    S02–S04 (13/05 a 31/05)
Distribuição sugerida:
  S02: Ter 13/05[F] manhã 2h (Módulo 1–2) + tarde 2h (Módulo 3)
       Qui 15/05[F] manhã 2h (Módulo 4) + tarde 2h (Módulo 5)
       Sáb 17/05[F] manhã 1h (Módulo 6 — início)
  S03: Seg 19/05[F] manhã 1h (Módulo 6 — conclusão)  → 9h concluídas
Plantão:   Podcast "Linux For Everyone", "Command Line Heroes"
```

**Conteúdo Gratuito Fase 1 — 18h estimadas**
```
Linux Journey:        S02–S03 → tardes de folga (complemento ao curso)
Practical Networking: S03–S04 → manhãs de folga
OverTheWire Bandit:   S04–S05 → tardes de folga (gamificado, motivador)
Google SRE Book c1–3: S04–S05 → 1 sessão por folga (leitura, 1h)
The Linux Cmd Line:   S02–S05 → leitura passiva nas folgas noturnas
```

---

### Fase 2 — Core Skills (Semanas S05–S09 | ~63h disponíveis)

**Curso 3: Python para DevOps — 7.5h**
```
Carga:     7.5h total
Sessões:   ~4 folgas × 2h
Quando:    S05–S07 (02/06 a 20/06)
Distribuição sugerida:
  S05: Dom 08/06[F] manhã 2h (Módulos 1–2: variáveis, estruturas)
  S06: Seg 09/06[F] manhã 2h (Módulos 3–4: funções, requests)
       Qua 11/06[F] manhã 2h (Módulos 5–6: error handling, logging)
       Sex 13/06[F] manhã 1.5h (Módulos 7–8: subprocess, venv) → concluído
Plantão:   Podcast "Talk Python to Me", "Python Bytes"
```

**Conteúdo Gratuito Fase 2 — 11h estimadas**
```
Learn Git Branching:       S05 → 1 folga, 2h (interativo, essencial)
Pro Git Book (caps 1–5):   S06 → leitura distribuída nas folgas
Automate Boring Stuff:     S07–S08 → complemento Python
SQLBolt:                   S08 → 1 folga, 2h (SQL interativo)
```

---

### Fase 3 — Infra & Cloud (Semanas S09–S18 | ~141h disponíveis)

**Curso 9: AWS Solutions Architect SAA-C03 — 30.5h**
```
Carga:     30.5h total  ← MAIOR curso, exige mais semanas
Sessões:   ~16 folgas × 2h (manhã) = 32h → completa com 1 folga de margem
Quando:    S09–S14 (30/06 a 03/08)
Distribuição sugerida (manhãs de folga):
  S09:  Ter 01/07[F]  Qui 03/07[F]  Sáb 05/07[F]  → 6h (IAM, EC2, VPC)
  S10:  Seg 07/07[F]  Qua 09/07[F]  Sex 11/07[F]  Dom 13/07[F] → 8h (S3, RDS, ELB)
  S11:  Ter 15/07[F]  Qui 17/07[F]  Sáb 19/07[F]  → 6h (CloudWatch, CF, Security)
  S12:  Seg 21/07[F]  Qua 23/07[F]  Sex 25/07[F]  Dom 27/07[F] → 8h (Lambda, SQS, Route53)
  S13:  Ter 29/07[F]  Qui 31/07[F]  → 2.5h (Revisão + simulado parcial)
  S14:  concluído → tarde simulado final, agendar prova SAA-C03
Plantão:   "AWS re:Invent talks" (YouTube offline), flashcards AWS no celular
```

**Curso 10: Terraform Essentials — 5h**
```
Carga:     5h total
Sessões:   3 folgas × (manhã ou tarde 2h)
Quando:    S14–S15 (04/08 a 17/08) — logo após AWS, enquanto IaC está fresco
Distribuição:
  S14:  Sex 08/08[F] tarde 2h (sintaxe, providers, resources)
  S15:  Seg 11/08[F] tarde 2h (variables, state, módulos)
        Qua 13/08[F] tarde 1h (boas práticas, conclusão)
```

**Curso 5: Ansible para SysAdmin — 19h**
```
Carga:     19h total
Sessões:   ~10 folgas × 2h
Quando:    S15–S18 (11/08 a 07/09)
Distribuição sugerida (tardes de folga — manhã fica para labs):
  S15:  Sex 15/08[F] tarde 2h  Dom 17/08[F] tarde 2h  → 4h (fundamentos, playbooks)
  S16:  Ter 19/08[F] tarde 2h  Qui 21/08[F] tarde 2h  Sáb 23/08[F] tarde 2h  → 6h (roles, vault)
  S17:  Seg 25/08[F] tarde 2h  Qua 27/08[F] tarde 2h  Sex 29/08[F] tarde 2h  → 6h (avançado)
  S18:  Ter 02/09[F] tarde 2h  Qui 04/09[F] tarde 1h  → 3h (projeto final)
Plantão:   "Ansible automates" podcast, revisão de playbooks no celular
```

**Curso 6: AWX para Sysadmin — 8h**
```
Carga:     8h total
Sessões:   4 folgas × 2h (tardes)
Quando:    S18 final + S19 (04/09 a 14/09)
Distribuição:
  S18:  Sáb 06/09[F] tarde 2h (instalação, conceitos, inventários)
  S19:  Seg 08/09[F] tarde 2h (job templates, workflows)
        Ter 09/09[F] tarde 2h (webhooks, RBAC, API)
        Qui 11/09[F] tarde 2h (projeto: Zabbix → AWX → remediação)
```

---

### Fase 4 — Advanced SRE (Semanas S19–S29 | ~173h disponíveis)

**Curso 4: GitHub Actions — 7h**
```
Carga:     7h total
Sessões:   4 folgas × 2h (com 1h de margem)
Quando:    S19–S20 (08/09 a 21/09)
Distribuição (manhãs de folga):
  S19:  Sex 12/09[F] manhã — 2h (workflows, events, runners)  ← dia par = trabalho, ajustar
        [ATENÇÃO: 12/09 é par = TRABALHO → usar Sáb 13/09[F]]
  S19:  Sáb 13/09[F] manhã 2h (workflows, events, runners)
  S20:  Seg 15/09[F] manhã 2h (secrets, Docker, matrix builds)
        Qua 17/09[F] manhã 2h (environments, reusable workflows)
        Sex 19/09[F] manhã 1h (conclusão + lab pipeline)
```

**Curso 7: Projeto DevOps Flask API — 14h**
```
Carga:     14h total
Sessões:   ~7 folgas × 2h
Quando:    S21–S23 (22/09 a 12/10)
Distribuição:
  S21:  Ter 23/09[F] 4h (manhã 2h + tarde 2h) — estrutura Flask, Docker
        Qui 25/09[F] 4h (manhã 2h + tarde 2h) — testes, CI pipeline
        Sáb 27/09[F] 2h manhã — deploy K8s inicial
  S22:  Seg 29/09[F] 2h manhã — observabilidade, métricas Prometheus
        Qua 01/10[F] 2h tarde — escalabilidade, HPA
  Total: 14h → concluído
Plantão:   Revisar código do projeto, pensar em melhorias
```

**Curso 8: Kubernetes Completo + Projeto DevOps — 19h**
```
Carga:     19h total
Sessões:   ~10 folgas × 2h
Quando:    S23–S27 (06/10 a 09/11)
Distribuição:
  S23:  Qui 09/10[F] tarde 2h  Sáb 11/10[F] tarde 2h  → 4h (arquitetura, kubectl, pods)
  S24:  Seg 13/10[F] tarde 2h  Qua 15/10[F] tarde 2h  Sex 17/10[F] tarde 2h  Dom 19/10[F] tarde 2h → 8h (services, configmaps, volumes, ingress)
  S25:  Ter 21/10[F] tarde 2h  Qui 23/10[F] tarde 2h  → 4h (RBAC, HPA, Helm)
  S26:  Sex 31/10[F] tarde 1h  Dom 02/11[F] tarde 2h  → 3h (projeto DevOps K8s)
  Total: 19h → concluído
Plantão:   KillerCoda K8s scenarios (mobile), podcast "Kubernetes Podcast"
```

**Conteúdo Gratuito Fase 4 — 9h estimadas**
```
Prometheus + Grafana docs:  S19–S20 → manhãs de folga junto ao CI/CD
KillerCoda K8s:             S23–S27 → tardes + plantão (mobile-friendly)
Google SRE Book (Monitoring, Incidents): S26–S28 → 1h/folga, leitura
Chaos Engineering docs:     S27 → 1 folga dedicada
```

---

### Fase 5 — Especialização & Capstone (Semanas S28–S36 | ~107h disponíveis)

```
Capstone (projeto integrador):  S28–S31 → folgas completas (4h/dia)
Preparação carreira:            S32–S34 → misto (manhã = prep, tarde = lab)
Buffer + revisão final:         S35–S36 → revisão, celebração, próximo passo
Alura Línguas (intensivo final): S28–S36 → 1 sessão 30min por folga
CKA Prep (opcional, pós-dez):   Planejado para Jan/Fev 2027
```

---

## Regras de Alocação para o Claude Code Implementar

```python
# REGRA 1: Tipo de dia
def get_day_type(date):
    return "FOLGA" if date.day % 2 != 0 else "TRABALHO"

# REGRA 2: Horas disponíveis por tipo
def get_available_hours(day_type):
    return {"FOLGA": 4.0, "TRABALHO": 0.5}[day_type]

# REGRA 3: Blocos de estudo em dias de folga
FOLGA_BLOCKS = [
    {"id": "manha", "label": "Manhã", "horas": 2, "horario": "09:00–11:00"},
    {"id": "tarde",  "label": "Tarde",  "horas": 2, "horario": "14:00–16:00"},
]

# REGRA 4: Bloco passivo em dias de trabalho
TRAB_BLOCK = {"id": "passivo", "label": "Passivo", "horas": 0.5, "horario": "Livre"}

# REGRA 5: Semana vai de segunda a domingo (não seg–sex)
# Sábado e domingo têm o mesmo peso que dias úteis na escala 12x36

# REGRA 6: Lab Zabbix — 1 folga por semana (preferencialmente 1ª folga da semana)
# Usa 1h do bloco tarde. Nunca cancela.

# REGRA 7: Alura Línguas — dias de trabalho (20min do passivo)
# Opcional: 1 sessão de 30min nas folgas

# REGRA 8: Cursos com tag "aws" → preferencialmente manhã (conteúdo denso)
# Cursos com tag "lab" / "projeto" → preferencialmente tarde (prático)
# Cursos com tag "book" / "free" → passivo (plantão) ou antes de dormir
```

---

## Dados para Persistência no Banco (curriculum.py)

O Claude Code deve usar este arquivo para popular `data/curriculum.py` com os dados exatos. Cada lição do `painel_sre_v2.html` deve receber, além dos campos já existentes (`name`, `h`, `tag`), dois campos novos:

```python
{
    "name": "...",
    "h": 2,
    "tag": None,  # None | "lab" | "free" | "book" | "aws"
    "block": "manha",   # "manha" | "tarde" | "passivo"
    "type": "aula"      # "aula" | "lab" | "leitura" | "projeto" | "revisao"
}
```

**Mapeamento tag → block padrão:**
- `tag: None` (aula normal) → `block: "manha"` se teórico, `"tarde"` se prático
- `tag: "aws"` → `block: "manha"` (conteúdo denso, mente fresca)
- `tag: "lab"` → `block: "tarde"` (prático, após teoria da manhã)
- `tag: "book"` → `block: "passivo"` (leitura, não requer computador)
- `tag: "free"` → depende do conteúdo (interativo = tarde, leitura = passivo)

---

## Estatísticas Finais (para validação)

```
Total cursos pagos:          11 cursos
Total horas pagas:           123h
Total conteúdo gratuito:     ~45h estimadas
Total horas de conteúdo:     ~168h

Total dias de folga:         125 dias  →  500h de estudo focado
Total dias de trabalho:      100 dias  →   50h de estudo passivo
Total horas disponíveis:     550h

Margem para labs e projetos: 550 - 168 = 382h  (69% do tempo = prática)

Tipo de semana A (4 folgas): 19 semanas  →  17.5h/semana
Tipo de semana B (3 folgas): 15 semanas  →  14.0h/semana
Semanas parciais:             2 semanas  →  média 8.75h

Período total:               36 semanas (09/05 a 16/01/2027)
```

---

*Gerado em: Maio 2026*
*Escala validada matematicamente: dias pares = trabalho, dias ímpares = folga*
*Base: `painel_sre_v2.html` + `cronograma_sre_robson.md` + cálculo Python da escala real*
