import json
from types import SimpleNamespace


class FakeLLMCreateTask:
    def create_initial_response(self, messages):
        return SimpleNamespace(
            id="resp_1",
            output=[
                SimpleNamespace(
                    type="function_call",
                    name="create_task",
                    call_id="call_1",
                    arguments=json.dumps(
                        {
                            "title": "submit assignment",
                            "description": "final project submission",
                        }
                    ),
                )
            ],
        )

    def continue_with_tool_output(self, previous_response_id, tool_call_id, tool_output):
        return SimpleNamespace(
            id="resp_2",
            output=[],
            output_text="Done — I created the task 'submit assignment'.",
        )

    @staticmethod
    def extract_text(response):
        return getattr(response, "output_text", "").strip()


class FakeLLMListTasks:
    def create_initial_response(self, messages):
        return SimpleNamespace(
            id="resp_3",
            output=[
                SimpleNamespace(
                    type="function_call",
                    name="list_tasks",
                    call_id="call_2",
                    arguments=json.dumps({}),
                )
            ],
        )

    def continue_with_tool_output(self, previous_response_id, tool_call_id, tool_output):
        parsed = json.loads(tool_output)
        task_count = len(parsed)
        return SimpleNamespace(
            id="resp_4",
            output=[],
            output_text=f"I found {task_count} task(s) in your list.",
        )

    @staticmethod
    def extract_text(response):
        return getattr(response, "output_text", "").strip()


class FakeLLMInvalidToolArgs:
    def create_initial_response(self, messages):
        return SimpleNamespace(
            id="resp_5",
            output=[
                SimpleNamespace(
                    type="function_call",
                    name="create_task",
                    call_id="call_3",
                    arguments="{invalid_json}",
                )
            ],
        )

    def continue_with_tool_output(self, previous_response_id, tool_call_id, tool_output):
        raise AssertionError("This should not be called for invalid tool arguments")

    @staticmethod
    def extract_text(response):
        return getattr(response, "output_text", "").strip()


def test_chat_creates_task_via_agent(monkeypatch, client) -> None:
    from app.services import agent_service

    monkeypatch.setattr(agent_service, "LLMService", FakeLLMCreateTask)

    response = client.post(
        "/chat",
        json={
            "message": "Create a task called submit assignment",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["reply"] == "Done — I created the task 'submit assignment'."
    assert isinstance(data["conversation_id"], int)

    tasks_response = client.get("/tasks")
    assert tasks_response.status_code == 200
    tasks_data = tasks_response.json()
    assert isinstance(tasks_data, list)
    assert len(tasks_data) >= 1
    assert any(task["title"] == "submit assignment" for task in tasks_data)


def test_chat_lists_tasks_via_agent(monkeypatch, client) -> None:
    create_task_response = client.post(
        "/tasks",
        json={
            "title": "prepare demo",
            "description": "demo for final assessment",
        },
    )
    assert create_task_response.status_code == 200

    from app.services import agent_service

    monkeypatch.setattr(agent_service, "LLMService", FakeLLMListTasks)

    response = client.post(
        "/chat",
        json={
            "message": "List all my tasks",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert "task" in data["reply"].lower()
    assert isinstance(data["conversation_id"], int)


def test_chat_persists_conversation_messages(monkeypatch, client) -> None:
    from app.services import agent_service

    monkeypatch.setattr(agent_service, "LLMService", FakeLLMCreateTask)

    response = client.post(
        "/chat",
        json={
            "message": "Create a task called submit assignment",
        },
    )

    assert response.status_code == 200
    conversation_id = response.json()["conversation_id"]

    messages_response = client.get(f"/chat/conversations/{conversation_id}")
    assert messages_response.status_code == 200
    messages_data = messages_response.json()

    assert messages_data["conversation_id"] == conversation_id
    assert len(messages_data["messages"]) >= 2
    assert messages_data["messages"][0]["role"] == "user"
    assert messages_data["messages"][1]["role"] == "assistant"


def test_chat_returns_error_for_invalid_tool_arguments(monkeypatch, client) -> None:
    from app.services import agent_service

    monkeypatch.setattr(agent_service, "LLMService", FakeLLMInvalidToolArgs)

    response = client.post(
        "/chat",
        json={
            "message": "Create a broken task",
        },
    )

    assert response.status_code == 400
    assert "Invalid tool arguments returned by model" in response.json()["detail"]
