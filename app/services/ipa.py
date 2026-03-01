import re
from app.services.text import sanitize_text

def load_ipa_dict():
    ipa_dict = {}
    # https://github.com/open-dict-data/ipa-dict
    # TODO: use "app/data/en_US.txt"
    ipa_dict_file = ""
    with open(ipa_dict_file, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                word = parts[0].lower()
                pronunciations = parts[1]
                # Remove outer slashes and split by ', '
                pronunciations = pronunciations.replace("/", "").split(", ")
                ipa = pronunciations
                ipa_dict[word] = ipa
    return ipa_dict

# TODO: load the file only once per server
IPA_DICT = load_ipa_dict()

def get_ipa(text):
    text = sanitize_text(text)
    words = re.findall(r"\b[\w'.,]+", text)
    ipa_parts = []
    for word in words:
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
        if ipa is None:
            for candidate in candidates:
                ipa = IPA_DICT.get(candidate)
                if ipa:
                    break
        # Fallback
        if ipa is None:
            ipa = [word]
        ipa_parts.append(ipa)

    return ipa_parts
    
def get_ipa_for_term(term):
    ipa_parts = get_ipa(term)

    if len(ipa_parts) == 1:
        return " ".join(f"/{i}/" for i in ipa_parts[0])
    else:
        return "/" + " ".join(i[0] for i in ipa_parts) + "/"
    
def get_ipa_for_sentence(sentence):
    ipa_parts = get_ipa(sentence)

    return " ".join(i[0] for i in ipa_parts)
