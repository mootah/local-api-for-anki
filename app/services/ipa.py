import re
import aiosqlite
from pathlib import Path
from typing import List, Optional
from app.services.text import sanitize_text

DB_PATH = Path(__file__).parent.parent / "data" / "ipa.db"

class IPADatabase:
    _instance = None
    _db = None

    @classmethod
    async def get_db(cls):
        if cls._db is None:
            cls._db = await aiosqlite.connect(DB_PATH)
            await cls._db.create_function("regexp", 2, lambda x, y: 1 if re.search(x, y) else 0)
            cls._db.row_factory = aiosqlite.Row
        return cls._db

    @classmethod
    async def close(cls):
        if cls._db is not None:
            await cls._db.close()
            cls._db = None

async def get_word_pronunciations(word: str) -> List[str]:
    """
    Returns a list of IPA pronunciations for a given word,
    with slashes removed. Returns an empty list if not found.
    """
    if not word or not any(c.isalnum() for c in word):
        return []

    lower_word = word.lower()
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

    db = await IPADatabase.get_db()
    for candidate in candidates:
        async with db.execute("SELECT ipa FROM ipa_dict WHERE word = ?", (candidate,)) as cursor:
            row = await cursor.fetchone()
            if row:
                ipa_str = row["ipa"]
                return [p.strip() for p in ipa_str.split(",")]

    return []

async def get_ipa(text: str) -> List[List[str]]:
    text = sanitize_text(text)
    words = re.findall(r"\b[\w'.,]+", text)
    ipa_parts = []
    for word in words:
        ipa = await get_word_pronunciations(word)
        # Fallback
        if not ipa:
            ipa = [word]
        ipa_parts.append(ipa)
    return ipa_parts

async def get_ipa_for_term(term: str) -> str:
    ipa_parts = await get_ipa(term)
    if not ipa_parts:
        return ""

    if len(ipa_parts) == 1:
        return " ".join(f"/{i}/" for i in ipa_parts[0])
    else:
        # For multiple words, take the first pronunciation of each word
        return "/" + " ".join(i[0] for i in ipa_parts) + "/"

async def get_ipa_for_sentence(sentence: str) -> str:
    ipa_parts = await get_ipa(sentence)
    if not ipa_parts:
        return ""

    return " ".join(i[0] for i in ipa_parts)

# CRUD Operations

async def create_ipa(word: str, ipa: str):
    db = await IPADatabase.get_db()
    try:
        await db.execute("INSERT INTO ipa_dict (word, ipa) VALUES (?, ?)", (word.lower(), ipa))
        await db.commit()
        return True
    except aiosqlite.IntegrityError:
        return False

async def update_ipa(word: str, ipa: str):
    db = await IPADatabase.get_db()
    async with db.execute("UPDATE ipa_dict SET ipa = ? WHERE word = ?", (ipa, word.lower())) as cursor:
        await db.commit()
        return cursor.rowcount > 0

async def delete_ipa(word: str):
    db = await IPADatabase.get_db()
    async with db.execute("DELETE FROM ipa_dict WHERE word = ?", (word.lower(),)) as cursor:
        await db.commit()
        return cursor.rowcount > 0

async def search_ipa(query: str, limit: int = 10, offset: int = 0):
    db = await IPADatabase.get_db()
    # Use REGEXP for regex search
    sql = "SELECT word, ipa FROM ipa_dict WHERE word REGEXP ? LIMIT ? OFFSET ?"
    async with db.execute(sql, (query, limit, offset)) as cursor:
        rows = await cursor.fetchall()

    count_sql = "SELECT COUNT(*) FROM ipa_dict WHERE word REGEXP ?"
    async with db.execute(count_sql, (query,)) as cursor:
        total_row = await cursor.fetchone()
        total = total_row[0]

    return [dict(row) for row in rows], total


async def get_ipa_record(word: str) -> Optional[dict]:
    db = await IPADatabase.get_db()
    async with db.execute("SELECT word, ipa FROM ipa_dict WHERE word = ?", (word.lower(),)) as cursor:
        row = await cursor.fetchone()
        if row:
            return dict(row)
    return None
