"""Sanity check for the fixture setup itself -- not app behavior. If this
fails, the problem is in conftest.py's DB/session wiring, not in the app."""


def test_client_exists(client):
    assert client is not None


def test_make_user_creates_a_row(make_user, session):
    user = make_user(email="fixture-smoke@example.com")
    assert user.id is not None
    assert user.email == "fixture-smoke@example.com"


def test_auth_headers_has_bearer_token(auth_headers):
    headers, user = auth_headers(email="fixture-smoke-2@example.com")
    assert headers["Authorization"].startswith("Bearer ")
    assert user.id is not None


def test_session_rolls_back_between_tests(session):
    """If the previous test's user leaked through, this would find 2 rows
    instead of 0 for this fresh email."""
    from models import User

    assert User.query.filter_by(email="fixture-smoke@example.com").count() == 0
