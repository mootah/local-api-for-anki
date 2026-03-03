import sqlite3
from pathlib import Path
from datetime import datetime
import os

# Paths relative to the script
DATA_DIR = Path(__file__).parent.parent / "app" / "data"
EXPORT_DIR = DATA_DIR / "exported"
DB_FILE = DATA_DIR / "ipa.db"

def export_db():
    if not DB_FILE.exists():
        print(f"Error: {DB_FILE} not found. Please run 'uv run task init-db' first.")
        return

    # Ensure export directory exists
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_file = EXPORT_DIR / f"en_US_{timestamp}.txt"

    print(f"Exporting from {DB_FILE} to {export_file}...")

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT word, ipa FROM ipa_dict ORDER BY word ASC")

        count = 0
        with open(export_file, 'w', encoding='utf-8') as f:
            for word, ipa in cursor:
                # Add slashes back to IPA parts
                # ipa is stored as "pron1, pron2"
                # we want output as "word\t/pron1/, /pron2/"
                ipa_parts = [p.strip() for p in ipa.split(",")]
                ipa_with_slashes = ", ".join([f"/{p}/" for p in ipa_parts])
                f.write(f"{word}\t{ipa_with_slashes}\n")
                count += 1

        print(f"Successfully exported {count} entries.")
    except Exception as e:
        print(f"An error occurred during export: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    export_db()
