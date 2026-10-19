# Testing Python

- `pytest` with plain `assert`; fixtures for setup; parametrize edge cases; name tests by behavior.
- API tests through the real app with `httpx`/TestClient (`ASGITransport` for async); override dependencies for
  auth and time, not for the code under test.
- Database: a real Postgres (testcontainers or a test database) beats SQLite for Postgres features; roll back
  per test or truncate; factories (factory_boy or plain functions) over giant fixtures.
- Async: the repo's plugin (`pytest-asyncio` or `anyio`); do not mix runners.
- Mock only external boundaries (HTTP, email, clock). Never mock the thing under test.
- Cover the error paths the contract lists and the edge cases from the brief; show red before green.
