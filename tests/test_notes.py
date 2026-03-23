from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_note() -> None:
    response = client.post(
        "/notes",
        json={"content": "This is a test note", "tags": "test", "is_important": True},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "This is a test note"
    assert data["is_important"] is True