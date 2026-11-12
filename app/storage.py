"""SQLite-backed leaderboard."""

import os
import sqlite3
from contextlib import closing
from pathlib import Path

DEFAULT_DB = Path(__file__).resolve().parent.parent / "quiz_arena.db"


def _db_path() -> str:
    return os.environ.get("QUIZ_ARENA_DB", str(DEFAULT_DB))


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with closing(_connect()) as conn, conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS scores (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   player TEXT NOT NULL,
                   pack TEXT NOT NULL,
                   score INTEGER NOT NULL,
                   created_at TEXT DEFAULT CURRENT_TIMESTAMP
               )"""
        )


def add_score(player: str, pack: str, score: int) -> None:
    with closing(_connect()) as conn, conn:
        conn.execute(
            "INSERT INTO scores (player, pack, score) VALUES (?, ?, ?)",
            (player, pack, score),
        )


def top_scores(pack: str, limit: int = 10) -> list[dict]:
    with closing(_connect()) as conn:
        rows = conn.execute(
            "SELECT player, score FROM scores WHERE pack = ? ORDER BY score DESC, id ASC LIMIT ?",
            (pack, limit),
        ).fetchall()
    return [dict(row) for row in rows]
