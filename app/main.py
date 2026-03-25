from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.routes import auth, chat, health, notes, tasks
from app.core.config import get_settings
from app.core.exceptions import AppException
from app.core.logging import setup_logging
from app.db.init_db import init_db

setup_logging()
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.exception_handler(AppException)
async def app_exception_handler(_, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


app.include_router(health.router)
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(tasks.router)
app.include_router(notes.router)