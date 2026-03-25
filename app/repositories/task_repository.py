from sqlalchemy.orm import Session

from app.db.models import Task


class TaskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, title: str, description: str | None = None) -> Task:
        task = Task(title=title, description=description)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def list_all(self) -> list[Task]:
        return self.db.query(Task).order_by(Task.created_at.desc(), Task.id.desc()).all()

    def list_by_status(self, status: str) -> list[Task]:
        return (
            self.db.query(Task)
            .filter(Task.status == status)
            .order_by(Task.created_at.desc(), Task.id.desc())
            .all()
        )

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def update_status(self, task: Task, status: str) -> Task:
        task.status = status
        self.db.commit()
        self.db.refresh(task)
        return task
