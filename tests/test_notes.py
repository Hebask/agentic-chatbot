def test_create_and_search_note(client) -> None:
    create_response = client.post(
        "/notes",
        json={
            "title": "Meeting Notes",
            "content": "Discussed FastAPI architecture and agent workflow",
        },
    )
    assert create_response.status_code == 200

    search_response = client.get("/notes/search?q=FastAPI")
    assert search_response.status_code == 200
    data = search_response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any("FastAPI" in note["content"] for note in data)
