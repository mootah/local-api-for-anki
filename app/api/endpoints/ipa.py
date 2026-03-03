from fastapi import APIRouter, HTTPException, Query
from app.schemas.ipa import IPARecord, IPACreate, IPAUpdate, IPASearchResult
from app.services import ipa as ipa_service

router = APIRouter()

@router.post("/", response_model=IPARecord)
async def create_ipa(ipa: IPACreate):
    success = await ipa_service.create_ipa(ipa.word, ipa.ipa)
    if not success:
        raise HTTPException(status_code=400, detail="Word already exists")
    return ipa

@router.get("/{word}", response_model=IPARecord)
async def get_ipa(word: str):
    record = await ipa_service.get_ipa_record(word)
    if not record:
        raise HTTPException(status_code=404, detail="Word not found")
    return IPARecord(**record)

@router.put("/{word}", response_model=IPARecord)
async def update_ipa(word: str, ipa: IPAUpdate):
    success = await ipa_service.update_ipa(word, ipa.ipa)
    if not success:
        raise HTTPException(status_code=404, detail="Word not found")
    return IPARecord(word=word, ipa=ipa.ipa)

@router.delete("/{word}")
async def delete_ipa(word: str):
    success = await ipa_service.delete_ipa(word)
    if not success:
        raise HTTPException(status_code=404, detail="Word not found")
    return {"message": "Deleted successfully"}

@router.get("/search", response_model=IPASearchResult)
async def search_ipa(
    q: str = Query(..., description="Regex query for word"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    results, total = await ipa_service.search_ipa(q, limit, offset)
    return IPASearchResult(
        results=[IPARecord(**r) for r in results],
        total=total,
        limit=limit,
        offset=offset
    )

