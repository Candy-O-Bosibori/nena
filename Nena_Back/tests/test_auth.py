"""Smoke tests for signup / signin / refresh."""
from models import User

VALID_PASSWORD = "Testpass1!"


def test_signup_creates_user_and_returns_tokens(client, session):
    resp = client.post(
        "/signup",
        json={"name": "New User", "email": "newuser@example.com", "password": VALID_PASSWORD},
    )
    assert resp.status_code == 200
    body = resp.get_json()
    assert "access_token" in body
    assert "refresh_token" in body
    assert User.query.filter_by(email="newuser@example.com").count() == 1


def test_signup_rejects_duplicate_email(client, make_user):
    make_user(email="dupe@example.com")

    resp = client.post(
        "/signup",
        json={"name": "Someone Else", "email": "dupe@example.com", "password": VALID_PASSWORD},
    )
    assert resp.status_code == 400


def test_signin_with_correct_credentials(client, make_user):
    make_user(email="signin@example.com", password=VALID_PASSWORD)

    resp = client.post(
        "/signin", json={"email": "signin@example.com", "password": VALID_PASSWORD}
    )
    assert resp.status_code == 200
    body = resp.get_json()
    assert "access_token" in body
    assert "refresh_token" in body


def test_signin_with_wrong_password(client, make_user):
    make_user(email="signin2@example.com", password=VALID_PASSWORD)

    resp = client.post(
        "/signin", json={"email": "signin2@example.com", "password": "WrongPass1!"}
    )
    assert resp.status_code == 401


def test_refresh_with_valid_refresh_token(client, make_user):
    make_user(email="refresh@example.com", password=VALID_PASSWORD)
    signin_resp = client.post(
        "/signin", json={"email": "refresh@example.com", "password": VALID_PASSWORD}
    )
    refresh_token = signin_resp.get_json()["refresh_token"]

    resp = client.post(
        "/refresh", headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert resp.status_code == 200
    body = resp.get_json()
    assert "access_token" in body
    assert "accessToken" in body
