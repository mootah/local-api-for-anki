import uvicorn
from fastapi import FastAPI
from app.api.router import api_router
from app.core.config import (HOST, PORT)

app = FastAPI(title="Local API for Anki")

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT, log_level="debug")
