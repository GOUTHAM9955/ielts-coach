---
name: project-overview
description: "What the IELTS Coach project is, why it exists, and how the whole system works"
metadata: 
  node_type: memory
  type: project
  originSessionId: e6f11138-ae3c-4a97-a340-3cd66c796fb5
---

## What this is

A personal IELTS General Training writing practice toolkit built by Goutham.
Goal: improve writing from Band 6 to Band 7+ by drilling real mistakes from actual writing sessions.

## How the system works

1. Goutham does a full writing test inside a Claude chat session
2. After the session, real errors are extracted — misspellings, vocab gaps, grammar mistakes
3. Those errors are added to the drill apps (spelling.json, vocabulary.json)
4. The drill apps are used in spare moments (morning commute, lunch break) to reinforce those exact mistakes

The apps are NOT generic IELTS tools — they are personalised to Goutham's actual errors.

## Data lives in JSON files — no database

- `data/spelling.json` — words Goutham misspells, with attempts/correct/last_seen tracking
- `data/vocabulary.json` — vocab words with definition, example, category, attempts/correct
- `data/sessions.json` — history of every practice session with date, score, duration

## Word bank comes from Google Sheets

Words are imported from a Google Sheets spreadsheet via `import_excel.py` using the `gspread` library.
Credentials are stored in `credentials.json` (gitignored).

**Why:** Goutham wanted a simple way to add new words after a writing session without editing JSON directly.
