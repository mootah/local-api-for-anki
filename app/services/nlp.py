import json
from functools import lru_cache
import spacy
from typing import List
from fastapi import HTTPException
from pydantic import ValidationError
from app.schemas.yomitan import (
    ScanResult, TokenReading, TermEntriesResponse, TermSource, Headword, DictionaryEntry, Frequency,
    TokenizeRequest, TermEntriesRequest
)
from app.services.text import sanitize_text
from app.services.ipa import get_word_pronunciations
from app.services.freq import get_frequency_score

# Load the spaCy model
nlp_tokenizer = spacy.blank("en")
try:
    # nlp = spacy.load("en_core_web_sm")
    nlp_lemmatizer = spacy.load("en_core_web_sm", disable=["parser", "ner"])
except OSError:
    # Fallback if the model is not found
    from spacy.cli.download import download as spacy_download
    spacy_download("en_core_web_sm")
    # nlp = spacy.load("en_core_web_sm")
    nlp_lemmatizer = spacy.load("en_core_web_sm", disable=["parser", "ner"])

async def tokenize_single_text(text: str, index: int) -> ScanResult:
    text = sanitize_text(text)
    doc = nlp_tokenizer.make_doc(text)
    content = []
    for token in doc:
        # Use token.text to maintain original inflection
        # ipa_list = await get_word_pronunciations(token.text)
        # reading = ipa_list[0] if ipa_list else ""
        # content.append([TokenReading(text=token.text, reading=reading)])
        content.append([TokenReading(text=token.text, reading="")])
        if token.whitespace_:
            content.append([TokenReading(text=" ", reading="")])

    return ScanResult(
        index=index,
        content=content
    )

async def tokenize_text(body_bytes: bytes) -> List[ScanResult]:
    try:
        data = json.loads(body_bytes)
        tokenize_request = TokenizeRequest.model_validate(data)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=422, detail=f"Invalid JSON: {str(e)}")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    if isinstance(tokenize_request.text, str):
        return [await tokenize_single_text(tokenize_request.text, 0)]
    else:
        results = []
        for i, t in enumerate(tokenize_request.text):
            results.append(await tokenize_single_text(t, i))
        return results

async def get_term_entries(body_bytes: bytes) -> TermEntriesResponse:
    try:
        data = json.loads(body_bytes)
        term_request = TermEntriesRequest.model_validate(data)
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=422, detail=f"Invalid JSON: {str(e)}")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))

    originalText = term_request.term
    doc = nlp_lemmatizer(originalText.lower())
    dictionary_entries = []

    for token in doc:
        if token.is_space:
            continue

        source = TermSource(
            originalText=originalText,
            transformedText=token.text,
            deinflectedText=token.lemma_,
            matchType="exact",
            matchSource="term",
            isPrimary=True
        )

        ipa_list = await get_word_pronunciations(token.text)
        reading = ipa_list[0] if ipa_list else ""
        headword = Headword(
            index=0,
            term=token.text,
            reading=reading,
            sources=[source],
            tags=[],
            wordClasses=[token.pos_]
        )

        pronunciations = [{"index": i, "pronunciation": p} for i, p in enumerate(ipa_list)]

        freq_score = get_frequency_score(token.text)
        frequencies = [
            Frequency(
                index=0,
                headwordIndex=0,
                dictionary="WordFreq",
                dictionaryIndex=0,
                dictionaryAlias="WordFreq",
                hasReading=True,
                frequency=float(freq_score),
                displayValue=freq_score,
                displayValueParsed=False
            )
        ]

        entry = DictionaryEntry(
            type="term",
            isPrimary=True,
            textProcessorRuleChainCandidates=[[]],
            inflectionRuleChainCandidates=[],
            score=0,
            frequencyOrder=0,
            dictionaryIndex=0,
            dictionaryAlias="spaCy",
            sourceTermExactMatchCount=1,
            matchPrimaryReading=False,
            maxOriginalTextLength=len(originalText),
            headwords=[headword],
            definitions=[],
            frequencies=frequencies,
            pronunciations=pronunciations
        )
        dictionary_entries.append(entry)

    return TermEntriesResponse(
        dictionaryEntries=dictionary_entries,
        originalTextLength=len(originalText)
    )
