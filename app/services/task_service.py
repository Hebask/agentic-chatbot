from sqlalchemy.orm import Session

from app.repositories.task_repository import TaskRepository
from app.db.models import Task


class TaskService:
    ALLOWED_STATUSES = {"pending", "in_progress", "completed"}

    def __init__(self, db: Session) -> None:
        self.repo = TaskRepository(db)

    def create_task(self, title: str, description: str | None = None) -> Task:
        return self.repo.create(title=title, description=description)

    def list_tasks(self) -> list[Task]:
        return self.repo.list_all()

    def update_task_status(self, task_id: int, status: str) -> Task:
        normalized_status = status.strip().lower()
        if normalized_status not in self.ALLOWED_STATUSES:
            raise ValueError(
                f"Invalid status '{status}'. Allowed: {sorted(self.ALLOWED_STATUSES)}"
            )

        task = self.repo.get_by_id(task_id)
        if not task:
            raise ValueError(f"Task with id {task_id} not found")

        return self.repo.update_status(task, normalized_status)