# Manual do Projeto: Transição de Carreira (NOC Sênior → SRE)

Este documento serve como o manual definitivo do projeto de transição de carreira, detalhando a origem, os objetivos, a metodologia de estudo e o plano de ação construído para levar um profissional de NOC Sênior ao cargo de Site Reliability Engineer (SRE).

---

## 1. O Objetivo: Por que este projeto nasceu?

A área de tecnologia evolui rapidamente, e as operações tradicionais de TI estão sendo substituídas por práticas de Engenharia de Confiabilidade de Sites (SRE) e DevOps. 
O objetivo primário deste projeto é pavimentar um caminho estruturado, realista e altamente prático para a **transição de carreira de NOC Sênior para SRE**.

Como NOC Sênior, já existe uma bagagem enorme em monitoramento, resposta a incidentes, troubleshooting básico e vivência de produção. A transição para SRE não é sobre descartar esse conhecimento, mas sim **evoluí-lo através da automação, infraestrutura como código (IaC), nuvem e cultura de observabilidade avançada**.

---

## 2. A Metodologia de Construção do Roadmap

Para garantir que o plano fosse à prova de falhas, ele foi construído com base em três pilares principais:

### A. O "SRE Roadmap for Beginners" (Medium)
Como guia mestre, utilizamos o amplamente reconhecido "SRE Roadmap for Beginners", garantindo que as **15 Hard Skills fundamentais** exigidas pelo mercado de SRE fossem cobertas. Desde Linux e Networking até Kubernetes, CI/CD e Incident Management.

### B. Aproveitamento de Cursos Existentes + Indicações da IA
O currículo foi montado fazendo um "inventário" dos excelentes cursos que você já possuía (como os da Udemy e LinuxTips). Onde o roadmap do Medium exigia habilidades que não estavam cobertas pelos cursos iniciais, a IA sugeriu cursos complementares e materiais gratuitos de altíssima qualidade (como Kubernetes, Ansible, GitHub Actions e o Google SRE Book).

### C. A Adaptação à Realidade (A Escala 12x36)
A maior causa de desistência em planos de estudo é a falta de adequação à rotina do profissional. Este roadmap foi **matematicamente moldado para a sua escala 12x36**:
- **Dias de Folga (Ímpares/Pares alternados):** Considerados como "Dias Úteis" de estudo profundo (4 horas/dia). Nesses dias ocorrem os laboratórios densos, aulas práticas e simulados.
- **Dias de Plantão:** Estudo passivo de 30 minutos (podcasts, leitura de documentação) para manter o cérebro aquecido sem gerar burnout.

---

## 3. O Diferencial: 30 Semanas de Labs Zabbix

SREs juniores no mercado muitas vezes são teóricos. Para garantir que seu perfil se destaque nos processos seletivos, o projeto incorpora a sua especialidade atual (Zabbix) e a eleva ao nível de Engenharia.
Foi criado um cronograma paralelo de **30 Labs Práticos de Zabbix (1 por semana)**. Em vez de apenas instalar o Zabbix, os labs focam em integra-lo com o ecossistema SRE:
- Integração do Zabbix com AWS via automação.
- Zabbix + Ansible para auto-remediação.
- Monitoramento de clusters Kubernetes.
- Criação de pipelines CI/CD que disparam webhooks para alertas no Zabbix.

Isso constrói um **portfolio prático** fortíssimo e mostra que você consegue integrar ferramentas legadas/enterprise com tecnologias Cloud Native.

---

## 4. O Caminho: As 5 Fases da Transição

O roadmap de 36 semanas (Junho 2026 a Janeiro 2027) está estruturado para evoluir a sua "bagagem" técnica progressivamente, sem pular etapas fundamentais.

### Fase 1: Foundation (Fundamentos) — Semanas 01 a 04
O mercado não contrata um SRE que não domina a base. Esta fase foca na cultura (SRE Mindset), administração de sistemas Linux e fundamentos de redes TCP/IP.
- **O que você ganha:** Confiança absoluta na linha de comando, entendimento sobre como as requisições fluem na rede e a mentalidade de tratar infraestrutura como software.

### Fase 2: Core Skills (Habilidades Centrais) — Semanas 05 a 08
O momento de deixar de ser apenas um operador e começar a ser um desenvolvedor de infraestrutura.
- **O que você ganha:** Habilidade de versionar código (Git/GitHub), escrever scripts eficientes para automação (Python) e entender a base de dados (SQL). Aqui nasce a capacidade de criar pipelines de dados e integrações via API.

### Fase 3: Infra & Cloud (Nuvem e IaC) — Semanas 09 a 18
A transição definitiva para o mundo moderno de operações. Todo o foco é em Cloud e Infraestrutura como Código.
- **O que você ganha:** Proficiência na AWS (com objetivo de tirar a certificação SAA-C03), e a capacidade de não clicar mais em interfaces web, provisionando e configurando servidores usando **Terraform e Ansible (AWX)** de ponta a ponta.

### Fase 4: Advanced SRE (SRE Avançado) — Semanas 19 a 29
A fase mais complexa e que consolida o cargo de SRE.
- **O que você ganha:** Orquestração de containers (Kubernetes/Docker), automação completa de pipelines de entrega (GitHub Actions), e cultura real de Observabilidade (Integração do seu Zabbix com Prometheus e Grafana, gestão de Error Budgets e SLOs).

### Fase 5: Especialização & Capstone — Semanas 30 a 36
A fase final não é sobre aprender novas ferramentas, mas sobre **vender o seu perfil para o mercado**.
- **O que você ganha:** Construção de um "Capstone Project" (um projeto final de grande escala unindo tudo o que aprendeu), preparação de currículo/portfolio e o início da preparação para uma certificação avançada como a CKA (Certified Kubernetes Administrator).

---

## 5. O Painel SRE Tracker (Ferramental)

Para garantir que a consistência não se perdesse, foi desenvolvido localmente o **Painel Estudos SRE (v2.0)** em Python/FastAPI.
Ele não é apenas uma tabela do Excel; é um sistema dinâmico que:
- Mapeia exatamente as horas de cada dia baseado na sua escala real.
- Calcula a porcentagem de conclusão de cada fase e do programa global.
- Possui uma aba dedicada ao seu Diferencial de Zabbix (Labs).
- Mostra exatamente os dias restantes até o objetivo final, gerando a "gamificação" necessária para manter a disciplina nos dias difíceis.

## 6. O Resultado Esperado (Janeiro de 2027)

Ao concluir as 36 semanas, a sua "bagagem" será drasticamente diferente:
Você deixará de ser o profissional que reage a alertas no dashboard (NOC) para se tornar o Engenheiro que **constrói o dashboard, automatiza a resolução do alerta, provisiona a infraestrutura em nuvem via código e implementa as pipelines de CI/CD para as equipes de desenvolvimento**.

Esse é o exato perfil do **Site Reliability Engineer (SRE)** exigido hoje por empresas de ponta. O projeto te dará o embasamento teórico, a experiência prática via labs e o portfólio necessário para passar por entrevistas técnicas e cenários de arquitetura sem nenhuma dificuldade.
