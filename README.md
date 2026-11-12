# Quiz Arena

A small trivia game, used as the hands-on project for the **Claude Code for AI-Native SDLC**
course. You'll grow it over three days: new features on Day 1, team standards and guardrails
on Day 2, and automation, scale and security on Day 3.

## Get started (Windows, PowerShell)

1. **Fork** this repository to your own GitHub account, then clone your fork:
   ```powershell
   git clone https://github.com/<your-username>/quiz-arena.git
   cd quiz-arena
   ```
2. Install dependencies (needs Python 3.12+ and [uv](https://docs.astral.sh/uv/)):
   ```powershell
   uv sync
   ```
3. Run the tests and the linter. Both should pass before you start:
   ```powershell
   uv run pytest
   uv run ruff check .
   ```
4. Play the game:
   ```powershell
   uv run uvicorn app.main:app --reload
   ```
   Open http://127.0.0.1:8000 in your browser.

5. Start Claude Code in the repository folder:
   ```powershell
   claude
   ```

## What's inside

| Path | What it is |
|---|---|
| `app/` | FastAPI back end: `game.py` (sessions), `scoring.py` (points), `questions.py` (packs), `storage.py` (SQLite leaderboard), `main.py` (HTTP API) |
| `web/` | Plain HTML/CSS/JavaScript front end, no build step |
| `data/packs/` | Question packs in JSON |
| `tests/` | `unit/`, `api/` and `acceptance/` tests (pytest) |
| `tickets/` | Backlog tickets you'll implement in the labs |

## Rules for the labs
- Work on a branch per lab (`git switch -c lab-2-1`), and commit often.
- Everything here is dummy data. Don't bring real project code or credentials into this repo.
