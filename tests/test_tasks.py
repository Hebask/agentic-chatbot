from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_task() -> None:
    response = client.post(
        "/tasks",
        json={"title": "Finish final assessment", "description": "Complete FastAPI chatbot project"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Finish final assessment"
    assert data["status"] == "pending"