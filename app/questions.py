"""Load question packs from data/packs/*.json.

Pack format (schema v1):
{
  "pack": "space",                 # unique id, matches the file name
  "title": "Space & Astronomy",
  "questions": [
    {"id": "space-01", "text": "...", "choices": ["a", "b", "c", "d"],
     "answer": 2, "difficulty": 1}
  ]
}
"answer" is the index of the correct choice. "difficulty" is 1 (easy) to 3 (hard).
"""

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

PACKS_DIR = Path(__file__).resolve().parent.parent / "data" / "packs"


@dataclass(frozen=True)
class Question:
    id: str
    text: str
    choices: tuple[str, ...]
    answer: int
    difficulty: int


@dataclass(frozen=True)
class Pack:
    id: str
    title: str
    questions: tuple[Question, ...]


class PackError(ValueError):
    """Raised when a pack file is missing or malformed."""


def _parse_question(raw: dict) -> Question:
    choices = tuple(raw["choices"])
    if len(choices) < 2:
        raise PackError(f"question {raw.get('id')} needs at least two choices")
    if not 0 <= raw["answer"] < len(choices):
        raise PackError(f"question {raw.get('id')} has an answer index out of range")
    if raw["difficulty"] not in (1, 2, 3):
        raise PackError(f"question {raw.get('id')} has an invalid difficulty")
    return Question(
        id=raw["id"],
        text=raw["text"],
        choices=choices,
        answer=raw["answer"],
        difficulty=raw["difficulty"],
    )


def load_pack(path: Path) -> Pack:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        questions = tuple(_parse_question(q) for q in raw["questions"])
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise PackError(f"cannot load pack {path.name}: {exc}") from exc
    return Pack(id=raw["pack"], title=raw["title"], questions=questions)


@lru_cache(maxsize=1)
def all_packs() -> dict[str, Pack]:
    packs = {}
    for path in sorted(PACKS_DIR.glob("*.json")):
        pack = load_pack(path)
        packs[pack.id] = pack
    return packs


def get_pack(pack_id: str) -> Pack:
    try:
        return all_packs()[pack_id]
    except KeyError as exc:
        raise PackError(f"unknown pack: {pack_id}") from exc
