# Changelog

Todas as alterações relevantes do SRE Tracker serão registradas neste arquivo.

O formato segue os princípios do [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
com as categorias `Adicionado`, `Alterado`, `Corrigido`, `Removido` e `Segurança`.

## [Não lançado]

## [3.1.0]

### Adicionado

- Endpoint `POST /api/activities/{activity_id}/reopen` para reverter atividades concluídas ou iniciadas por engano de volta para o estado pendente.
- Botão `↩ Reabrir` em cards de atividades concluídas e `↩ Desfazer início` em atividades em andamento no frontend.
- Templates públicos de configuração pessoal `MANUAL_PROJETO_SRE.example.md` e `STATE_SAVE.example.md`.
- Suporte a Docker Compose com persistência por bind mount do arquivo SQLite (`sre_tracker.db`) no host.
- Testes automatizados para o fluxo de reabertura de atividades (totalizando 52 testes na suíte).

### Alterado

- Currículo oficial (`data/curriculum.py` e `COURSES.md`):
  - `aws-restart`: prazo oficial fixado para ~25/09/2026 e registro de aulas seg–sex 19h–20h.
  - `aws-clf`: promovido para prioridade alta e execução integral, com pré-requisito `aws-restart` e janela de acesso até 25/10/2026.
- `services/curriculum_seed.py`: campo `sequence` tornado imutável durante atualizações do catálogo, prevenindo colisões de chave UNIQUE.
- `docker-compose.yml`: variáveis sensíveis e data âncora agora são lidas dinamicamente do `.env`.
- `.gitignore`: arquivos pessoais (`MANUAL_PROJETO_SRE.md`, `STATE_SAVE.md`, `GEMINI.md`, `*.db.bak-*`) adicionados para proteção contra vazamento.
- `README.md`: documentação completa com instruções de execução via Docker Compose, gestão de arquivos de configuração pessoal e tabela da API atualizada.

### Removido

- Curso `devops-jornada` (e suas atividades associadas) removido do currículo e migrado no banco de dados.

## [3.0.0]

### Adicionado

- Modelos dinâmicos `Course`, `Activity`, `StudySlot`, `ActivityProgress`,
  `ActivityHistory` e `AppSetting`.
- Schemas Pydantic correspondentes à nova arquitetura.
- Seed idempotente de cursos e atividades a partir de `data/curriculum.py`.
- Serviço da escala 12x36 com âncora de folga configurável.
- Geração idempotente de quatro slots nas folgas e dois slots nos dias de trabalho.
- Motor de alocação, pré-requisitos, adiamento e reagendamento.
- Histórico de ações e estados `blocked`, `skipped` e `cancelled`.
- API dinâmica de cursos, atividades, agenda, histórico, estatísticas e progresso.
- Endpoint para adicionar nota sem alterar o estado da atividade.
- Interface dinâmica com as seções Hoje, Fila, Cursos, Roadmap, Projetos,
  AWS re/Start, Google Cloud, Histórico e Estatísticas.
- Testes de modelos, seed, escala, scheduling, API e integração estática do frontend.

### Alterado

- Migração da experiência de cronograma rígido para uma agenda contínua baseada na escala 12x36.
- Frontend passou a consumir a nova API em vez de depender de `WEEKS` injetado no HTML.
- A tela Hoje passou a consumir a rota canônica `GET /api/schedule/today`.
- Bundle do frontend atualizado para `app.js?v=7`, invalidando versões antigas em cache.

### Corrigido

- Integração da seção Hoje com a agenda registrada no FastAPI.
- Proteção contra prefixo duplicado `/api/api/` coberta por testes.
- Confirmação de resposta com `date`, `day_type` e `slots` na rota da agenda atual.

### Removido

- Referências visuais ao cronograma de 36 semanas, prazo de janeiro de 2027,
  dias restantes e calendário rígido.
- Dependência real de `WEEKS` na nova interface e na agenda dinâmica.

### Verificação

- Suíte atual: `48 passed`.
- `GET /api/schedule/today`: HTTP 200.
- Interface Hoje validada em navegador, sem painel de erro.
