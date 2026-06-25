# IELTS Coach — CLAUDE.md

## Start of every session — read this first

Before doing anything, read all files in `.claude/memory/`. Start with `.claude/memory/MEMORY.md` for the index, then read each file. This gives you the full project context — what's built, what's next, who Goutham is, and the coding rules.

---

## What this project is

A personal IELTS General Training writing practice toolkit built by Goutham.
Goal: improve writing from Band 6 to Band 7+ by drilling real errors from actual
writing sessions.

This project has two equal goals: **build a working IELTS practice app** and **learn Python properly along the way**.

### How we work together

**1. Learning first, building second**
Before writing any code, check whether Goutham has already learned the Python concept needed.
- If yes → ask him to write it first, then review and give feedback
- If no → teach the concept first: explain it clearly, give a simple example, ask follow-up questions to confirm understanding, then build together

**2. Industry standards from day one**
Even though this is a learning project, all code must follow real-world professional practices:
- Meaningful variable and function names
- One responsibility per function (a function does one thing only)
- Error handling at every point where something could go wrong
- No hardcoded values — use constants or config
- Code must be readable by someone who didn't write it

**3. Evaluate before moving on**
After Goutham writes code, always:
- Point out what was done well
- Explain any mistakes clearly (not just fix them — explain why it was wrong)
- Suggest the industry-standard way if his approach works but has a better alternative

**4. Never just hand over finished code**
Always explain what each piece does and why it was written that way.
The goal is that Goutham could write it himself the next time without help.

---

## How the system works

Goutham uses **Claude chat sessions** as full writing tests and feedback tools.
After each session, real errors (spelling mistakes, vocabulary gaps, grammar rules,
awkward sentences) are extracted and added to the apps.

The apps are the **drill tools** — short practice sessions in spare moments
(morning commute, lunch break) that reinforce exactly the errors from real writing.

---

## Project modules — build in this order

| File | Module | Status | Needs API? |
|------|--------|--------|-----------|
| `utils.py` | M1 — Data layer | ✅ Done | No |
| `spelling.py` | M2 — Spelling flashcards | ✅ Done | No |
| `import_excel.py` | M2 — Google Sheets importer | ✅ Done | No (gspread) |
| `progress.py` | M2 — Terminal progress charts | ✅ Done | No (matplotlib) |
| `vocabulary.py` | M2 — Vocabulary flashcards | 🔲 Not started | No |
| `coach.py` | M3 — Grammar + sentence correction | 🔲 Not started | Yes — Claude API |
| `app.py` | M4 — Flask web wrapper | ✅ Done (spelling + web UI) | No (M3 not wired yet) |

**Update the status column above after finishing each module.**

---

## Data layer (M1)

All data lives in `data/` as JSON files. No database.

| File | What it stores |
|------|---------------|
| `data/spelling.json` | List of words Goutham misspells |
| `data/vocabulary.json` | Vocabulary words with definitions and examples |
| `data/sessions.json` | History of every practice session with timestamps |

### spelling.json format
```json
[
  {
    "word": "necessary",
    "attempts": 5,
    "correct": 3,
    "last_seen": "2025-01-15"
  }
]
```

### vocabulary.json format
```json
[
  {
    "word": "elaborate",
    "definition": "to develop or explain in more detail",
    "example": "Could you elaborate on your reasons for leaving?",
    "category": "formal",
    "attempts": 3,
    "correct": 2,
    "last_seen": "2025-01-15"
  }
]
```

### sessions.json format
```json
[
  {
    "date": "2025-01-15",
    "app": "spelling",
    "words_practiced": 10,
    "correct": 7,
    "incorrect": 3,
    "duration_minutes": 8
  }
]
```

---

## Coding rules — always follow these

1. Add a comment above every function explaining what it does in plain English
2. Use plain `for` loops — never list comprehensions
3. Print clear messages so the user always knows what is happening
4. Handle missing files with a helpful message — never let the app crash
5. API key must come from the `.env` file via `python-dotenv` — never hardcode it
6. Keep functions short — max 20 lines each, split if longer
7. Use `colorama` for coloured terminal output to make apps feel polished
8. Every app must have an `add` mode so new words can be added in under 2 minutes

---

## Tech stack

```
Python 3.10+
anthropic          — Claude API (M3 only)
python-dotenv      — loading .env file safely
colorama           — coloured terminal output
Flask              — web wrapper (M4 only)
```

Install all dependencies:
```bash
pip install anthropic python-dotenv colorama flask
```

---

## Environment variables

Create a `.env` file in the project root (already in `.gitignore`):
```
ANTHROPIC_API_KEY=your_key_here
```

Never put the actual key in any Python file or commit it to GitHub.

---

## M3 coach.py — how it should behave

The coach has two modes:

**Mode 1 — Sentence correction**
User pastes a sentence from their writing. Claude evaluates it and returns:
- What is wrong and why
- A corrected version
- Which IELTS criterion is affected (Task Achievement / Coherence / Lexical / Grammar)

**Mode 2 — Grammar drill**
User is shown one of their previously corrected sentences and must fix it themselves
first, then sees the correct answer. More active than Mode 1.

The Claude API system prompt for coach.py must enforce short, structured responses.
Do not let Claude write essay-length feedback. Output must be:
- Max 5 lines
- Always include: ISSUE / CORRECTED / CRITERION
- Structured so it can be parsed and saved to sessions.json

---

## File structure

```
ielts-coach/
├── CLAUDE.md           ← This file — read first every session
├── README.md           ← Project overview for GitHub
├── requirements.txt    ← Python packages
├── .env                ← API key (gitignored — never commit)
├── .gitignore          ← Ignore .env, __pycache__, venv
├── utils.py            ← M1: shared data read/write functions
├── spelling.py         ← M2: spelling flashcard app (terminal)
├── import_excel.py     ← M2: imports words from Google Sheets
├── progress.py         ← M2: terminal progress charts (matplotlib)
├── vocabulary.py       ← M2: vocabulary flashcard app (NOT BUILT YET)
├── coach.py            ← M3: Claude-powered grammar + sentence coach (NOT BUILT YET)
├── app.py              ← M4: Flask web app (spelling quiz live)
├── audio/              ← Generated MP3 files for audio quiz mode
├── data/
│   ├── spelling.json   ← Spelling word bank
│   ├── vocabulary.json ← Vocabulary word bank
│   └── sessions.json   ← Practice session history
├── templates/          ← Flask HTML templates
└── static/             ← CSS and other static assets
```

---

## Current session context

- **Owner:** Goutham
- **IELTS target:** Band 7+ in writing (currently Band 6)
- **Known weak areas:** spelling, grammar, vocabulary range, sentence structure
- **Build phase:** M2 spelling + M4 Flask web UI done — next is vocabulary.py
- **Next task:** Build vocabulary.py — vocabulary flashcard app (same structure as spelling.py)

---

## How to start a Claude Code session

```bash
cd ielts-coach
claude
```

Then tell Claude Code what to build next. Example:
> "Build utils.py — the data layer. Follow the rules in CLAUDE.md."
