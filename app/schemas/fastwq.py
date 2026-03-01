from pydantic import BaseModel

class FastWQResponse(BaseModel):
    query: str
    ipa_word: str
    ipa_sentence: str
    cefr: str
    frequency: str
