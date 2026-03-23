from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.note import NoteCreate, NoteResponse
from app.services.note_service import NoteService

router = APIRouter(prefix="/notes", tags=["notes"])


@router.post("", response_model=NoteResponse)
def create_note(payload: NoteCreate, db: Session = Depends(get_db)) -> NoteResponse:
    service = NoteService(db)
    return service.save_note(
        content=payload.content,
        tags=payload.tags,
        is_important=payload.is_important,
    )


@router.get("/search", response_model=list[NoteResponse])
def search_notes(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
) -> list[NoteResponse]:
    service = NoteService(db)
    return service.search_notes(q)