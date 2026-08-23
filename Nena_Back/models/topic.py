from datetime import datetime, timezone

from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_serializer import SerializerMixin

from models import db


class Topic(db.Model, SerializerMixin):
    __tablename__ = 'topics'

    id = db.Column(db.Integer, primary_key=True)
    mode_id = db.Column(db.Integer, db.ForeignKey('modes.id'), nullable=False)
    text = db.Column(db.String, nullable=False)
    difficulty = db.Column(Enum('easy', 'medium', 'hard', name='topic_difficulty'), nullable=False)
    tags = db.Column(JSON, nullable=False, default=[])
    meta = db.Column(JSON, nullable=True, default={})
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    mode = db.relationship('Mode', backref='topics')

    # `recordings` and `feedback_recommendations` are implicit backrefs; excluded
    # by default so topics never drag the recording graph along behind them.
    serialize_rules = ('-mode', '-recordings', '-feedback_recommendations')
