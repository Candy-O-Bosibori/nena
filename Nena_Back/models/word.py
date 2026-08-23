from sqlalchemy_serializer import SerializerMixin

from models import db


class Word(db.Model, SerializerMixin):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='words')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'word', name='uq_word_user'),
    )

    serialize_rules = ('-user',)
