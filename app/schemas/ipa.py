from pydantic import BaseModel
from typing import List, Optional

class IPARecord(BaseModel):
    word: str
    ipa: str

class IPACreate(IPARecord):
    pass

class IPAUpdate(BaseModel):
    ipa: str

class IPASearchResult(BaseModel):
    results: List[IPARecord]
    total: int
    limit: int
    offset: int
