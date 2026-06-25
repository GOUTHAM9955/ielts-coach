---
name: project-status
description: "Current build status of every module — what's done, what's next, and why"
metadata: 
  node_type: memory
  type: project
  originSessionId: e6f11138-ae3c-4a97-a340-3cd66c796fb5
---

## Modules — last updated 2026-06-25

| File | What it does | Status |
|------|-------------|--------|
| `utils.py` | Shared load/save functions for all JSON data files | ✅ Done |
| `spelling.py` | Terminal spelling quiz — audio mode + written mode, weighted word selection, score tracking | ✅ Done |
| `import_excel.py` | Imports words from Google Sheets into spelling.json | ✅ Done |
| `progress.py` | Terminal progress charts using matplotlib (word accuracy bar chart + score over time line chart) | ✅ Done |
| `app.py` + templates | Flask web app — browser-based spelling quiz with audio and written modes | ✅ Done |
| `vocabulary.py` | Terminal vocabulary flashcard app | 🔲 Not started — next to build |
| `coach.py` | Claude API powered grammar + sentence correction coach | 🔲 Not started — needs Anthropic API |

## What to build next

**vocabulary.py** — same structure as spelling.py but for vocabulary words.
- Show word → user guesses definition or uses it in a sentence
- Two modes: definition mode and example sentence mode
- Weighted selection (same logic as spelling.py)
- Save attempts/correct back to vocabulary.json

## Known bugs in current code (not yet fixed)

1. `app.py` check() route — retrieves `mode` from session but never passes it to `result.html`
   → "Next Word" link in result.html renders as `?mode=` (blank), so mode is lost between questions
2. `app.py` — `send_file` is imported but never used
3. Home page links to `/progress` but that route doesn't exist in app.py — would 404

## Web UI state

The Flask templates (home.html, spelling.html, quiz.html, result.html, end.html) are plain unstyled HTML.
A UI enhancement was planned but paused — user wants to learn while building, so we go step by step.
