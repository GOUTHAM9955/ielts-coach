---
name: technical-decisions
description: Key technical decisions made during the build and why they were chosen
metadata: 
  node_type: memory
  type: project
  originSessionId: e6f11138-ae3c-4a97-a340-3cd66c796fb5
---

## Weighted word selection (spelling.py + app.py)

Words with more errors appear more often in the quiz.
Formula: words with 0 attempts get weight 10. Others get `max(4, 10 - (correct/attempts * 10))`.
**Why:** Goutham should spend more time on his hardest words, not waste time on ones he already knows.

## Audio mode uses gTTS + afplay

Audio files are generated with Google Text-to-Speech (gTTS) and saved as MP3 in `audio/`.
Terminal playback uses `afplay` (macOS only).
Web playback uses an HTML `<audio>` tag served by Flask.
**Why:** No paid API needed, files are cached so they don't regenerate each time.

## Audio filenames

`word.replace("/", "_").replace(" ", "_") + ".mp3"`
**Why:** Words can contain spaces and slashes (e.g. "brother's wedding") which are invalid in filenames.

## Google Sheets as word bank

Words are stored in a Google Sheet and imported via `import_excel.py`.
`credentials.json` holds the service account key (gitignored).
**Why:** Easy for Goutham to add words after a writing session without touching code or JSON.

## Flask session for quiz state

Current quiz score (total, correct) and current word are stored in Flask's session cookie.
**Why:** Simple stateless approach — no database needed for a single-user personal app.

## No database — JSON files only

All data is plain JSON in the `data/` directory.
**Why:** Beginner-friendly, no setup required, easy to inspect and edit directly.

See also: [[coding-standards]], [[project-overview]]
