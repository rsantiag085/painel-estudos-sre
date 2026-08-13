# Manual do Projeto: Transição para SRE/DevOps

> **Este é um arquivo de exemplo.**
> Copie-o para `MANUAL_PROJETO_SRE.md`, remova este aviso e preencha com
> as suas informações reais. O arquivo original está listado no `.gitignore`
> e nunca será enviado ao repositório.

**Público:** profissionais em transição para SRE ou DevOps
**Escala padrão:** [sua escala — ex: 12x36, comercial, etc.]
**Versão:** 3.0 — cronograma dinâmico e sustentável

---

## Estado atual da aplicação

A migração para a agenda dinâmica está implementada. A aplicação atualmente possui:

- catálogo persistido de cursos e atividades originado em `data/curriculum.py`;
- IDs permanentes de atividades, sem datas embutidas;
- cálculo da escala de trabalho e geração idempotente de slots;
- alocação por sequência e pré-requisitos;
- reagendamento com histórico para atividades não realizadas ou adiadas;
- API de agenda, cursos, atividades, progresso, histórico e estatísticas;
- frontend diário integrado à nova API;
- exportação compatível com dados legados sempre que possível.

---

## 1. Por que este projeto existe

[Descreva aqui sua motivação pessoal para usar esta ferramenta. Exemplo:]

Este projeto foi criado para orientar a transição de um profissional de
[sua área atual] para uma função de Site Reliability Engineering ou DevOps.

A experiência atual não deve ser descartada. Conhecimentos em [suas ferramentas atuais]
constituem uma base relevante.

---

## 2. Objetivo profissional

[Liste as posições que você deseja alcançar. Exemplos:]

- Site Reliability Engineer;
- DevOps Engineer;
- Cloud Operations Engineer;
- Platform Engineer;
- Analista de Infraestrutura com foco em automação e cloud.

O alvo principal é uma oportunidade:

- compatível com seus objetivos profissionais;
- sustentável em relação à rotina pessoal;
- com possibilidade de evolução técnica.

---

## 3. Princípios do projeto

### 3.1 Sustentabilidade

O plano não deve comprometer:

- sono;
- saúde;
- vida pessoal;
- responsabilidades domésticas;
- trabalho atual.

### 3.2 Consistência acima de velocidade

Metas mínimas — adapte à sua realidade:

- **[tipo de dia 1]:** [X] horas;
- **[tipo de dia 2]:** [Y] horas.

### 3.3 Uma trilha principal por vez

Manter no máximo:

1. um curso principal do roadmap;
2. uma trilha paralela obrigatória, quando aplicável.

### 3.4 Aprender fazendo

Cada fase deve resultar em artefatos concretos:
scripts, código, pipelines, dashboards, infraestrutura, documentação, runbooks,
post-mortems, repositórios públicos.

---

## 4. Base técnica do roadmap

[Descreva aqui as referências que você usou para montar sua trilha. Exemplos:]

- SRE Roadmap for Beginners;
- SRE Practical Roadmap 2026;
- experiência prática já existente;
- Google SRE Book;
- Site Reliability Workbook;
- exigências comuns em vagas de SRE e DevOps.

---

## 5. Escala de trabalho

### Data-base

Defina `SCALE_ANCHOR_DATE` no arquivo `.env` com uma data conhecida como dia de
**FOLGA** (ou descanso). O valor abaixo é apenas um exemplo neutro.

```bash
# .env
SCALE_ANCHOR_DATE=2030-01-01   # substitua por uma data real de FOLGA
```

A fórmula usada internamente:

```python
from datetime import date

SCALE_ANCHOR = date.fromisoformat(os.getenv("SCALE_ANCHOR_DATE", "2030-01-01"))

def get_day_type(current_date: date) -> str:
    days = (current_date - SCALE_ANCHOR).days
    return "FOLGA" if days % 2 == 0 else "TRABALHO"
```

---

## 6. Rotina de estudo

### 6.1 Dia de folga / descanso

[Adapte os horários à sua rotina pessoal. Exemplo:]

| Bloco | Horário sugerido | Uso |
|---|---|---|
| F1 | [horário] | conteúdo teórico |
| F2 | [horário] | exercício ou continuação |
| F3 | [horário] | laboratório |
| F4 | [horário] | laboratório, revisão ou trilha paralela |

### 6.2 Dia de trabalho

[Adapte os horários à sua rotina pessoal. Exemplo:]

| Bloco | Horário sugerido | Uso |
|---|---|---|
| T1 | [horário] | curso principal |
| T2 | [horário] | revisão ou leitura |

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

---

## 8. Fases da transição

[As fases abaixo refletem o roadmap padrão. Adapte conforme seu currículo em `data/curriculum.py`.]

### Fase 1 — Fundamentos operacionais

Competências: Linux, redes, Git, SQL, Python.

### Fase 2 — Containers, cloud e IaC

Competências: Docker, AWS (ou outra cloud), Terraform, Ansible.

### Fase 3 — CI/CD e Kubernetes

Competências: GitHub Actions, Kubernetes, Helm, segurança de pipelines.

### Fase 4 — Observabilidade e SRE

Competências: Prometheus, Grafana, OpenTelemetry, SLO, alertas, incidentes.

### Fase 5 — Especialização e carreira

Competências: [suas especializações], portfólio, currículo, entrevistas.

---

## 9. Trilhas paralelas

### 9.1 [Nome da sua trilha paralela obrigatória — ex: AWS re/Start]

[Descreva aqui sua trilha paralela, prazos e como registrar no painel.]

### 9.2 [Outra trilha paralela opcional — ex: Google Cloud Skills]

[Descreva frequência, recursos disponíveis e critérios de uso.]

---

## 10. Projetos de portfólio

### Projeto 1 — [Nome do projeto]

Demonstrar: [competências relevantes]

### Projeto 2 — [Nome do projeto]

Demonstrar: [competências relevantes]

### Projeto 3 — [Nome do projeto]

Demonstrar: [competências relevantes]

---

## 11. Critérios de prontidão para vagas

[Ajuste a lista abaixo com as competências que você definiu como gate para começar a se candidatar:]

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

---

## 12. Regra central do projeto

> O cronograma deve se adaptar à vida do usuário. A vida do usuário não deve ser quebrada para obedecer ao cronograma.

---

*Versão 3.0 — agenda configurável*
*Transição sustentável para SRE/DevOps*
