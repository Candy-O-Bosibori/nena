from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_serializer import SerializerMixin

from models import db


class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    filler_words = db.Column(db.Integer)
    filler_word_list = db.Column(JSON)
    pace_wpm = db.Column(db.Float)
    vocabulary_count = db.Column(db.Text)
    vocabulary_list = db.Column(JSON)
    notes = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Foreign Key
    recording_id = db.Column(db.Integer, db.ForeignKey('recordings.id'), nullable=False, unique=True)

    # Relationship back to Recording
    recording = db.relationship('Recording', back_populates='feedback')

    serialize_rules = ('-recording.feedback',)
