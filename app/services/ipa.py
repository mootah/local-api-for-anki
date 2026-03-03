import re
from functools import lru_cache
from pathlib import Path
from app.services.text import sanitize_text

def load_ipa_dict():
    ipa_dict = {}
    # https://github.com/open-dict-data/ipa-dict
    ipa_dict_file = Path(__file__).parent.parent / "data" / "en_US.txt"
    try:
        with open(ipa_dict_file, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    word = parts[0].lower()
                    pronunciations = parts[1]
                    # Remove outer slashes and split by ', '
                    pronunciations = pronunciations.replace("/", "").split(", ")
                    ipa_dict[word] = pronunciations
    except FileNotFoundError:
        # Fallback or log error
        pass
    return ipa_dict

# Load the file once per server start
IPA_DICT = load_ipa_dict()

@lru_cache(maxsize=1024)
def get_word_pronunciations(word: str):
    """
    Returns a list of IPA pronunciations for a given word,
    with slashes removed. Returns an empty list if not found.
    """
    if not word or not any(c.isalnum() for c in word):
        return []

    lower_word = word.lower()
    ipa = None
    # Create candidates based on word ending
    candidates = []
    if lower_word.endswith(("'s", "s'")):
        candidates = [
            lower_word,
            lower_word.replace("'", ""),
            lower_word[:-2]   # remove 's
        ]
    elif lower_word.endswith((".", ",")):
        candidates = [
            lower_word,
            lower_word[:-1]
        ]
    else:
        candidates = [lower_word]

    # Check IPA_DICT
    for candidate in candidates:
        ipa = IPA_DICT.get(candidate)
        if ipa:
            break

    return ipa if ipa is not None else []

@lru_cache(maxsize=1024)
def get_ipa(text):
    text = sanitize_text(text)
    words = re.findall(r"\b[\w'.,]+", text)
    ipa_parts = []
    for word in words:
        ipa = get_word_pronunciations(word)

        # Fallback
        if not ipa:
            ipa = [word]
        ipa_parts.append(ipa)

    return ipa_parts

@lru_cache(maxsize=1024)
def get_ipa_for_term(term):
    ipa_parts = get_ipa(term)
    if not ipa_parts:
        return ""

    if len(ipa_parts) == 1:
        return " ".join(f"/{i}/" for i in ipa_parts[0])
    else:
        # For multiple words, take the first pronunciation of each word
        return "/" + " ".join(i[0] for i in ipa_parts) + "/"

@lru_cache(maxsize=1024)
def get_ipa_for_sentence(sentence):
    ipa_parts = get_ipa(sentence)
    if not ipa_parts:
        return ""

    return " ".join(i[0] for i in ipa_parts)
