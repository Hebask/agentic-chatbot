from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError, ValidationError
from app.db.models import Task
from app.repositories.task_repository import TaskRepository


class TaskService:
    ALLOWED_STATUSES = {"pending", "in_progress", "completed"}

    def __init__(self, db: Session) -> None:
        self.repo = TaskRepository(db)

    def create_task(self, title: str, description: str | None = None) -> Task:
        cleaned_title = title.strip()
        if not cleaned_title:
            raise ValidationError("Task title cannot be empty")
        return self.repo.create(title=cleaned_title, description=description)

    def list_tasks(self, status: str | None = None) -> list[Task]:
        if status is None:
            return self.repo.list_all()

        normalized_status = status.strip().lower()
        if normalized_status not in self.ALLOWED_STATUSES:
            raise ValidationError(
                f"Invalid status '{status}'. Allowed values: {sorted(self.ALLOWED_STATUSES)}"
            )

        return self.repo.list_by_status(normalized_status)

    def update_task_status(self, task_id: int, status: str) -> Task:
        normalized_status = status.strip().lower()
        if normalized_status not in self.ALLOWED_STATUSES:
            raise ValidationError(
                f"Invalid status '{status}'. Allowed values: {sorted(self.ALLOWED_STATUSES)}"
            )

        task = self.repo.get_by_id(task_id)
        if not task:
            raise NotFoundError(f"Task with id {task_id} not found")

        return self.repo.update_status(task, normalized_status)
