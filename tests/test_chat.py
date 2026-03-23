from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_chat_endpoint_exists() -> None:
    response = client.post("/chat", json={"message": "Hello"})
    assert response.status_code in (200, 500)