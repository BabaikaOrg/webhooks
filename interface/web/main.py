import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import init_app

from .routes.mailgun import router as mailgun_router
from .routes.status import router as status_router

log = logging.getLogger(__name__)

SENTRY_ENABLED = os.environ.get("SENTRY_ENABLED", "false").lower() == "true"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Entry point lifecycle event. Runs before the server starts"""
    try:
        await init_app()
        app.include_router(status_router, prefix="")
        app.include_router(mailgun_router, prefix="/mailgun")
    except Exception as e:
        log.exception(f"Failed to initialize webql service: {e}")
        raise e
    yield
    # If there is any cleanup needed it would go here


def create_app() -> FastAPI:
    """Create FastAPI app with all routes."""
    try:
        root_api = FastAPI(lifespan=lifespan)
    except Exception as e:
        log.exception(f"Failed to create webql service: {e}")
        raise e
    return root_api
