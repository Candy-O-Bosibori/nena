"""Regression tests for the anonymous-browsing pass: exactly 4 endpoints
should be reachable with no Authorization header, everything else must
still 401. If someone re-adds @jwt_required() to one of the 4, or forgets it
on something that should stay protected, this is what catches it."""


def test_modes_is_public(client):
    resp = client.get("/modes")
    assert resp.status_code == 200


def test_topics_is_public(client):
    resp = client.get("/topics")
    assert resp.status_code == 200


def test_topics_random_is_public(client):
    resp = client.get("/topics/random?mode=random-topic")
    # 200 if a matching topic exists in the test DB, 404 if none do (empty
    # DB) -- either way, it must not be 401. The auth gate is what this test
    # protects, not the seed data.
    assert resp.status_code != 401


def test_topics_today_is_public(client):
    resp = client.get("/topics/today?mode=daily-reflection")
    assert resp.status_code != 401


def test_recordings_still_requires_auth(client):
    resp = client.get("/recordings")
    assert resp.status_code == 401


def test_words_still_requires_auth(client):
    resp = client.get("/words")
    assert resp.status_code == 401
