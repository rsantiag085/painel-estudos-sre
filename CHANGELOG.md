# Changelog

Todas as alterações relevantes do SRE Tracker serão registradas neste arquivo.

O formato segue os princípios do [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/),
com as categorias `Adicionado`, `Alterado`, `Corrigido`, `Removido` e `Segurança`.

## [Não lançado]

### Adicionado

- Arquivo `STATE_SAVE.md` para registrar o ponto de retomada entre sessões de trabalho.
- Procedimento de encerramento diário acionado pela frase **salvar o ponto**.

### Alterado

- Ponto de retomada consolidado ao final da sessão de 05/08/2026, após execução
  bem-sucedida de toda a suíte de testes.
- Documentação principal atualizada para descrever a API, a estrutura de arquivos
  e o estágio real da migração dinâmica.
- Documentos do cronograma anterior em `docs_planejamento/` identificados como
  material histórico e não normativo.

## [2026-08-05]

### Adicionado

- Modelos dinâmicos `Course`, `Activity`, `StudySlot`, `ActivityProgress`,
  `ActivityHistory` e `AppSetting`.
- Schemas Pydantic correspondentes à nova arquitetura.
- Seed idempotente de cursos e atividades a partir de `data/curriculum.py`.
- Serviço da escala 12x36 com a âncora 05/08/2026 como FOLGA.
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
