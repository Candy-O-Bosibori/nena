from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_serializer import SerializerMixin

from models import db


class Feedback(db.Model, SerializerMixin):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)

    # Existing metrics
    filler_words = db.Column(db.Integer)
    filler_word_list = db.Column(JSON)
    pace_wpm = db.Column(db.Float)
    vocabulary_count = db.Column(db.Text)
    vocabulary_list = db.Column(JSON)
    notes = db.Column(db.String, nullable=True)

    # New deterministic metrics (Step 5)
    hedge_count = db.Column(db.Integer, nullable=True)
    hedge_list = db.Column(JSON, nullable=True)
    time_to_point_seconds = db.Column(db.Float, nullable=True)
    concreteness_ratio = db.Column(db.Float, nullable=True)
    long_pause_count = db.Column(db.Integer, nullable=True)

    # LLM coaching columns (Step 6)
    coach_notes = db.Column(JSON, nullable=True)
    focus_area = db.Column(db.String, nullable=True)
    focus_reason = db.Column(db.String, nullable=True)
    framework_adherence = db.Column(JSON, nullable=True)
    landing_strength = db.Column(db.String, nullable=True)
    strongest_moment = db.Column(db.String, nullable=True)
    next_topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Foreign Keys
    recording_id = db.Column(db.Integer, db.ForeignKey('recordings.id'), nullable=False, unique=True)

    # Relationships
    recording = db.relationship('Recording', back_populates='feedback')
    next_topic = db.relationship('Topic', foreign_keys=[next_topic_id], backref='feedback_recommendations')

    serialize_rules = ('-recording', '-next_topic')
