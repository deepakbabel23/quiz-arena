"""Game sessions: one player working through one pack."""

import random
import uuid
from dataclasses import dataclass, field

from app.questions import Question, get_pack
from app.scoring import score_answer

MAX_QUESTIONS = 5


class GameError(ValueError):
    """Raised for invalid moves, such as answering after the game is over."""


@dataclass
class AnswerRecord:
    question_id: str
    choice: int
    correct: bool
    points: int


@dataclass
class Game:
    id: str
    player: str
    pack_id: str
    questions: list[Question]
    index: int = 0
    score: int = 0
    answers: list[AnswerRecord] = field(default_factory=list)

    @property
    def finished(self) -> bool:
        return self.index >= len(self.questions)

    def current_question(self) -> Question:
        if self.finished:
            raise GameError("game is over")
        return self.questions[self.index]

    def submit_answer(self, choice: int, seconds_taken: float) -> AnswerRecord:
        question = self.current_question()
        if not 0 <= choice < len(question.choices):
            raise GameError("choice out of range")
        correct = choice == question.answer
        points = score_answer(correct, question.difficulty, seconds_taken)
        record = AnswerRecord(question.id, choice, correct, points)
        self.answers.append(record)
        self.score += points
        self.index += 1
        return record


_GAMES: dict[str, Game] = {}


def start_game(player: str, pack_id: str, seed: int | None = None) -> Game:
    pack = get_pack(pack_id)
    rng = random.Random(seed)
    questions = list(pack.questions)
    rng.shuffle(questions)
    game = Game(
        id=uuid.uuid4().hex[:12],
        player=player,
        pack_id=pack_id,
        questions=questions[:MAX_QUESTIONS],
    )
    _GAMES[game.id] = game
    return game


def get_game(game_id: str) -> Game:
    try:
        return _GAMES[game_id]
    except KeyError as exc:
        raise GameError(f"unknown game: {game_id}") from exc
