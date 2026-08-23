from sqlalchemy_serializer import SerializerMixin

from models import db


class Mode(db.Model, SerializerMixin):
    __tablename__ = 'modes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, nullable=True)
    explainer = db.Column(db.String, nullable=True)
    slug = db.Column(db.String, unique=True, nullable=False)
    default_timer_seconds = db.Column(db.Integer, nullable=True)
    accent_color = db.Column(db.String, nullable=False)
    sort_order = db.Column(db.Integer, nullable=False, default=0)

    # Relationships
    recordings = db.relationship('Recording', back_populates='mode')

    # Relationships are opt-in per endpoint: serializing them by default reopens
    # cycles (mode -> topics -> recordings -> user -> recordings -> ...) that
    # one-level-deep rules cannot close.
    serialize_rules = ('-recordings', '-topics')
