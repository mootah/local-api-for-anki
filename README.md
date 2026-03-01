
# Local API for English Sentence Mining

This project provides a similar API to [yomitan-api](https://github.com/yomidevs/yomitan-api) for the annotation functionality of [asbplayer](https://github.com/killergerbah/asbplayer), and a backfill API for [FastWordQuery](https://github.com/sirius-fan/FastWordQuery).

The API backend is based on

- [spaCy](https://github.com/explosion/spaCy)
- [ipa-dict](https://github.com/open-dict-data/ipa-dict)
- [wordfreq](https://github.com/rspeer/wordfreq)
- [cefrpy](https://github.com/Maximax67/cefrpy)

## Installation

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/).
2. Clone this repository:
   ```bash
   git clone https://github.com/mootah/local-api-for-anki.git
   cd local-api-for-anki
   ```
3. Initialize the project:
   ```bash
   uv sync
   ```
4. Start the server:
   ```bash
   uv run task server
   ```

   You can see the api reference from http://127.0.0.1:19634/docs

## For asbplayer annotation

1. In asbplayer, set the `Yomitan API URL` to `http://127.0.0.1:19634`.

## For FastWQ

1. Open your FastWQ addon directory.
2. Copy `addon/localapi.py` into `service/dict/`.
3. Restart Anki.

## API

### Yomitan

- `/serverVersion`
- `/yomitanVersion`
- `/tokenize`
- `/termEntries`

### Fast Word Query

- `/fastwq/{word}`
