# Proposal

## Why

Atualmente, os erros retornados pela API podem não seguir um formato unificado e claro, dificultando o tratamento por clientes (front-end, outros serviços, etc.). Padronizar os erros conforme o formato RFC 7807 (Problem Details for HTTP APIs) garantirá uma estrutura consistente, rica em detalhes e fácil de consumir.

## What Changes

- Implementação de um padrão global para respostas de erro na API FastAPI.
- A resposta de erro conterá os seguintes campos (baseados na RFC 7807):
  - `type`: Uma URI que identifica o tipo de erro.
  - `title`: Um resumo curto e legível do tipo de problema.
  - `status`: O código de status HTTP.
  - `detail`: Uma explicação detalhada do que ocorreu.
  - `instance`: Uma URI opcional com a ocorrência exata.
- Atualização dos Global Exception Handlers no `src/main.py` para utilizar esse novo formato.

## Capabilities

### New Capabilities
- `api-error-handling`: Padronização de respostas de erro da API de acordo com a RFC 7807.

### Modified Capabilities
Nenhuma.

## Impact

- Modifica os exception handlers em `src/main.py`.
- Afeta as respostas HTTP da API para os status 400, 404, 409 e 422.
- Melhora a experiência de desenvolvedores/clientes consumindo a API.
