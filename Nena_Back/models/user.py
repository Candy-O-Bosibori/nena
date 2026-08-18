import re
from datetime import datetime, timezone

from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

from models import db


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # relationships with recording and activity log
    recordings = db.relationship('Recording', back_populates='user', cascade="all, delete-orphan")
    activity_logs = db.relationship('ActivityLog', back_populates='user', cascade="all, delete-orphan")
    words = db.relationship('Word', back_populates='user', cascade="all, delete-orphan")

    # serialization rules
    serialize_rules = ('-recordings.user', '-activity_logs.user', '-words.user')

    # validation
    # email
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email
        assert re.match(r"[^@]+@[^@]+\.[^@]+", email), "Invalid email format"
        return email

    # password
    @validates('password')
    def validate_password(self, key, password):
        assert len(password) > 8
        assert re.search(r"[A-Z]", password), "Password should contain at least one uppercase letter"
        assert re.search(r"[a-z]", password), "Password should contain at least one lowercase letter"
        assert re.search(r"[0-9]", password), "Password should contain at least one digit"
        assert re.search(r"[!@#$%^&*(),.?\":{}|<>]", password), "Password should contain at least one special character"
        return password

    def __repr__(self):
        return f"<User {self.id}, {self.name}, {self.email}, {self.password}>"
