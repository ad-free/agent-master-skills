# Contract-first workflow

Folded from the former `api-contract-designer` skill. Use after the decision tree has chosen the style, when
frontend and backend (or two services) must agree before either side builds.

## 1. Write the contract

Use the format the repo already uses (OpenAPI 3.1, GraphQL SDL, Protobuf, or shared TypeScript/Pydantic types).
For every operation define:

- path / operation name, method, request body, path/query/header params
- response schema for each status the client must handle (200/201, 400, 401, 403, 404, 409, 422, 500)
- one error envelope shared by every endpoint (match the project's existing one)
- auth scheme, pagination (cursor vs offset), filtering and sorting params
- consumers: who calls it, and what breaks for them if the field changes

## 2. Generate, don't hand-copy

- Client types from the spec (`openapi-typescript`, GraphQL codegen, or the backend's schema export).
- Runtime validation from the same source (Zod / Pydantic), so the boundary checks what the types promise.
- Mocks from the spec (MSW, Prism) with scenarios for success, each error, empty, and slow responses.

## 3. Validate

- Lint the spec (Spectral or `swagger-parser`; GraphQL schema validation).
- Contract test: mocks and real responses both validate against the schema.
- Both sides review the contract before implementation starts.

## 4. Change it safely

- Additive changes are safe; removing or renaming a field, or narrowing a type, is breaking.
- Breaking change: new version or a deprecation window, consumers listed and told, types and mocks regenerated.
