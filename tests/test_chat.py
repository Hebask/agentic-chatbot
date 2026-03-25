def test_create_conversation(client) -> None:
    response = client.post(
        "/chat/conversations",
        json={"title": "Test Conversation"},
    )
    assert response.status_code == 200
    data = response.json()

    assert "conversation_id" in data
    assert isinstance(data["conversation_id"], int)


def test_list_conversations(client) -> None:
    client.post("/chat/conversations", json={"title": "Conversation A"})

    response = client.get("/chat/conversations")
    assert response.status_code == 200
    data = response.json()

    assert "conversations" in data
    assert isinstance(data["conversations"], list)
    assert len(data["conversations"]) >= 1


def test_get_conversation_messages_empty(client) -> None:
    create_response = client.post("/chat/conversations", json={"title": "Empty Chat"})
    conversation_id = create_response.json()["conversation_id"]

    response = client.get(f"/chat/conversations/{conversation_id}")
    assert response.status_code == 200
    data = response.json()

    assert data["conversation_id"] == conversation_id
    assert data["messages"] == []
