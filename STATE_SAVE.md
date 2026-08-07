# State Save — SRE Tracker

Este arquivo guarda o ponto de retomada do projeto entre sessões de trabalho.

Quando o usuário disser **salvar o ponto**, este documento deve ser atualizado com
o estado real do repositório naquele momento. O registro deve ser objetivo e não
deve substituir o histórico permanente do `CHANGELOG.md`.

## Último ponto salvo

- **Data:** 05/08/2026 22:48 — America/Fortaleza
- **Objetivo da sessão:** consolidar a documentação e preparar a publicação das mudanças no GitHub.
- **Estado:** implementação e documentação alinhadas; publicação aguardando nova autenticação do GitHub CLI.
- **Comando para retomar:** `uvicorn main:app --reload --log-level debug`
- **Endereço local:** http://127.0.0.1:8000
- **Última suíte executada:** `48 passed in 7.95s`

## O que foi concluído

- Nova arquitetura de cursos, atividades, slots, progresso, histórico e configurações.
- Seed idempotente baseado em `COURSES` e `ACTIVITIES`.
- Escala 12x36 e geração idempotente de slots.
- Alocação e reagendamento de atividades.
- API dinâmica e frontend integrado.
- Correção da rota da tela Hoje para `GET /api/schedule/today`.
- Invalidação do cache do JavaScript com `app.js?v=7`.
- Verificação HTTP e visual da seção Hoje.
- Atualização de `README.md`, `MANUAL_PROJETO_SRE.md` e `COURSES.md` conforme a implementação real.
- Identificação de `docs_planejamento/` como arquivo histórico não normativo.
- Criação e consolidação de `CHANGELOG.md` e deste ponto de retomada.

## Estado validado

- 05/08/2026 retorna `FOLGA`.
- A tela Hoje carrega quatro slots.
- A rota `/api/schedule/today` retorna HTTP 200.
- Não existe rota duplicada `/api/api/schedule/today`.
- O navegador carregou `app.js?v=7` sem painel de erro.

## Próximo passo recomendado

1. Executar `gh auth login -h github.com`.
2. Confirmar a autenticação com `gh auth status`.
3. Criar a branch `agent/migracao-agenda-dinamica`.
4. Revisar e versionar as mudanças, sem incluir `data/curriculum.py.bak`.
5. Executar a suíte final, fazer push e abrir um Pull Request draft.
6. Após a publicação, revisar a Fila e decidir sobre paginação, busca ou filtros.

## Arquivos e áreas alteradas nesta etapa

- Documentação e currículo: `COURSES.md`, `MANUAL_PROJETO_SRE.md`, `README.md` e `data/curriculum.py`.
- Persistência e contratos: `database.py`, `models.py` e `schemas.py`.
- Aplicação e API: `main.py`, `routers/` e `services/`.
- Interface: `templates/index.html`, `static/app.js` e `static/style.css`.
- Testes e configuração: `tests/` e `pytest.ini`.
- Continuidade: `CHANGELOG.md` e `STATE_SAVE.md`.

## Erros e contornos da sessão

- A tela Hoje apresentou `Not Found` em uma instância antiga da aplicação.
- A tabela de rotas e o OpenAPI confirmaram `GET /api/schedule/today` sem prefixo duplicado.
- O frontend passou a chamar a rota canônica sem query string e o bundle foi atualizado para `app.js?v=7` para evitar cache antigo.
- Um primeiro `curl` de validação não alcançou o servidor por isolamento da ferramenta; a chamada foi repetida no mesmo contexto de rede e retornou HTTP 200.
- `/favicon.ico` continua retornando 404, sem impacto funcional.

## Pendências conhecidas

- O diretório de trabalho possui alterações ainda não commitadas.
- O token do GitHub CLI para `rsantiag085` está inválido; nenhum stage, commit ou push foi realizado.
- `data/curriculum.py.bak` é um artefato de backup e não deve entrar no commit.
- `WEEKS` ainda pode existir apenas como compatibilidade temporária em código legado.
- A fila pode renderizar muitas atividades de uma vez.
- O favicon ainda não existe; `/favicon.ico` retorna 404 sem afetar a aplicação.

## Protocolo para “salvar o ponto”

Ao encerrar um dia de trabalho:

1. Inspecionar `git status` e registrar os arquivos relevantes alterados.
2. Executar os testes adequados e anotar o resultado exato.
3. Registrar erros ainda abertos e soluções temporárias adotadas.
4. Atualizar neste arquivo a data, o estado, o último trabalho concluído e o próximo passo.
5. Transferir as mudanças relevantes para a seção `[Não lançado]` do `CHANGELOG.md`.
6. Não fazer commit ou push sem solicitação explícita do usuário.

## Modelo para o próximo registro

```text
Data e hora:
Objetivo da sessão:
Concluído:
Arquivos alterados:
Testes executados:
Resultado dos testes:
Erros ou bloqueios:
Decisões e contornos:
Próximo passo exato:
Comando para retomar:
```
