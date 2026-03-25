import pytest
from fastapi.testclient import TestClient

from app.main import app


def pytest_configure():
    """
    Shared pytest configuration hook.
    Kept here so future global test setup can be added in one place.
    """
    return None


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
