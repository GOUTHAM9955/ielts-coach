# IELTS Coach

A personal IELTS General Training writing practice toolkit — built with Python
to drill real errors from actual writing sessions.

## Why I built this

I scored Band 6 in IELTS writing and want to reach Band 7+. My weak areas are
spelling, grammar, vocabulary range, and sentence structure. Instead of generic
practice apps, this toolkit is fed by real errors from my own writing — making
every practice session directly relevant to what I actually get wrong.

## How it works

1. **Write** — Take a full IELTS writing test in Claude chat (Task 1 letter + Task 2 essay)
2. **Get feedback** — Claude analyses every error by category
3. **Extract errors** — Add real mistakes to the apps (takes ~2 minutes)
4. **Drill** — Practice spelling, vocabulary, grammar in spare moments on any device

## Apps

| App | What it does | API needed |
|-----|-------------|-----------|
| `spelling.py` | Spelling flashcards from your real mistakes | No |
| `vocabulary.py` | Vocabulary cards with definitions and examples | No |
| `coach.py` | Grammar + sentence correction with AI feedback | Yes |

## Tech stack

- Python 3.10+
- Claude API (Anthropic) — for grammar and sentence coach
- Flask — web interface
- Deployed on Render

## Project structure

```
ielts-coach/
├── utils.py            # Shared data layer
├── spelling.py         # Spelling flashcard app
├── vocabulary.py       # Vocabulary flashcard app
├── coach.py            # AI grammar + sentence coach
├── app.py              # Flask web wrapper
└── data/               # JSON word banks and session history
```

## Setup

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ielts-coach.git
cd ielts-coach

# Install dependencies
pip install -r requirements.txt

# Add your API key
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Run spelling app
python spelling.py

# Run vocabulary app
python vocabulary.py

# Run grammar coach
python coach.py
```

## Progress tracker

| Date | Task | Band estimate |
|------|------|--------------|
| — | Baseline | 6.0 |

---

Built as a real Python project — modular, version controlled, and deployed to the web.
