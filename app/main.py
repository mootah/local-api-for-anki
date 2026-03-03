import sys
from pathlib import Path
import uvicorn
from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import (HOST, PORT)

DB_PATH = Path(__file__).parent / "data" / "ipa.db"

if not DB_PATH.exists():
    print("Database not found. Please run 'uv run task init-db' to initialize the database.")
    sys.exit(1)

app = FastAPI(title="Local API for Anki")

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, log_level="debug")
