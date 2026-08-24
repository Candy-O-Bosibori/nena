"""Shared pytest fixtures for the backend test suite.

app.py has no application factory -- it builds `app` and binds every
extension (db, bcrypt, jwt) at module-import time, reading DATABASE_URL from
the environment as it does. So the only way to point tests at a scratch
database is to set DATABASE_URL *before* `app` is imported anywhere -- this
module does that first, then imports app once for the whole test session.

Tests run against a dedicated `test` schema inside the same Postgres
database/role the app already uses locally (the nena_user role isn't granted
CREATEDB, but can freely create/drop schemas) -- so no separate database or
extra privileges are required, and the same approach works unchanged in CI
against a Postgres service container.
"""
import os

_TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "postgresql://nena_user:nena_password@localhost:5432/nena?options=-csearch_path=test",
)
os.environ["DATABASE_URL"] = _TEST_DATABASE_URL
# app.py also requires these to be non-empty; local .env normally supplies
# them, but keep tests independent of a .env file being present.
os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("JWT_SECRET_KEY", "test-jwt-secret-key")

import pytest
import sqlalchemy as sa
from flask_bcrypt import generate_password_hash
from flask_jwt_extended import create_access_token

import app as app_module
from models import db as _db, User


@pytest.fixture(scope="session")
def app():
    application = app_module.app
    application.config["TESTING"] = True
    return application


@pytest.fixture(scope="session")
def db(app):
    with app.app_context():
        _db.session.execute(sa.text("CREATE SCHEMA IF NOT EXISTS test"))
        _db.session.commit()
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.session.execute(sa.text("DROP SCHEMA test CASCADE"))
        _db.session.commit()


@pytest.fixture
def session(app, db):
    """Give each test a clean slate.

    Flask-SQLAlchemy 3.x's scoped session doesn't reliably bind to a single
    externally-managed connection/transaction (configure(bind=...) is
    silently overridden by its own engine resolution), so a
    begin-savepoint-then-rollback pattern doesn't actually isolate tests --
    verified directly: rows survived a rollback of the "outer" transaction.
    Truncating every app table after each test sidesteps that entirely and
    is simple enough not to be worth fighting the ORM over for a smoke-test
    suite this size.
    """
    with app.app_context():
        yield db.session
        db.session.rollback()
        for table in reversed(db.metadata.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def make_user(session):
    """Create a User row the same way SignUp does (bcrypt hash, model
    validation included), returning the model instance."""

    def _make_user(email="test@example.com", password="Testpass1!", name="Test User"):
        hashed = generate_password_hash(password).decode("utf-8")
        user = User(name=name, email=email, password=hashed)
        session.add(user)
        session.commit()
        return user

    return _make_user


@pytest.fixture
def auth_headers(make_user):
    """A ready-to-use Authorization header for a freshly created user,
    mirroring exactly what /signin hands back (create_access_token with the
    stringified user id as identity)."""

    def _auth_headers(**user_kwargs):
        user = make_user(**user_kwargs)
        token = create_access_token(identity=str(user.id))
        return {"Authorization": f"Bearer {token}"}, user

    return _auth_headers
