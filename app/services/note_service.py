from sqlalchemy.orm import Session

from app.db.models import Note
from app.repositories.note_repository import NoteRepository


class NoteService:
    def __init__(self, db: Session) -> None:
        self.repo = NoteRepository(db)

    def save_note(
        self,
        content: str,
        tags: str | None = None,
        is_important: bool = False,
    ) -> Note:
        cleaned_content = content.strip()
        if not cleaned_content:
            raise ValueError("Note content cannot be empty")
        return self.repo.create(
            content=cleaned_content,
            tags=tags,
            is_important=is_important,
        )

    def search_notes(self, query: str) -> list[Note]:
        cleaned_query = query.strip()
        if not cleaned_query:
            raise ValueError("Search query cannot be empty")
        return self.repo.search(cleaned_query)