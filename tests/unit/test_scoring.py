from app.scoring import BASE_POINTS, TIME_LIMIT_S, score_answer, time_bonus


def test_wrong_answer_scores_zero():
    assert score_answer(False, 3, 1.0) == 0


def test_correct_answer_earns_base_plus_bonus():
    assert score_answer(True, 1, 10.0) == BASE_POINTS[1] + time_bonus(10.0, 1)


def test_no_bonus_at_time_limit():
    assert time_bonus(TIME_LIMIT_S, 2) == 0


def test_slow_correct_answer_earns_half_base():
    assert score_answer(True, 2, TIME_LIMIT_S + 5) == BASE_POINTS[2] // 2


def test_harder_questions_earn_more():
    assert score_answer(True, 3, 5.0) > score_answer(True, 1, 5.0)
