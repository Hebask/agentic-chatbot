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


def test_list_tasks_with_status_filter() -> None:
    client.post("/tasks", json={"title": "Task pending"})
    created = client.post("/tasks", json={"title": "Task completed"})
    task_id = created.json()["id"]

    update_response = client.patch(
        f"/tasks/{task_id}/status",
        json={"status": "completed"},
    )
    assert update_response.status_code == 200

    filtered = client.get("/tasks", params={"status": "completed"})
    assert filtered.status_code == 200
    assert isinstance(filtered.json(), list)