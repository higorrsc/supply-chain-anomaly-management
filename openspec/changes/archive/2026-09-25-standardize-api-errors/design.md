# Design

## Context

Atualmente, `src/main.py` possui *Global Exception Handlers* que capturam as exceções de domínio e retornam simples `{"detail": "..."}`. A RFC 7807 (Problem Details) introduz uma estrutura mais semântica. O FastAPI possui nativamente os mecanismos para injetar classes próprias de serialização e models do Pydantic para padronizar esses retornos.

## Goals / Non-Goals

**Goals:**
- Adaptar as respostas de erro globais para o formato `type`, `title`, `status`, `detail`, `instance`.
- Garantir que as validações originais de request (FastAPI `RequestValidationError`) também sigam o padrão RFC 7807 se possível (opcional).
- Assegurar compatibilidade com o OpenAPI Swagger (schemas).

**Non-Goals:**
- Criar URIs hospedadas reias para a propriedade `type`. Usaremos URNs semânticas fixas como `urn:api:error:conflict` ou `about:blank`.

## Decisions

**1. Pydantic Model para as Respostas de Erro:**
Criaremos um `RFC7807Error` herdando de `BaseModel` em `src/core/presentation/api/schemas.py` (ou local equivalente) para documentar a resposta no Swagger.

**2. Handlers no main.py:**
Modificaremos os exception handlers atuais no `src/main.py`:
- `domain_error_handler` (400)
- `entity_not_found_handler` (404)
- `conflict_error_handler` (409)
- `entity_validation_error_handler` (422)

Cada handler criará e retornará um JSONResponse preenchido de acordo com a RFC 7807. O campo `type` será derivado da exceção (ex: `urn:problem-type:entity-not-found`) e o campo `instance` será capturado de `request.url.path`.

## Risks / Trade-offs

- **[Risco] Cliente existente parar de funcionar:** Se houver clientes que parseavam estritamente `response.json()["detail"]`, eles quebrarão. 
  - **Mitigação:** Manteremos `detail` como uma chave para suportar clientes legados indiretamente, mas como a estrutura muda (adicionando `title`, `status`), qualquer parse manual precisará saber do formato RFC 7807, o que é um padrão do mercado.
