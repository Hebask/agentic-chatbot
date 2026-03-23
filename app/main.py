from fastapi import FastAPI

from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.notes import router as notes_router
from app.api.routes.tasks import router as tasks_router
from app.core.config import settings
from app.core.logging import setup_logging
from app.db.init_db import init_db

setup_logging()
init_db()

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
)


app.include_router(health_router)
app.include_router(tasks_router)
app.include_router(notes_router)
app.include_router(chat_router)