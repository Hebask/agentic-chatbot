from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.exceptions import NotFoundError, ValidationError
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdateStatus
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)) -> TaskResponse:
    try:
        service = TaskService(db)
        return service.create_task(payload.title, payload.description)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    status: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[TaskResponse]:
    try:
        service = TaskService(db)
        return service.list_tasks(status=status)
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.patch("/{task_id}/status", response_model=TaskResponse)
def update_task_status(
    task_id: int,
    payload: TaskUpdateStatus,
    db: Session = Depends(get_db),
) -> TaskResponse:
    try:
        service = TaskService(db)
        return service.update_task_status(task_id, payload.status)
    except NotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc