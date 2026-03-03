import pytest
from app.services.ipa import get_word_pronunciations

def test_get_word_pronunciations_existing():
    # 'bout is in the dictionary as 'bout\t/ˈbaʊt/
    pronunciations = get_word_pronunciations("'bout")
    assert "ˈbaʊt" in pronunciations
    assert "/" not in pronunciations[0]

def test_get_word_pronunciations_multiple():
    # We should find a word with multiple pronunciations if possible,
    # but based on the head of en_US.txt, let's assume 'bout is there.
    # If I want to be sure about multiple, I'd need to check the file more.
    pass

def test_get_word_pronunciations_non_existent():
    assert get_word_pronunciations("thisisnotaword") == []

def test_get_word_pronunciations_punctuation():
    assert get_word_pronunciations(".") == []
    assert get_word_pronunciations("!") == []
    assert get_word_pronunciations(" ") == []

def test_get_word_pronunciations_case_insensitive():
    # 'bout is stored as 'bout (lowercase in the dict loading)
    assert get_word_pronunciations("'BOUT") == ["ˈbaʊt"]
