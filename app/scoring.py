"""Scoring rules for Quiz Arena.

A correct answer earns base points for its difficulty plus a speed bonus.
A wrong answer earns nothing (there is no penalty).
"""

BASE_POINTS = {1: 100, 2: 200, 3: 300}
TIME_LIMIT_S = 20
BONUS_PER_SECOND = 5


def time_bonus(seconds_taken: float, difficulty: int) -> int:
    """Faster answers earn more. The bonus is capped at 50 points."""
    remaining = TIME_LIMIT_S - seconds_taken
    if remaining <= 0:
        return 0
    return int(remaining * BONUS_PER_SECOND * difficulty)


def score_answer(correct: bool, difficulty: int, seconds_taken: float) -> int:
    """Return the points for one answer."""
    if not correct:
        return 0
    if seconds_taken > TIME_LIMIT_S:
        # Too slow: the answer still counts, but only for half the base points.
        return BASE_POINTS[difficulty] // 2
    return BASE_POINTS[difficulty] + time_bonus(seconds_taken, difficulty)
