# State Save — SRE Tracker

> **Este é um arquivo de exemplo.**
> Copie-o para `STATE_SAVE.md`, remova este aviso e use-o para registrar
> o ponto de retomada das suas sessões de desenvolvimento.
> O arquivo original está listado no `.gitignore` e nunca será enviado ao repositório.

Este arquivo guarda o ponto de retomada do projeto entre sessões de trabalho.

Quando você quiser **salvar o ponto**, atualize este documento com o estado real
do repositório naquele momento. O registro deve ser objetivo e não deve substituir
o histórico permanente do `CHANGELOG.md`.

---

## Último ponto salvo

- **Data e hora:**
- **Objetivo da sessão:**
- **Estado:**
- **Comando para retomar:**
- **Endereço local:** http://localhost:8000
- **Última suíte executada:**

## O que foi concluído

- [Liste aqui o que foi feito nesta sessão]

## Estado validado

- [ ] Os testes passam (`pytest`)
- [ ] A aplicação sobe sem erros
- [ ] A rota `/api/schedule/today` retorna HTTP 200
- [ ] O frontend carrega sem erros de console

## Próximo passo recomendado

1. [Descreva o próximo passo exato]

## Arquivos alterados nesta sessão

- [liste os arquivos relevantes]

## Erros e contornos

- [Descreva erros encontrados e soluções adotadas]

## Pendências conhecidas

- [Liste itens pendentes]

---

## Protocolo para "salvar o ponto"

Ao encerrar um dia de trabalho:

1. Inspecionar `git status` e registrar os arquivos relevantes alterados.
2. Executar os testes adequados e anotar o resultado exato.
3. Registrar erros ainda abertos e soluções temporárias adotadas.
4. Atualizar neste arquivo a data, o estado, o último trabalho concluído e o próximo passo.
5. Transferir as mudanças relevantes para a seção `[Não lançado]` do `CHANGELOG.md`.
6. Não fazer commit ou push sem solicitação explícita.

---

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
