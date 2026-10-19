# Testing Python

- `pytest` with plain `assert`; fixtures for setup; parametrize edge cases; name tests by behavior.
- API tests through the real app with `httpx`/TestClient (`httpx.AsyncClient(transport=httpx.ASGITransport(app=app),
  base_url="http://testserver")` for async); httpx does not run ASGI lifespan events, so wrap startup/shutdown with
  `asgi-lifespan`'s `LifespanManager`. Override dependencies for auth and time, not for the code under test.
- Database: a real Postgres (testcontainers or a test database) beats SQLite for Postgres features; roll back
  per test or truncate; factories (factory_boy or plain functions) over giant fixtures.
- Async: the repo's plugin (`pytest-asyncio` or `anyio`); do not mix runners. pytest-asyncio defaults to strict
  mode (needs `@pytest.mark.asyncio` and `@pytest_asyncio.fixture`); `asyncio_mode = "auto"` removes that and is
  the simplest choice when asyncio is the only async library.
- Mock only external boundaries (HTTP, email, clock). Never mock the thing under test.
- Cover the error paths the contract lists and the edge cases from the brief; show red before green.
