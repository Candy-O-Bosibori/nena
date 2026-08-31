import re
from datetime import datetime, timezone

from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

from models import db


def validate_password_strength(password):
    """Raw-password strength check, usable before hashing.

    The model's own `validates('password')` runs on whatever value is
    assigned to `.password` -- which is always the bcrypt hash, never the
    raw password, since callers hash before assigning. A hash's character
    mix happens to satisfy the same regexes, so that validator alone never
    actually enforces anything; callers must run this against the raw
    password themselves before hashing it.
    """
    assert len(password) > 8, "Password must be more than 8 characters"
    assert re.search(r"[A-Z]", password), "Password should contain at least one uppercase letter"
    assert re.search(r"[a-z]", password), "Password should contain at least one lowercase letter"
    assert re.search(r"[0-9]", password), "Password should contain at least one digit"
    assert re.search(r"[!@#$%^&*(),.?\":{}|<>]", password), "Password should contain at least one special character"


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=True)
    image = db.Column(db.String, nullable=True)
    google_id = db.Column(db.String, unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # relationships with recording and activity log
    recordings = db.relationship('Recording', back_populates='user', cascade="all, delete-orphan")
    activity_logs = db.relationship('ActivityLog', back_populates='user', cascade="all, delete-orphan")
    words = db.relationship('Word', back_populates='user', cascade="all, delete-orphan")

    # serialization rules
    serialize_rules = ('-recordings', '-activity_logs', '-words', '-password')

    # validation
    # email
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email), "Invalid email format"
        return email

    # password is always assigned as an already-hashed value (see
    # validate_password_strength above for why there's no @validates here)

    def __repr__(self):
        return f"<User {self.id}, {self.name}, {self.email}, {self.password}>"
