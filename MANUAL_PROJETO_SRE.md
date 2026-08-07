# Manual do Projeto: Transição para SRE/DevOps

**Público:** profissionais em transição para SRE ou DevOps
**Escala padrão:** 12x36, com data-base configurável
**Versão:** 3.0 — cronograma dinâmico e sustentável

---

## Estado atual da aplicação

A migração para a agenda dinâmica está implementada. A aplicação atualmente possui:

- catálogo persistido de cursos e atividades originado em `data/curriculum.py`;
- IDs permanentes de atividades, sem datas embutidas;
- cálculo da escala 12x36 e geração idempotente de slots;
- alocação por sequência e pré-requisitos;
- reagendamento com histórico para atividades não realizadas ou adiadas;
- API de agenda, cursos, atividades, progresso, histórico e estatísticas;
- frontend diário integrado à nova API;
- exportação compatível com dados legados sempre que possível.

`WEEKS` não participa da nova agenda e existe somente como compatibilidade temporária.

---

## 1. Por que este projeto existe

Este projeto foi criado para orientar a transição de um profissional de monitoramento e operações para uma função de Site Reliability Engineering ou DevOps.

A experiência atual não deve ser descartada. Conhecimentos em Zabbix, Grafana, disponibilidade, incidentes, troubleshooting, SLA, SLI, SLO e automação constituem uma base relevante.

A transição consiste em ampliar essa base com:

- Linux e redes;
- Git e programação;
- containers;
- cloud;
- Infrastructure as Code;
- CI/CD;
- Kubernetes;
- observabilidade;
- práticas formais de confiabilidade;
- projetos de portfólio.

O objetivo não é dominar todas as ferramentas existentes. O objetivo é demonstrar capacidade de compreender um serviço, automatizar sua infraestrutura, implantá-lo, observá-lo e responder adequadamente quando ele falhar.

---

## 2. Objetivo profissional

O projeto busca preparar o usuário para concorrer a vagas de:

- Site Reliability Engineer;
- DevOps Engineer;
- Cloud Operations Engineer;
- Platform Engineer em nível inicial ou intermediário;
- Analista de Infraestrutura com foco em automação e cloud;
- Analista de Observabilidade.

O alvo principal é uma oportunidade:

- compatível com seus objetivos profissionais;
- sustentável em relação à rotina pessoal;
- com possibilidade de evolução técnica.

A formação deve ser sólida, mas não depende de um prazo final rígido.

---

## 3. Princípios do projeto

### 3.1 Sustentabilidade

O plano não deve comprometer:

- sono;
- saúde;
- vida pessoal;
- responsabilidades domésticas;
- trabalho atual.

Estudar até tarde para compensar um dia difícil não é considerado disciplina. É considerado risco de interrupção futura.

### 3.2 Consistência acima de velocidade

Metas mínimas:

- **dia de folga:** 2 horas;
- **dia de trabalho:** 1 hora.

O progresso será medido por:

- blocos concluídos;
- competências adquiridas;
- laboratórios realizados;
- projetos entregues;
- revisões concluídas.

Não será medido apenas por horas de vídeo.

### 3.3 Uma trilha principal por vez

O aluno deverá manter no máximo:

1. um curso principal do roadmap;
2. uma trilha paralela obrigatória, quando aplicável:
   - AWS re/Start;
   - Canvas;
   - Google Cloud Skills.

Não iniciar vários cursos técnicos principais simultaneamente.

### 3.4 Aprender fazendo

Cada fase deve resultar em artefatos concretos:

- scripts;
- código;
- pipelines;
- dashboards;
- infraestrutura;
- documentação;
- runbooks;
- post-mortems;
- repositórios públicos.

---

## 4. Base técnica do roadmap

O roadmap foi construído a partir da combinação de:

- SRE Roadmap for Beginners;
- SRE Practical Roadmap 2026;
- experiência prática já existente;
- cursos disponíveis;
- Google SRE Book;
- Site Reliability Workbook;
- exigências comuns em vagas de SRE e DevOps.

O primeiro roadmap fornece a base progressiva. O segundo adiciona tecnologias atuais, como Terraform, GitOps e maior foco em entrevistas.

A trilha combinada prioriza:

```text
Linux e redes
→ Git, SQL e Python
→ Docker
→ cloud
→ Terraform e Ansible
→ CI/CD
→ Kubernetes
→ observabilidade
→ SLO e incidentes
→ especializações
```

---

## 5. Escala 12x36

A escala deve ser calculada pela sequência real de dias corridos.

### Data-base

Cada instalação deve definir `SCALE_ANCHOR_DATE` com uma data conhecida como
`FOLGA`. O valor `2030-01-01` abaixo é apenas um exemplo neutro.

Implementação recomendada:

```python
from datetime import date

SCALE_ANCHOR = date.fromisoformat(os.getenv("SCALE_ANCHOR_DATE", "2030-01-01"))

def get_day_type(current_date: date) -> str:
    days = (current_date - SCALE_ANCHOR).days
    return "FOLGA" if days % 2 == 0 else "TRABALHO"
```

Não utilizar regras mensais baseadas em dias pares ou ímpares.

---

## 6. Rotina de estudo

### 6.1 Dia de folga

Carga mínima: 2 horas, divididas em quatro blocos de 30 minutos.

| Bloco | Horário sugerido | Uso |
|---|---|---|
| F1 | 13h30–14h00 | conteúdo teórico |
| F2 | 14h10–14h40 | exercício ou continuação |
| F3 | 15h20–15h50 | laboratório |
| F4 | 16h00–16h30 | laboratório, revisão ou AWS |

Um intervalo livre opcional pode ser usado para:

- flashcards;
- leitura de documentação;
- revisão de comandos;
- anotações;
- questões.

Esse intervalo é opcional e não entra na carga mínima.

### 6.2 Dia de trabalho

Carga mínima: 1 hora.

| Bloco | Horário sugerido | Uso |
|---|---|---|
| T1 | 7h00–7h30 | curso principal |
| T2 | intervalo de almoço | revisão, leitura ou AWS |

O período da tarde é imprevisível e não deve ser considerado no planejamento obrigatório.

O período noturno deve priorizar:

- AWS re/Start, quando houver aula;
- organização do dia seguinte;
- leitura;
- sono.

### 6.3 Regra de sono

Nos dias de trabalho, o descanso deve ser priorizado.

Estudos não concluídos não devem ser compensados reduzindo o sono.

---

## 7. Funcionamento dinâmico do cronograma

O cronograma não terá datas definitivas para cada aula.

A aplicação manterá:

- uma fila ordenada de atividades;
- uma agenda de slots disponíveis;
- histórico de execução;
- reagendamentos;
- progresso por competência.

### Estados das atividades

| Estado | Significado |
|---|---|
| `pending` | ainda não iniciada |
| `in_progress` | iniciada |
| `done` | concluída |
| `deferred` | não realizada e devolvida à fila |
| `blocked` | depende de recurso ou pré-requisito |
| `skipped` | retirada conscientemente |
| `cancelled` | removida definitivamente |

### Regra de “não feito”

Quando uma atividade for marcada como não feita:

1. o slot original é registrado no histórico;
2. a atividade recebe status `deferred`;
3. ela volta para a fila;
4. ocupa o próximo slot compatível;
5. as atividades concluídas permanecem intactas;
6. o sistema não desloca manualmente todo o calendário.

A atividade deverá possuir ID permanente, sem data:

```text
linux-admin-sec03-lesson01
python-devops-project-alert-router
terraform-module-state-backend
```

---

## 8. Fases da transição

## Fase 1 — Fundamentos operacionais

Competências:

- Linux;
- redes;
- Git;
- SQL;
- Python.

Resultados esperados:

- administrar uma VM Linux;
- diagnosticar conectividade;
- manipular logs;
- criar scripts;
- versionar código;
- consultar banco de dados;
- consumir APIs.

Projeto principal:

```text
linux-sre-toolkit
```

---

## Fase 2 — Containers, cloud e IaC

Competências:

- Docker;
- AWS;
- Terraform;
- Ansible.

Resultados esperados:

- containerizar aplicações;
- compreender arquitetura AWS;
- provisionar infraestrutura como código;
- configurar servidores automaticamente;
- controlar custos e permissões.

Projetos:

```text
terraform-aws-lab
ansible-sre-lab
```

---

## Fase 3 — CI/CD e Kubernetes

Competências:

- GitHub Actions;
- Kubernetes;
- Helm;
- segurança de pipelines;
- deployment.

Resultados esperados:

- criar pipelines;
- executar testes;
- construir imagens;
- implantar aplicações;
- trabalhar com workloads Kubernetes;
- configurar probes, recursos, volumes e RBAC.

Projeto principal:

```text
Flask API — código ao deploy
```

---

## Fase 4 — Observabilidade e SRE

Competências:

- Prometheus;
- Grafana;
- Loki;
- Tempo ou Jaeger;
- OpenTelemetry;
- SLI;
- SLO;
- error budget;
- alertas;
- incident response;
- post-mortems.

Resultados esperados:

- instrumentar aplicação;
- criar métricas RED;
- correlacionar telemetria;
- definir SLO;
- criar alertas acionáveis;
- escrever runbook;
- conduzir incidente simulado.

Projeto principal:

```text
prometheus-sre-lab
```

---

## Fase 5 — Especialização e carreira

Conteúdos:

- Zabbix avançado;
- AWX;
- Google Cloud DevOps;
- DevOps agêntico;
- portfólio;
- currículo;
- entrevistas.

Resultados esperados:

- integrar Zabbix com automação;
- centralizar playbooks;
- criar projetos documentados;
- apresentar incidentes em entrevistas;
- demonstrar decisões técnicas.

---

## 9. Trilhas paralelas

### 9.1 AWS re/Start

Enquanto estiver ativo:

- faz parte da carga oficial;
- Canvas não deve ser acumulado todas as noites;
- tarefas obrigatórias têm prioridade;
- o conteúdo deve ser relacionado ao curso SAA-C03.

### 9.2 Google Cloud Skills

Recursos disponíveis:

- 30 créditos mensais;
- US$ 10 mensais de Google Cloud.

Frequência recomendada:

- a cada quarta folga;
- substituir dois blocos do roadmap;
- não adicionar como terceira trilha simultânea.

Programa:

```text
Professional Cloud DevOps Engineer
https://www.skills.google/paths/20
```

A certificação profissional não precisa ser feita imediatamente.

---

## 10. Diferencial com Zabbix

O Zabbix permanece como diferencial técnico, mas não haverá obrigação de um laboratório fixo por semana.

Os laboratórios serão vinculados às competências estudadas.

Exemplos:

- Linux: instalação e troubleshooting do agente;
- Python: automação via API;
- Ansible: instalação em massa;
- AWS: monitoramento de recursos;
- Kubernetes: coleta e integração;
- Prometheus: dashboards combinados;
- SRE: SLA, SLO e incidentes;
- AWX: remediação com aprovação.

O objetivo é transformar experiência operacional em:

- automação;
- arquitetura;
- integração;
- confiabilidade;
- portfólio.

---

## 11. Projetos de portfólio

### Projeto 1 — Linux, Ansible e Zabbix

Demonstrar:

- administração Linux;
- scripts;
- Ansible;
- instalação de agentes;
- template;
- LLD;
- documentação.

### Projeto 2 — Flask API em AWS e Kubernetes

Demonstrar:

- desenvolvimento;
- testes;
- Docker;
- CI/CD;
- Terraform;
- AWS;
- Kubernetes;
- Helm;
- segurança;
- deployment.

### Projeto 3 — Observabilidade e confiabilidade

Demonstrar:

- Prometheus;
- Grafana;
- logs;
- traces;
- OpenTelemetry;
- SLO;
- alertas;
- runbook;
- post-mortem.

### Projeto 4 — Assistente agêntico controlado

Demonstrar:

- leitura de alertas;
- coleta de contexto;
- sugestão de diagnóstico;
- aprovação humana;
- auditoria.

---

## 12. Painel Estudos SRE

O painel deve deixar de operar como um calendário rígido.

### Funções obrigatórias

- calcular automaticamente folga e trabalho;
- gerar slots de estudo;
- manter fila de atividades;
- reagendar atividades adiadas;
- registrar histórico;
- mostrar curso atual;
- mostrar próxima atividade;
- separar teoria, prática e revisão;
- acompanhar AWS re/Start;
- acompanhar Google Cloud Skills;
- mostrar progresso por competência;
- registrar projetos e milestones;
- exportar e importar backup.

### O que o painel não deve fazer

- impor prazo final fixo;
- prender ID à data;
- recalcular manualmente todas as datas;
- marcar o aluno como atrasado por uma atividade adiada;
- exigir quatro horas em todas as folgas;
- considerar estudo noturno obrigatório após plantão;
- obrigar laboratório Zabbix semanal.

### Métricas úteis

- blocos planejados;
- blocos concluídos;
- taxa de execução;
- horas práticas;
- horas de vídeo;
- atividades adiadas;
- sequência sustentável;
- projetos concluídos;
- competências consolidadas.

A taxa de execução deve ser mais importante que uma data final artificial.

---

## 13. Critérios de prontidão para vagas

Não é necessário concluir toda a trilha para começar a se candidatar.

O aluno pode iniciar candidaturas quando conseguir demonstrar:

- Linux e redes;
- Git;
- Python ou Bash;
- Docker;
- fundamentos de cloud;
- Terraform;
- CI/CD;
- Kubernetes básico;
- monitoramento;
- experiência com incidentes;
- ao menos dois projetos documentados.

Para vagas SRE, também deve conseguir explicar:

- SLI;
- SLO;
- SLA;
- error budget;
- toil;
- alerta acionável;
- post-mortem;
- disponibilidade;
- latência;
- capacidade.

---

## 14. Resultado esperado

O resultado não será definido por uma data específica.

O projeto será bem-sucedido quando o usuário puder demonstrar que consegue:

1. administrar e diagnosticar sistemas Linux;
2. compreender redes e dependências;
3. escrever automações;
4. versionar infraestrutura;
5. criar pipelines;
6. operar aplicações em containers;
7. trabalhar com Kubernetes;
8. implementar observabilidade;
9. definir objetivos de confiabilidade;
10. responder a incidentes;
11. documentar decisões;
12. apresentar projetos em entrevistas.

A meta é tornar-se um profissional SRE ou DevOps competente, capaz de receber uma oportunidade e demonstrar valor.

---

## 15. Regra central do projeto

> O cronograma deve se adaptar à vida do aluno. A vida do aluno não deve ser quebrada para obedecer ao cronograma.

---

*Versão 3.0 — agenda configurável*
*Transição sustentável de Monitoramento para SRE/DevOps*
