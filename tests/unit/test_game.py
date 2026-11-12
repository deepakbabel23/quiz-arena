import pytest

from app.game import MAX_QUESTIONS, GameError, start_game


def test_game_has_at_most_max_questions():
    game = start_game("ana", "space", seed=1)
    assert len(game.questions) <= MAX_QUESTIONS


def test_same_seed_gives_same_order():
    a = start_game("ana", "space", seed=7)
    b = start_game("ben", "space", seed=7)
    assert [q.id for q in a.questions] == [q.id for q in b.questions]


def test_correct_answer_adds_points():
    game = start_game("ana", "space", seed=1)
    q = game.current_question()
    record = game.submit_answer(q.answer, 3.0)
    assert record.correct
    assert game.score == record.points > 0


def test_cannot_answer_after_game_over():
    game = start_game("ana", "space", seed=1)
    while not game.finished:
        game.submit_answer(0, 5.0)
    with pytest.raises(GameError):
        game.submit_answer(0, 5.0)


def test_choice_out_of_range_is_rejected():
    game = start_game("ana", "space", seed=1)
    with pytest.raises(GameError):
        game.submit_answer(99, 5.0)
