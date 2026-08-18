from datetime import datetime, timezone

from sqlalchemy_serializer import SerializerMixin

from models import db


class Recording(db.Model, SerializerMixin):
    __tablename__ = 'recordings'

    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String, nullable=True)
    transcription = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    duration_minutes = db.Column(db.Integer, nullable=False)

    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mode_id = db.Column(db.Integer, db.ForeignKey('modes.id'), nullable=False)

    user = db.relationship('User', back_populates='recordings')
    mode = db.relationship('Mode', back_populates='recordings')
    feedback = db.relationship('Feedback', back_populates='recording', cascade="all, delete-orphan", uselist=False)

    serialize_rules = ('-user.recordings', '-mode.recordings', '-feedback.recording')
