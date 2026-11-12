# AGENTS.md

Instructions for AI coding agents working in this repository.
(Written when the team used a different coding agent.)

## Commands
- Install: `uv sync`
- Run the app: `uv run uvicorn app.main:app --reload` (then open http://127.0.0.1:8000)
- Tests: `uv run pytest`
- Lint: `uv run ruff check .`

## Layout
- `app/` FastAPI back end (game logic, scoring, storage)
- `web/` plain HTML/CSS/JS front end, no build step
- `data/packs/` question packs (JSON, schema v1)
- `tests/` unit, API and acceptance tests

## Conventions
- Python 3.12, type hints on public functions.
- Keep the front end dependency-free.
