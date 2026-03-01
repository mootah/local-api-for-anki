from fastapi import APIRouter
from app.schemas.fastwq import FastWQResponse
from app.services.ipa import get_ipa_for_term, get_ipa_for_sentence
from app.services.cefr import get_cefr_level
from app.services.freq import get_frequency_score

router = APIRouter()

@router.get("/fastwq/{query}", response_model=FastWQResponse)
async def fast_word_query(query: str):
    """
    API endpoint for Anki Fast Word Query.
    Returns IPA, CEFR level, and frequency score for the given query.
    """
    return FastWQResponse(
        query=query,
        ipa_word=get_ipa_for_term(query),
        ipa_sentence=get_ipa_for_sentence(query),
        cefr=get_cefr_level(query),
        frequency=get_frequency_score(query)
    )
