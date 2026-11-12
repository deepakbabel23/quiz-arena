def test_list_packs(client):
    packs = client.get("/api/packs").json()
    assert {p["id"] for p in packs} >= {"space", "web-fundamentals"}


def test_unknown_pack_returns_404(client):
    res = client.post("/api/games", json={"player": "ana", "pack": "nope"})
    assert res.status_code == 404


def test_player_name_too_long_is_rejected(client):
    res = client.post("/api/games", json={"player": "x" * 21, "pack": "space"})
    assert res.status_code == 422


def test_full_game_lands_on_leaderboard(client):
    game = client.post("/api/games", json={"player": "ana", "pack": "space", "seed": 3}).json()
    gid = game["game_id"]
    for _ in range(game["total_questions"]):
        client.get(f"/api/games/{gid}/question")
        client.post(f"/api/games/{gid}/answer", json={"choice": 0, "seconds_taken": 4})
    assert client.get(f"/api/games/{gid}/question").json()["finished"] is True
    board = client.get("/api/leaderboard/space").json()
    assert board[0]["player"] == "ana"
