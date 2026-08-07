# Catálogo e Trilha de Estudos SRE — Robson Santiago

**Objetivo profissional:** transição de Analista de Monitoramento para SRE ou DevOps remoto  
**Escala de referência:** 12x36  
**Data-base da escala:** 05/08/2026 = FOLGA; 06/08/2026 = TRABALHO  
**Versão:** 3.0 — catálogo dinâmico, sem prazo final fixo

---

## Estado de implementação

O catálogo descrito neste documento está materializado por `COURSES` e `ACTIVITIES`
em `data/curriculum.py`. O serviço de seed sincroniza esses registros de forma
idempotente com as tabelas `courses` e `activities`.

A ordem pedagógica é representada pelo campo `sequence`; datas e slots são
responsabilidade dos serviços de escala e scheduling. `WEEKS` não deve ser usado
para criar novas alocações.

---

## 1. Finalidade deste arquivo

Este arquivo define:

- os cursos e recursos aprovados para a trilha;
- a ordem pedagógica recomendada;
- os pré-requisitos entre competências;
- a prioridade de cada conteúdo;
- quais cursos devem ser feitos integralmente ou seletivamente;
- os projetos usados para comprovar aprendizado;
- as trilhas paralelas de AWS e Google Cloud.

Este arquivo **não define datas fixas para cada aula**.

Datas, horários, reagendamentos e slots da escala 12x36 devem ser gerenciados dinamicamente pela aplicação. Uma atividade não concluída deve voltar para a fila e ocupar um próximo slot compatível, sem reescrever todo o roadmap.

---

## 2. Regras pedagógicas

### 2.1 Uma trilha principal por vez

A aplicação deve manter no máximo:

1. **uma trilha principal do roadmap SRE**;
2. **uma trilha paralela obrigatória**, enquanto existir:
   - AWS re/Start e Canvas;
   - Google Cloud Skills, em frequência controlada.

Não iniciar dois cursos técnicos principais simultaneamente.

### 2.2 Aprendizado orientado a prática

Cada curso deve gerar ao menos um dos seguintes resultados:

- laboratório versionado;
- script;
- documentação;
- dashboard;
- pipeline;
- infraestrutura reproduzível;
- runbook;
- post-mortem;
- projeto de portfólio.

Concluir videoaulas sem prática não representa domínio da competência.

### 2.3 Critério para avançar

Uma competência pode ser considerada consolidada quando o aluno consegue:

- explicar os conceitos principais;
- executar uma atividade sem copiar integralmente a aula;
- diagnosticar erros básicos;
- documentar o procedimento;
- aplicar o conteúdo em um projeto próprio.

### 2.4 Revisão

Após cada curso principal:

- realizar uma sessão de revisão;
- finalizar o laboratório;
- atualizar o README do projeto;
- registrar dificuldades e pontos que precisam de reforço.

---

## 3. Capacidade de estudo na escala 12x36

### Dia de folga

Carga mínima do roadmap: **2 horas**, divididas em quatro blocos de 30 minutos.

Slots preferenciais:

| Slot | Horário sugerido | Uso |
|---|---|---|
| F1 | 13h30–14h00 | teoria |
| F2 | 14h10–14h40 | teoria ou exercício |
| F3 | 15h20–15h50 | laboratório |
| F4 | 16h00–16h30 | laboratório, revisão ou AWS |

Slot opcional:

| Slot | Horário sugerido | Uso |
|---|---|---|
| FX | espera do ônibus, aproximadamente 30 min | leitura, flashcards ou revisão leve |

### Dia de trabalho

Carga mínima: **1 hora**, dividida em dois blocos de 30 minutos.

| Slot | Horário sugerido | Uso |
|---|---|---|
| T1 | 7h00–7h30 | curso principal |
| T2 | intervalo de almoço | revisão, AWS ou leitura |

O período noturno de dias de trabalho não deve ser utilizado para compensar estudos perdidos. A prioridade é preservar o sono.

### Regra matemática da escala

```python
from datetime import date

SCALE_ANCHOR = date(2026, 8, 5)  # FOLGA

def get_day_type(current_date: date) -> str:
    days = (current_date - SCALE_ANCHOR).days
    return "FOLGA" if days % 2 == 0 else "TRABALHO"
```

Não usar regras mensais de dias pares ou ímpares.

---

## 4. Estados de uma atividade

A aplicação deverá aceitar:

| Status | Significado |
|---|---|
| `pending` | ainda não iniciada |
| `in_progress` | iniciada e não concluída |
| `done` | concluída |
| `deferred` | adiada e devolvida à fila |
| `skipped` | retirada conscientemente da trilha |
| `blocked` | depende de pré-requisito, recurso ou correção |
| `cancelled` | removida definitivamente |

### Comportamento de “não feito”

“Não feito” deve ser registrado como `deferred`.

A atividade:

1. mantém seu ID permanente;
2. registra o histórico do slot perdido;
3. volta para a fila;
4. recebe o próximo slot compatível;
5. não altera as atividades já concluídas;
6. não exige recalcular um prazo final fixo.

---

# 5. Roadmap principal

## Fase 1 — Fundamentos operacionais

### 1. Administração de Sistemas GNU/Linux: Fundamentos e Prática

- **Plataforma:** Udemy
- **Carga de vídeo:** 9h11
- **Prioridade:** muito alta
- **Execução:** integral, acelerando conteúdos já dominados
- **Objetivo:** consolidar terminal, arquivos, permissões, usuários, processos, manipulação de texto e Shell Script.
- **URL:** https://www.udemy.com/course/adm-so-gnulinux/

Conteúdo prioritário:

- pipes e redirecionamentos;
- `grep`, `awk`, `sed` e expressões regulares;
- usuários, grupos, `sudoers` e permissões;
- processos;
- Shell Script;
- inventário do sistema.

Complementos necessários:

- systemd e journald;
- performance;
- armazenamento;
- redes;
- troubleshooting.

Projeto:

```text
linux-sre-toolkit/
├── check_cpu.sh
├── check_memory.sh
├── check_disk.sh
├── check_process.sh
├── check_port.sh
├── analyze_log.sh
└── README.md
```

---

### 2. Fundamentos de Redes para DevOps

- **Situação:** curso ainda não adquirido
- **Prioridade de compra:** alta
- **Objetivo:** TCP/IP, DNS, HTTP/HTTPS, TLS, roteamento, NAT, sockets e troubleshooting.
- **Ferramentas esperadas:** `ip`, `ss`, `dig`, `curl`, `mtr`, `tcpdump`, `nc`, `openssl`.

Este é o principal conteúdo ainda ausente na coleção atual.

Projeto:

- diagnosticar DNS, HTTP, TLS e conectividade;
- produzir um runbook de troubleshooting de rede;
- capturar e interpretar tráfego básico com `tcpdump`.

---

### 3. Git e GitHub

- **Situação:** usar recursos gratuitos inicialmente
- **Prioridade:** alta
- **Recursos:**
  - GitHub Skills;
  - Learn Git Branching;
  - Pro Git, capítulos iniciais.

Conteúdo mínimo:

- commits;
- branches;
- merge e rebase;
- resolução de conflitos;
- pull requests;
- tags;
- `.gitignore`;
- revisão de código;
- commits claros.

Comprar um curso específico apenas se houver dificuldade prática persistente.

---

### 4. Introdução a Bancos de Dados e Linguagem SQL

- **Plataforma:** Udemy
- **Carga de vídeo:** 1h58
- **Prioridade:** média
- **Execução:** integral
- **URL:** https://www.udemy.com/course/introducao-a-bancos-de-dados-e-linguagem-sql/

Objetivo:

- compreender banco relacional;
- criar tabelas;
- inserir e consultar dados;
- usar filtros e `JOIN`;
- apoiar automações e troubleshooting.

Projeto:

```text
incident-database/
├── schema.sql
├── seed.sql
├── queries.sql
└── README.md
```

Tabelas sugeridas:

- serviços;
- incidentes;
- alertas;
- equipes.

---

### 5. Python para DevOps

- **Plataforma:** Udemy
- **Carga de vídeo:** 7h18
- **Prioridade:** alta
- **Execução:** integral, retomando projetos conforme os pré-requisitos
- **URL:** https://www.udemy.com/course/python-para-devops/

Conteúdo principal:

- fundamentos de Python;
- funções e tratamento de erros;
- type hints;
- YAML;
- logging;
- CLI;
- Kubernetes Python SDK;
- FastAPI;
- roteamento de alertas.

Complementos:

- `pytest`;
- mocks;
- `requests`/`httpx`;
- retries, timeout e backoff;
- empacotamento;
- Boto3;
- métricas da própria automação.

Projeto principal:

```text
alert-router/
Zabbix ou Alertmanager
→ FastAPI
→ classificação
→ Telegram, e-mail ou Discord
→ logs estruturados
→ métricas Prometheus
```

---

## Fase 2 — Containers, cloud e infraestrutura como código

### 6. Docker

- **Situação:** curso dedicado ainda não adquirido
- **Prioridade de compra:** alta
- **Objetivo:** imagens, containers, Dockerfiles, volumes, redes, Compose, segurança e troubleshooting.

Os cursos integradores existentes usam Docker, mas não substituem uma formação estruturada.

Projeto:

- containerizar uma API;
- criar ambiente com Docker Compose;
- usar volumes e redes;
- implementar health check;
- reduzir tamanho e superfície de ataque da imagem.

---

### 7. AWS re/Start — Campinho Digital

- **Situação:** em andamento
- **Tipo:** trilha paralela obrigatória
- **Horário:** aulas 19h00–20h20 e módulos no Canvas
- **Objetivo:** fundamentos operacionais de AWS e preparação para a trilha de cloud.

Regras:

- contabilizar a carga do re/Start dentro do estudo total;
- não acumular Canvas, roadmap e Google Skills na mesma noite;
- tarefas obrigatórias têm prioridade sobre revisões opcionais.

---

### 8. Preparatório AWS Cloud Practitioner CLF-C02

- **Plataforma:** Cloud Basics Academy
- **Carga:** 11h24
- **Prioridade:** baixa
- **Execução:** seletiva
- **URL:** https://cloudbasics.academy/plataforma/cursos/2732

Uso recomendado:

- nivelamento;
- infraestrutura global;
- responsabilidade compartilhada;
- IAM;
- custos;
- CloudWatch, CloudTrail e AWS Config.

Não é necessário realizar a certificação CLF-C02 antes da SAA-C03.

Carga sugerida: 6 a 8 horas.

---

### 9. AWS Solutions Architect Associate SAA-C03

- **Plataforma:** Udemy
- **Carga de vídeo:** 30h31
- **Prioridade:** muito alta
- **Execução:** integral
- **URL:** https://www.udemy.com/course/certificacao-amazon-aws-2019-solutions-architect/

Objetivo:

- arquitetura segura;
- resiliência;
- desempenho;
- custos;
- IAM;
- VPC;
- EC2;
- S3;
- bancos;
- alta disponibilidade;
- disaster recovery.

A certificação é recomendada após laboratórios e simulados.

Projetos:

1. aplicação web altamente disponível;
2. VPC com subnets públicas e privadas;
3. arquitetura com RTO e RPO documentados;
4. infraestrutura recriada posteriormente com Terraform.

Controle obrigatório:

- budgets;
- alertas;
- destruição dos recursos;
- conferência de EBS, IPs e load balancers.

---

### 10. Terraform Essentials

- **Plataforma:** LinuxTips
- **Carga:** mais de 5 horas
- **Prioridade:** alta
- **Execução:** integral
- **URL:** https://linuxtips.io/treinamento/terraform-essentials/

Conteúdo:

- HCL;
- providers;
- recursos;
- variáveis;
- state;
- backend;
- módulos;
- workspaces;
- importação;
- dados sensíveis.

Complementos:

- outputs, locals e data sources;
- `for_each`;
- lifecycle;
- locking;
- múltiplos ambientes;
- `terraform test`;
- segurança;
- CI/CD;
- drift.

Projeto:

```text
terraform-aws-lab/
├── modules/
├── environments/
├── backend/
└── README.md
```

---

### 11. Ansible para SysAdmin

- **Plataforma:** Udemy
- **Carga de vídeo:** 18h56
- **Prioridade:** alta
- **Execução:** integral
- **URL:** https://www.udemy.com/course/ansible-para-sysadmin/

Conteúdo:

- inventários;
- playbooks;
- variables;
- handlers;
- conditions;
- loops;
- templates;
- roles;
- Galaxy;
- Collections;
- Vault;
- Linux e Windows;
- inventário dinâmico AWS.

Complementos:

- `ansible-lint`;
- Molecule;
- CI/CD;
- observabilidade;
- rollback;
- AWX.

Projeto:

- configurar VMs Linux;
- instalar Docker, Nginx e Zabbix Agent;
- separar ambientes;
- validar idempotência;
- usar Ansible Vault.

---

## Fase 3 — CI/CD e orquestração

### 12. GitHub Actions: Guia Completo — Do Zero ao Deploy

- **Plataforma:** Udemy
- **Carga:** 7h07
- **Prioridade:** alta
- **Execução:** integral, dividida por pré-requisitos
- **URL:** https://www.udemy.com/course/github-actions-guia-completo-do-zero-ao-deploy/

Conteúdo:

- workflows;
- jobs e steps;
- triggers;
- conditions;
- contexts;
- secrets;
- environments;
- matrix;
- Python;
- Docker;
- Terraform;
- Kubernetes.

Complementos:

- reusable workflows;
- composite actions;
- cache;
- artifacts;
- concurrency;
- self-hosted runners;
- OIDC;
- proteção de produção.

Projeto:

```text
pull request
→ lint
→ testes
→ análise de segurança
→ build
→ scan
→ push
→ deploy em homologação
→ aprovação
→ produção
```

---

### 13. Kubernetes Completo: Orquestração Docker + Projeto DevOps

- **Plataforma:** Udemy
- **Carga:** 18h51
- **Prioridade:** muito alta
- **Execução:** integral
- **URL:** https://www.udemy.com/course/kubernetes-power-profissional-formacao-inicial-completa/

Conteúdo:

- arquitetura;
- Pods;
- ReplicaSets;
- Deployments;
- Services;
- Namespaces;
- probes;
- requests e limits;
- volumes;
- DaemonSets;
- Jobs;
- CronJobs;
- ConfigMaps;
- Secrets;
- StatefulSets;
- EndpointSlices;
- RBAC.

Complementos:

- Readiness e Startup Probes;
- Ingress;
- HPA;
- NetworkPolicy;
- StorageClass;
- PodDisruptionBudget;
- affinity;
- taints e tolerations;
- Helm;
- troubleshooting;
- observabilidade;
- GitOps.

Projeto:

- aplicação com múltiplos workloads;
- probes;
- limites;
- persistência;
- RBAC;
- simulação de falhas;
- runbook.

---

### 14. Projeto DevOps: Flask API — Do Código ao Deploy

- **Plataforma:** Udemy
- **Carga:** 14h08
- **Prioridade:** muito alta
- **Tipo:** projeto integrador principal
- **Execução:** integral em duas etapas
- **URL:** https://www.udemy.com/course/projeto-devops-flask-api-do-codigo-ao-deploy/

Abrange:

- Flask;
- MongoDB;
- Pytest;
- Docker;
- Docker Compose;
- Makefile;
- lint e segurança;
- GitHub Actions;
- Kind;
- Kubernetes;
- Helm;
- Sealed Secrets;
- Terraform;
- EKS e ECR;
- Route 53;
- TLS;
- OIDC;
- RBAC.

Etapa A:

- código;
- testes;
- Docker;
- CI.

Etapa B:

- Terraform;
- Kubernetes;
- Helm;
- EKS;
- DNS;
- TLS;
- CD.

Expansão SRE obrigatória:

- métricas RED;
- logs estruturados;
- tracing;
- dashboard;
- SLO;
- burn rate;
- alerta;
- runbook;
- post-mortem.

---

## Fase 4 — Observabilidade e práticas de SRE

### 15. Monitoramento de Aplicações com Prometheus e Grafana

- **Plataforma:** Udemy
- **Carga:** 5h37
- **Prioridade:** alta
- **Execução:** integral, acelerando Grafana básico
- **URL:** https://www.udemy.com/course/monitorando-aplicacoes-com-prometheus-e-grafana/

Conteúdo:

- arquitetura do Prometheus;
- pull model;
- Counter, Gauge, Histogram e Summary;
- instrumentação Node.js;
- scraping;
- PromQL;
- dashboards;
- alertas iniciais.

Complementos obrigatórios:

- Alertmanager;
- recording rules;
- service discovery;
- relabeling;
- cardinalidade;
- Node Exporter;
- Blackbox Exporter;
- kube-state-metrics;
- SLO e burn rate;
- Grafana Alerting atual.

Projeto:

```text
prometheus-sre-lab/
├── application/
├── prometheus/
├── alertmanager/
├── grafana/
├── load-test/
└── docs/
```

---

### 16. OpenTelemetry, logs e traces

- **Situação:** formação estruturada ainda ausente
- **Prioridade de compra:** futura
- **Momento:** após Docker, Kubernetes e Prometheus
- **Objetivo:** métricas, logs e traces correlacionados.

Conteúdo necessário:

- OpenTelemetry SDK;
- Collector;
- instrumentação automática e manual;
- propagação de contexto;
- sampling;
- cardinalidade;
- Loki;
- Tempo ou Jaeger;
- Grafana;
- Kubernetes.

Não comprar antes de concluir Prometheus e Kubernetes.

---

### 17. Práticas formais de SRE

- **Fonte principal:** Google SRE Book e Site Reliability Workbook
- **Prioridade:** muito alta
- **Tipo:** leitura e aplicação contínua
- **URLs:**
  - https://sre.google/sre-book/table-of-contents/
  - https://sre.google/workbook/table-of-contents/

Conteúdo:

- SLI;
- SLO;
- SLA;
- error budget;
- burn rate;
- toil;
- alertas acionáveis;
- capacidade;
- on-call;
- incident response;
- runbooks;
- post-mortems;
- simplicidade;
- gestão de risco.

Entregáveis:

- SLO de disponibilidade;
- SLO de latência;
- política de error budget;
- alerta multiwindow;
- runbook;
- exercício de incidente;
- post-mortem sem culpabilização.

---

## Fase 5 — Especializações

### 18. Curso de Zabbix 7 — Completo e atualizado

- **Plataforma:** Udemy
- **Carga:** 30h12
- **Prioridade:** média
- **Execução:** seletiva
- **URL:** https://www.udemy.com/course/curso-de-zabbix/

Priorizar:

- alta disponibilidade;
- PostgreSQL e TimescaleDB;
- LLD;
- Proxy;
- segurança;
- AD e 2FA;
- API;
- triggers avançadas;
- SLA;
- ODBC;
- SNMP;
- integração Grafana.

Acelerar fundamentos já dominados.

Projeto:

```text
zabbix-platform-lab/
├── docker/
├── ansible/
├── templates/
├── api/
├── grafana/
└── docs/
```

---

### 19. AWX para SysAdmin

- **Plataforma:** Udemy
- **Carga:** 7h48
- **Prioridade:** média
- **Pré-requisitos:** Ansible e Kubernetes básico
- **URL:** https://www.udemy.com/course/awx-para-sysadmin/

Conteúdo:

- AWX Operator;
- organizações;
- usuários e times;
- RBAC;
- LDAP;
- projetos Git;
- inventários;
- credenciais;
- Job Templates;
- Surveys;
- Workflows;
- aprovações;
- agendamentos.

Projeto:

- instalação de Zabbix Agent;
- workflow com aprovação;
- inventários separados;
- notificações;
- RBAC;
- backup e recuperação documentados.

---

### 20. DevOps: Automação sem Enrolação

- **Plataforma:** Udemy
- **Carga:** 14h35
- **Prioridade:** média
- **Execução:** seletiva
- **URL:** https://www.udemy.com/course/devops-automacao-sem-enrolacao/

Priorizar:

- AWS CLI;
- Azure CLI;
- `jq`;
- pipeline Terraform + Ansible + GitHub Actions;
- AKS;
- HPA;
- Ingress;
- KEDA;
- troubleshooting;
- Datadog.

Pular ou acelerar fundamentos já cobertos.

Este curso substitui o uso do curso curto “SRE DevOps: Jornada do início ao fim” como integrador.

---

### 21. SRE DevOps: Jornada do Início ao Fim

- **Plataforma:** Udemy
- **Carga:** 4h02
- **Prioridade:** baixa
- **Execução:** opcional e panorâmica
- **URL:** https://www.udemy.com/course/jornada-devops-sre-do-inicio-ao-fim/

Pode ser usado apenas para visão arquitetural.

Não utilizar como fonte principal de:

- Terraform;
- Kubernetes;
- observabilidade;
- SRE;
- GitOps;
- segurança.

---

### 22. DevOps Agêntico: Sem Enrolação

- **Plataforma:** Udemy
- **Carga:** 4h59
- **Prioridade:** média/baixa
- **Momento:** final da trilha
- **URL:** https://www.udemy.com/course/devops-agentico-sem-enrolacao/

Objetivo:

- IA aplicada a operações;
- análise de incidentes;
- geração de código e PRs;
- uso controlado de ferramentas;
- automação assistida.

Regra de maturidade:

```text
somente leitura
→ recomendações
→ geração de código ou PR
→ execução em laboratório
→ aprovação humana
→ automação limitada e auditada
```

Projeto:

```text
agentic-sre-assistant/
Alerta
→ coleta de contexto
→ análise
→ sugestão
→ aprovação humana
→ registro de auditoria
```

---

# 6. Programa Google Cloud

## Professional Cloud DevOps Engineer — Google Skills

- **Programa:** https://www.skills.google/paths/20
- **Benefícios disponíveis:**
  - 30 créditos mensais no Google Skills;
  - US$ 10 mensais para Google Cloud.
- **Prioridade:** paralela, controlada
- **Frequência:** a cada quarta folga, substituir dois blocos do roadmap por Google Skills.

Objetivos:

- CI/CD;
- SRE;
- observabilidade;
- troubleshooting;
- performance;
- custos;
- operação no Google Cloud.

Regras:

- não adicionar como terceira trilha diária;
- usar créditos somente em labs alinhados ao módulo atual;
- excluir recursos após o laboratório;
- registrar créditos consumidos;
- não ter pressa para realizar a certificação profissional.

---

# 7. Recursos gratuitos

| Recurso | Aplicação |
|---|---|
| GitHub Skills | Git e GitHub |
| Learn Git Branching | branches e merge |
| Pro Git | referência |
| Linux Journey | revisão Linux |
| OverTheWire Bandit | terminal e segurança |
| The Linux Command Line | leitura |
| SQLBolt | SQL |
| Automate the Boring Stuff | Python |
| KillerCoda | Kubernetes |
| Prometheus Docs | métricas e PromQL |
| Grafana Tutorials | dashboards |
| Google SRE Book | princípios |
| Site Reliability Workbook | implementação |
| Google Cloud Skills | cloud e SRE |

Conteúdo gratuito deve ser usado para reforçar lacunas, não para criar múltiplas trilhas simultâneas.

---

# 8. Projetos de portfólio

## Projeto 1 — Linux, Ansible e Zabbix

Objetivo:

- administrar Linux;
- automatizar configuração;
- instalar Zabbix Agent;
- criar template e LLD;
- versionar scripts;
- documentar troubleshooting.

## Projeto 2 — Flask API em AWS e Kubernetes

Objetivo:

- código;
- testes;
- Docker;
- CI/CD;
- Terraform;
- AWS;
- Kubernetes;
- Helm;
- DNS;
- TLS;
- segurança.

## Projeto 3 — Observabilidade e confiabilidade

Objetivo:

- Prometheus;
- Grafana;
- Loki;
- Tempo;
- OpenTelemetry;
- SLI;
- SLO;
- error budget;
- alerta;
- runbook;
- incidente;
- post-mortem.

## Projeto 4 — Automação agêntica controlada

Objetivo:

- receber alerta;
- coletar contexto autorizado;
- sugerir diagnóstico;
- localizar runbook;
- exigir aprovação;
- registrar auditoria.

---

# 9. Priorização resumida

## Obrigatórios

1. GNU/Linux.
2. Redes.
3. Git/GitHub.
4. SQL básico.
5. Python para DevOps.
6. Docker.
7. AWS re/Start.
8. AWS SAA-C03.
9. Terraform.
10. Ansible.
11. GitHub Actions.
12. Kubernetes.
13. Projeto Flask.
14. Prometheus e Grafana.
15. OpenTelemetry.
16. Práticas formais de SRE.

## Seletivos

- Cloud Practitioner;
- Zabbix 7;
- DevOps Automação sem Enrolação;
- curso curto Jornada SRE/DevOps.

## Especializações

- AWX;
- Google Professional Cloud DevOps Engineer;
- DevOps Agêntico.

---

# 10. Compras recomendadas

## Comprar quando for iniciar a fase

1. **Fundamentos de Redes para DevOps**
2. **Curso dedicado de Docker**

## Comprar futuramente

3. **OpenTelemetry e observabilidade completa**, apenas depois de Kubernetes e Prometheus.

## Não comprar agora

- outro curso de AWS;
- outro curso básico de Kubernetes;
- outro curso de GitHub Actions;
- outro curso de Ansible;
- outro curso de Terraform;
- curso adicional de Zabbix;
- curso de Helm antes de validar a necessidade.

A coleção atual já é suficiente para vários meses de estudo consolidado.

---

# 11. Campos esperados pela aplicação

Cada curso:

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
    "prerequisites": [],
}
```

Cada atividade:

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
    "prerequisites": [],
}
```

Os IDs não podem conter datas.

---

# 12. O que não deve voltar para este arquivo

Não incluir novamente:

- calendário mensal fixo;
- datas de cada aula;
- semanas S01–S36;
- prazo final rígido;
- regra de dia par ou ímpar por mês;
- IDs baseados em datas;
- cálculo de conclusão definitiva;
- reagendamento manual de todas as atividades;
- 30 labs obrigatórios presos a semanas.

Essas informações devem ser produzidas dinamicamente pela aplicação.

---

*Versão 3.0 — 05/08/2026*  
*Catálogo dinâmico para a escala 12x36*  
*Objetivo: conhecimento consolidado, projetos verificáveis e transição sustentável para SRE/DevOps.*
