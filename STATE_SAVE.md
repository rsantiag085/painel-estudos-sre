# State Save — SRE Tracker

Este arquivo guarda o ponto de retomada do projeto entre sessões de trabalho.

Quando o usuário disser **salvar o ponto**, este documento deve ser atualizado com
o estado real do repositório naquele momento. O registro deve ser objetivo e não
deve substituir o histórico permanente do `CHANGELOG.md`.

## Último ponto salvo

- **Data:** encerramento da sessão de configuração multiusuário
- **Objetivo da sessão:** tornar o painel reutilizável por terceiros e publicar uma versão segura.
- **Estado:** implementação, testes, documentação e publicação concluídos no branch `main`.
- **Comando para retomar:** `python -m uvicorn main:app --host 127.0.0.1 --port 8000`
- **Endereço local:** http://127.0.0.1:8000
- **Última suíte executada:** `51 passed in 8.78s`

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
- Configuração de primeiro acesso com nome, início e referência da escala.
- Persistência das preferências de cada instalação em `AppSetting`.
- Histórico Git higienizado e autoria vinculada ao `noreply` da conta GitHub.
- Remoção de documentos pessoais e de uma cópia duplicada do catálogo.

## Estado validado

- A escala respeita a data e o tipo de dia configurados pelo usuário.
- A tela Hoje carrega quatro slots.
- A rota `/api/schedule/today` retorna HTTP 200.
- Não existe rota duplicada `/api/api/schedule/today`.
- O navegador carregou o fluxo de configuração sem erros de console.

## Próximo passo recomendado

1. Concluir os testes manuais da agenda antes do início oficial dos estudos.
2. Limpar os resultados criados durante os testes, preservando cursos e configurações.
3. Revisar a Fila e decidir sobre paginação, busca ou filtros.
4. Adicionar favicon e metadados visuais do repositório quando conveniente.

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
