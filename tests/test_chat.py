from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_conversation() -> None:
    response = client.post("/chat/conversations")
    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert isinstance(data["conversation_id"], int)


def test_list_conversations() -> None:
    client.post("/chat/conversations")
    response = client.get("/chat/conversations")
    assert response.status_code == 200
    data = response.json()
    assert "conversations" in data
    assert isinstance(data["conversations"], list)


def test_get_empty_conversation_messages() -> None:
    create_response = client.post("/chat/conversations")
    conversation_id = create_response.json()["conversation_id"]

    response = client.get(f"/chat/conversations/{conversation_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["conversation_id"] == conversation_id
    assert isinstance(data["messages"], list)