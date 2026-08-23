from datetime import datetime, timezone

from sqlalchemy_serializer import SerializerMixin

from models import db


class Recording(db.Model, SerializerMixin):
    __tablename__ = 'recordings'

    id = db.Column(db.Integer, primary_key=True)
    transcription = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    duration_minutes = db.Column(db.Float, nullable=False)
    framework_slug = db.Column(db.String, nullable=True)

    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mode_id = db.Column(db.Integer, db.ForeignKey('modes.id'), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=True)

    user = db.relationship('User', back_populates='recordings')
    mode = db.relationship('Mode', back_populates='recordings')
    topic = db.relationship('Topic', backref='recordings')
    feedback = db.relationship('Feedback', back_populates='recording', cascade="all, delete-orphan", uselist=False)

    serialize_rules = ('-user', '-mode', '-topic', '-feedback')
