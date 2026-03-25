def test_create_and_list_tasks(client) -> None:
    create_response = client.post(
        "/tasks",
        json={
            "title": "Write report",
            "description": "Prepare final submission report",
        },
    )
    assert create_response.status_code == 200

    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    data = list_response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert any(task["title"] == "Write report" for task in data)


def test_update_task_status(client) -> None:
    create_response = client.post(
        "/tasks",
        json={
            "title": "Prepare slides",
            "description": "Create project presentation",
        },
    )
    task_id = create_response.json()["id"]

    update_response = client.patch(
        f"/tasks/{task_id}/status",
        json={"status": "completed"},
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["status"] == "completed"
