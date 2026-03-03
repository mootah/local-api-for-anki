import asyncio
import sqlite3
from pathlib import Path

# Paths relative to the script
DATA_DIR = Path(__file__).parent.parent / "app" / "data"
TXT_FILE = DATA_DIR / "en_US.txt"
DB_FILE = DATA_DIR / "ipa.db"

def init_db():
    if not TXT_FILE.exists():
        print(f"Error: {TXT_FILE} not found.")
        return

    print(f"Reading from {TXT_FILE}...")

    # We use standard sqlite3 for initialization as it's faster for bulk inserts
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS ipa_dict")
    cursor.execute("""
        CREATE TABLE ipa_dict (
            word TEXT PRIMARY KEY,
            ipa TEXT NOT NULL
        )
    """)

    batch = []
    batch_size = 1000
    count = 0

    with open(TXT_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                word = parts[0].lower()
                pronunciations = parts[1]
                # Remove outer slashes and store
                # Original format: /pron1/, /pron2/
                # We want: pron1, pron2
                ipa = pronunciations.replace("/", "")

                batch.append((word, ipa))
                count += 1

                if len(batch) >= batch_size:
                    cursor.executemany("INSERT OR IGNORE INTO ipa_dict (word, ipa) VALUES (?, ?)", batch)
                    batch = []

    if batch:
        cursor.executemany("INSERT OR IGNORE INTO ipa_dict (word, ipa) VALUES (?, ?)", batch)

    cursor.execute("CREATE INDEX idx_word ON ipa_dict(word)")
    conn.commit()
    conn.close()

    print(f"Successfully imported {count} entries into {DB_FILE}")

if __name__ == "__main__":
    init_db()
