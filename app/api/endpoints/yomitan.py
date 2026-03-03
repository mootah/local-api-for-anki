from fastapi import APIRouter, Request, HTTPException
from typing import List
from app.schemas.yomitan import ScanResult, TermEntriesResponse, TokenizeRequest, TermEntriesRequest
from app.services.nlp import tokenize_text, get_term_entries
from app.core.config import SERVER_VER, YOMITAN_VER

router = APIRouter()

@router.post("/serverVersion")
async def server_version():
    return {"version": SERVER_VER}

@router.post("/yomitanVersion")
async def yomitan_version():
    return {"version": YOMITAN_VER}

@router.post(
    "/tokenize",
    response_model=List[ScanResult],
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": TokenizeRequest.model_json_schema()
                },
                "application/octet-stream": {
                    "schema": {"type": "string", "format": "binary"},
                    "description": "JSON bytes to tokenize (must match TokenizeRequest schema)"
                }
            }
        }
    }
)
async def tokenize(request: Request) -> List[ScanResult]:
    body = await request.body()
    if not body:
        raise HTTPException(status_code=422, detail="Empty body")
    return await tokenize_text(body)

@router.post(
    "/termEntries",
    response_model=TermEntriesResponse,
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "schema": TermEntriesRequest.model_json_schema()
                },
                "application/octet-stream": {
                    "schema": {"type": "string", "format": "binary"},
                    "description": "JSON bytes of the term (must match TermEntriesRequest schema)"
                }
            }
        }
    }
)
async def term_entries(request: Request) -> TermEntriesResponse:
    body = await request.body()
    if not body:
        raise HTTPException(status_code=422, detail="Empty body")
    return await get_term_entries(body)
