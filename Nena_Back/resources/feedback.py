import re

from flask import make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from models import db, Recording, Feedback, Word


class FeedbackResource(Resource):
    filler_words_lst = [
        "um", "uh", "like", "actually", "basically", "literally", "kinda", "right", "hmm", "mhm", "uh-huh", "huh"
    ]

    @jwt_required()
    def post(self, recording_id):
        user_id = get_jwt_identity()

        recording = Recording.query.filter_by(id=recording_id, user_id=user_id).first()
        if not recording:
            return make_response({"error": "Recording not found"}, 404)

        transcription = recording.transcription
        duration = recording.duration_minutes / 60 or 1  # avoid division by zero

        words = re.findall(r"\w+", transcription.lower())
        total_words = len(words)

        pace_wpm = round(total_words / duration, 2)

        filler_words_used = [w for w in words if w in self.filler_words_lst]
        filler_count = len(set(filler_words_used))

        db_words = Word.query.with_entities(Word.word).all()
        db_vocab = set(w[0].lower() for w in db_words)

        used_advanced_words = [w for w in words if w.lower() in db_vocab]
        vocab_count = len(set(used_advanced_words))

        notes = "Great work! Try to reduce filler words and use more diverse vocabulary."

        feedback = Feedback(
            filler_words=filler_count,
            filler_word_list=filler_words_used,
            pace_wpm=pace_wpm,
            vocabulary_count=vocab_count,
            vocabulary_list=list(set(used_advanced_words)),
            notes=notes,
            recording_id=recording.id,
        )
        db.session.add(feedback)
        db.session.commit()

        return make_response(feedback.to_dict(rules=('-recording',)), 201)

    @jwt_required()
    def get(self, recording_id):
        user_id = get_jwt_identity()
        feedback = (
            Feedback.query.join(Recording)
            .filter(Feedback.recording_id == recording_id, Recording.user_id == user_id)
            .first()
        )
        if not feedback:
            return make_response({"error": "Feedback not found"}, 404)

        return make_response(feedback.to_dict(rules=('-recording',)), 200)


def register(api):
    api.add_resource(FeedbackResource, '/feedback')
