import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.routes.chat import router as chat_router
from app.api.routes.health import router as health_router
from app.api.routes.notes import router as notes_router
from app.api.routes.tasks import router as tasks_router
from app.core.config import settings
from app.core.exceptions import AppError, NotFoundError, ValidationError
from app.core.logging import setup_logging
from app.db.init_db import init_db

setup_logging()
init_db()

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    debug=settings.app_debug,
)


@app.exception_handler(NotFoundError)
async def not_found_exception_handler(_: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ValidationError)
async def validation_exception_handler(_: Request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(AppError)
async def app_exception_handler(_: Request, exc: AppError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.exception_handler(Exception)
async def unhandled_exception_handler(_: Request, exc: Exception):
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})


app.include_router(health_router)
app.include_router(tasks_router)
app.include_router(notes_router)
app.include_router(chat_router)
