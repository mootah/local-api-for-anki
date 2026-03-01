from app.services.text import sanitize_text

def test_sanitize_text_html():
    html = "<div>Hello <b>world</b>!</div>"
    assert sanitize_text(html) == "Hello world!"

def test_sanitize_text_cloze():
    cloze = "{{c1::cloze deletion}}"
    assert sanitize_text(cloze) == "cloze deletion"

def test_sanitize_text_mixed():
    mixed = "<div>{{c1::Text}} with <p>HTML</p></div>"
    assert sanitize_text(mixed) == "Text with HTML"
