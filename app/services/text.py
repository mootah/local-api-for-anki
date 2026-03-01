import re
from bs4 import BeautifulSoup

def sanitize_text(text: str) -> str:
    # Remove HTML tags
    text = text.replace("<br>", " ")
    soup = BeautifulSoup(text, "html.parser")
    text = soup.get_text()
    # Remove cloze deletions
    text = re.sub(r'\{\{c\d+::([^}]+)\}\}', r'\1', text)
    # Keep only ASCII characters
    # text = re.sub(r'[^\x00-\x7F]+', '', text)
    return text
