from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.models import Note


class NoteRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, content: str, tags: str | None = None, is_important: bool = False) -> Note:
        note = Note(content=content, tags=tags, is_important=is_important)
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    def search(self, query: str) -> list[Note]:
        return (
            self.db.query(Note)
            .filter(
                or_(
                    Note.content.ilike(f"%{query}%"),
                    Note.tags.ilike(f"%{query}%"),
                )
            )
            .order_by(Note.created_at.desc())
            .all()
        )
