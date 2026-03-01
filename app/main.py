import uvicorn
from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="Morph API")

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=19634, log_level="debug")
