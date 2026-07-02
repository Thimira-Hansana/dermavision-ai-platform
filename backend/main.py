"""FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.db.session import init_db
from backend.api.routes.health import router as health_router
from backend.api.routes.history import router as history_router
from backend.api.routes.predict import router as predict_router
from backend.api.routes.system import router as system_router
from dermavision_ai.core.logging import configure_logging
from dermavision_ai.core.settings import get_settings


@asynccontextmanager
async def lifespan(_app: FastAPI):
    configure_logging()
    await init_db()
    yield


settings = get_settings()
app = FastAPI(
    title="DermaVision AI API",
    version="0.1.0",
    description="Explainable skin lesion classification backend.",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

outputs_dir = Path("outputs")
outputs_dir.mkdir(parents=True, exist_ok=True)
app.mount("/outputs", StaticFiles(directory=str(outputs_dir)), name="outputs")

app.include_router(health_router)
app.include_router(system_router)
app.include_router(predict_router)
app.include_router(history_router)
