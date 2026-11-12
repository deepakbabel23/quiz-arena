"""HTTP API and static web front end for Quiz Arena.

Run locally:  uv run uvicorn app.main:app --reload
Then open:    http://127.0.0.1:8000
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app import storage
from app.game import GameError, get_game, start_game
from app.questions import PackError, all_packs

WEB_DIR = Path(__file__).resolve().parent.parent / "web"


@asynccontextmanager
async def lifespan(_app: FastAPI):
    storage.init_db()
    yield


app = FastAPI(title="Quiz Arena", lifespan=lifespan)


class NewGame(BaseModel):
    player: str = Field(min_length=1, max_length=20)
    pack: str
    seed: int | None = None


class Answer(BaseModel):
    choice: int
    seconds_taken: float = Field(ge=0)


@app.get("/api/packs")
def list_packs() -> list[dict]:
    return [
        {"id": p.id, "title": p.title, "questions": len(p.questions)} for p in all_packs().values()
    ]


@app.post("/api/games", status_code=201)
def create_game(body: NewGame) -> dict:
    try:
        game = start_game(body.player, body.pack, body.seed)
    except PackError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"game_id": game.id, "total_questions": len(game.questions)}


@app.get("/api/games/{game_id}/question")
def current_question(game_id: str) -> dict:
    try:
        game = get_game(game_id)
        if game.finished:
            return {"finished": True, "score": game.score}
        q = game.current_question()
    except GameError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "finished": False,
        "number": game.index + 1,
        "total": len(game.questions),
        "id": q.id,
        "text": q.text,
        "choices": list(q.choices),
        "difficulty": q.difficulty,
        "score": game.score,
    }


@app.post("/api/games/{game_id}/answer")
def answer(game_id: str, body: Answer) -> dict:
    try:
        game = get_game(game_id)
        record = game.submit_answer(body.choice, body.seconds_taken)
    except GameError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if game.finished:
        storage.add_score(game.player, game.pack_id, game.score)
    return {
        "correct": record.correct,
        "points": record.points,
        "score": game.score,
        "finished": game.finished,
    }


@app.get("/api/leaderboard/{pack_id}")
def leaderboard(pack_id: str, limit: int = 10) -> list[dict]:
    return storage.top_scores(pack_id, limit)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(WEB_DIR / "index.html")


app.mount("/static", StaticFiles(directory=WEB_DIR), name="static")
