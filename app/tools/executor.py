from sqlalchemy.orm import Session

from app.services.note_service import NoteService
from app.services.task_service import TaskService


class ToolExecutor:
    def __init__(self, db: Session) -> None:
        self.task_service = TaskService(db)
        self.note_service = NoteService(db)

    def execute(self, tool_name: str, arguments: dict) -> dict:
        if tool_name == "create_task":
            task = self.task_service.create_task(
                title=arguments["title"],
                description=arguments.get("description"),
            )
            return {
                "success": True,
                "tool": tool_name,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                },
            }

        if tool_name == "list_tasks":
            tasks = self.task_service.list_tasks()
            return {
                "success": True,
                "tool": tool_name,
                "tasks": [
                    {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "status": task.status,
                        "created_at": task.created_at.isoformat(),
                    }
                    for task in tasks
                ],
            }

        if tool_name == "update_task_status":
            task = self.task_service.update_task_status(
                task_id=arguments["task_id"],
                status=arguments["status"],
            )
            return {
                "success": True,
                "tool": tool_name,
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "created_at": task.created_at.isoformat(),
                },
            }

        if tool_name == "save_note":
            note = self.note_service.save_note(
                content=arguments["content"],
                tags=arguments.get("tags"),
                is_important=arguments.get("is_important", False),
            )
            return {
                "success": True,
                "tool": tool_name,
                "note": {
                    "id": note.id,
                    "content": note.content,
                    "tags": note.tags,
                    "is_important": note.is_important,
                    "created_at": note.created_at.isoformat(),
                },
            }

        if tool_name == "search_notes":
            notes = self.note_service.search_notes(arguments["query"])
            return {
                "success": True,
                "tool": tool_name,
                "notes": [
                    {
                        "id": note.id,
                        "content": note.content,
                        "tags": note.tags,
                        "is_important": note.is_important,
                        "created_at": note.created_at.isoformat(),
                    }
                    for note in notes
                ],
            }

        raise ValueError(f"Unknown tool: {tool_name}")