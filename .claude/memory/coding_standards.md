---
name: coding-standards
description: "The coding rules for this project — beginner-friendly Python, always follow these"
metadata: 
  node_type: memory
  type: project
  originSessionId: e6f11138-ae3c-4a97-a340-3cd66c796fb5
---

These rules come from CLAUDE.md and must be followed in every file:

1. **Comment above every function** — plain English explaining what it does
2. **Plain for loops only** — never list comprehensions (beginner-friendly)
3. **Max 20 lines per function** — split into smaller functions if longer
4. **Never crash on missing files** — always handle errors with a helpful message
5. **API key from .env only** — use `python-dotenv`, never hardcode keys
6. **colorama for terminal output** — use Fore.GREEN / Fore.RED to make it feel polished
7. **Every app needs an add mode** — so new words can be added in under 2 minutes
8. **Print clear messages** — user should always know what is happening

## Tech stack

- Python 3.10+
- `anthropic` — Claude API (coach.py only)
- `python-dotenv` — loading .env safely
- `colorama` — coloured terminal output
- `flask` — web app (app.py only)
- `gtts` — text to speech for audio quiz mode
- `gspread` — Google Sheets API for importing words
- `matplotlib` — progress charts (progress.py only)

## Environment variables (.env file)

```
ANTHROPIC_API_KEY=...
SESSION_ENCRIPTION_SECRET_KEY=...
```

See also: [[project-overview]]
