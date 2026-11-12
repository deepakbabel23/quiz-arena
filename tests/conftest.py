import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("QUIZ_ARENA_DB", str(tmp_path / "test.db"))
    from app.main import app

    with TestClient(app) as test_client:
        yield test_client
