---
name: concepts-learned
description: Python concepts Goutham has covered — check this before every coding task to know whether to teach or review
metadata:
  type: user
---

## How to use this file

Before any coding task, check this list.
- **Strong** → remind him, let him write it, then review
- **Weak** → remind him what it does, let him try, then fill gaps
- **Not learned** → teach the concept fully before writing any code

## Concept tracker — last updated 2026-06-25

| Concept | Confidence | First used in | Notes |
|---------|------------|---------------|-------|
| Functions (`def`, parameters, return) | Strong | `utils.py` | Comfortable writing and reading them |
| `if / else / elif` | Strong | `spelling.py` | No issues |
| `for` loops | Strong | `spelling.py`, `utils.py` | Plain loops only, no list comprehensions |
| Reading and writing JSON files | Good | `utils.py` | Understands the pattern, may need reminding on edge cases |
| `random.choices` with weights | Weak | `spelling.py` | Used it but doesn't fully understand how weights work |
| Reading `.env` with `python-dotenv` | Weak | `app.py` | Used it, hasn't learned why it's needed or how it works |
| Flask routes (`@app.route`) | Very weak | `app.py` | Knows it exists, doesn't understand how routing works |
| Flask session cookies | Very weak | `app.py` | Used it but doesn't understand what a session is |

## Concepts not yet covered (needed for upcoming modules)

| Concept | Needed for |
|---------|-----------|
| Flask templates (Jinja2) | UI enhancement |
| HTML basics | UI enhancement |
| CSS basics | UI enhancement |
| `import` and modules | All files — review needed |
| Classes and objects (OOP) | coach.py potentially |
| Anthropic API / `anthropic` SDK | coach.py |
| Error handling (`try / except`) | All files — not yet taught properly |
