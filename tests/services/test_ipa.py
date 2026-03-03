import pytest
from app.services.ipa import get_word_pronunciations

@pytest.mark.asyncio
async def test_get_word_pronunciations_existing():
    # 'bout is in the dictionary as 'bout\t/ˈbaʊt/
    pronunciations = await get_word_pronunciations("'bout")
    assert "ˈbaʊt" in pronunciations
    assert "/" not in pronunciations[0]

@pytest.mark.asyncio
async def test_get_word_pronunciations_non_existent():
    assert await get_word_pronunciations("thisisnotaword") == []

@pytest.mark.asyncio
async def test_get_word_pronunciations_punctuation():
    assert await get_word_pronunciations(".") == []
    assert await get_word_pronunciations("!") == []
    assert await get_word_pronunciations(" ") == []

@pytest.mark.asyncio
async def test_get_word_pronunciations_case_insensitive():
    # 'bout is stored as 'bout (lowercase in the dict loading)
    assert await get_word_pronunciations("'BOUT") == ["ˈbaʊt"]
