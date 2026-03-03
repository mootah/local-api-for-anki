from pydantic import BaseModel
from typing import List, Union, Optional

class TokenizeRequest(BaseModel):
    text: Union[str, List[str]]
    scanLength: int

class TermEntriesRequest(BaseModel):
    term: str

class TermSource(BaseModel):
    originalText: str
    transformedText: str
    deinflectedText: str
    matchType: str
    matchSource: str
    isPrimary: bool

class Headword(BaseModel):
    index: int
    term: str
    reading: str
    sources: List[TermSource]
    tags: List[dict]
    wordClasses: List[str]

class Frequency(BaseModel):
    index: int
    headwordIndex: int
    dictionary: str
    dictionaryIndex: int
    dictionaryAlias: str
    hasReading: bool
    frequency: Union[int, float]
    displayValue: str
    displayValueParsed: bool

class DictionaryEntry(BaseModel):
    type: str
    isPrimary: bool
    textProcessorRuleChainCandidates: List[List[str]]
    inflectionRuleChainCandidates: List[dict]
    score: int
    frequencyOrder: int
    dictionaryIndex: int
    dictionaryAlias: str
    sourceTermExactMatchCount: int
    matchPrimaryReading: bool
    maxOriginalTextLength: int
    headwords: List[Headword]
    definitions: List[dict]
    frequencies: List[Frequency]
    pronunciations: List[dict]

class TermEntriesResponse(BaseModel):
    dictionaryEntries: List[DictionaryEntry]
    originalTextLength: int

class TokenReading(BaseModel):
    text: str
    reading: str

class ScanResult(BaseModel):
    id: str = "scan"
    source: str = "scanning-parser"
    dictionary: Optional[str] = None
    index: int
    content: List[List[TokenReading]]
