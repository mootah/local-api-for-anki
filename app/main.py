import logging
from pathlib import Path
import uvicorn
from prometheus_client import multiprocess, CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.responses import Response
from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import (HOST, PORT)

DB_PATH = Path(__file__).parent / "data" / "ipa.db"

logger = logging.getLogger("uvicorn")

app = FastAPI(title="Local API for Anki")

@app.on_event("startup")
def check_db():
    if not DB_PATH.exists():
        logger.error("Database not found. Please run 'uv run task init-db' to initialize the database.")

app.include_router(api_router)

Instrumentator().instrument(app)

@app.get("/metrics")
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    data = generate_latest(registry)
    return Response(data, media_type=CONTENT_TYPE_LATEST)
