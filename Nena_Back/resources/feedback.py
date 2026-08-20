import re

from flask import make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from models import db, Recording, Feedback, Word, Mode, Topic
from services.coaching import get_coaching_feedback


class FeedbackResource(Resource):
    filler_words_lst = [
        "um", "uh", "like", "actually", "basically", "literally", "kinda", "right", "hmm", "mhm", "uh-huh", "huh"
    ]

    hedge_phrases_lst = [
        "kind of", "sort of", "a lot", "quite a bit", "i guess", "i think", "maybe", "perhaps", "somewhat",
        "rather", "quite", "fairly", "pretty", "almost", "basically", "essentially", "arguably", "arguably"
    ]

    vague_words_lst = [
        "stuff", "things", "a lot", "some", "kind of", "sort of", "something", "whatever", "etc"
    ]

    greeting_words_lst = [
        "so", "um", "uh", "okay", "ok", "hi", "hello", "hey", "well", "alright", "right", "yeah", "yes"
    ]

    stopwords_set = {
        "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "from",
        "is", "are", "am", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did",
        "will", "would", "could", "should", "may", "might", "must", "can", "as", "if", "that", "this", "it"
    }

    vague_patterns = [
        r'\bstuff\b', r'\bthings\b', r'\bwhatever\b', r'\betc\b', r'\bsomething\b', r'\bsomehow\b'
    ]

    def _compute_hedges(self, text):
        hedge_phrases_found = []
        text_lower = text.lower()
        for phrase in self.hedge_phrases_lst:
            if phrase in text_lower:
                hedge_phrases_found.extend([phrase] * text_lower.count(phrase))
        return len(set(hedge_phrases_found)), list(set(hedge_phrases_found))

    def _compute_time_to_point(self, transcription):
        if not transcription or not transcription.strip():
            return None

        words = re.findall(r"\w+", transcription.lower())
        if not words:
            return None

        greeting_and_fillers = set(self.greeting_words_lst + self.filler_words_lst)
        first_content_idx = None
        for i, word in enumerate(words):
            if word not in greeting_and_fillers and word not in self.hedge_phrases_lst:
                first_content_idx = i
                break

        if first_content_idx is None:
            return None

        try:
            estimated_wpm = 150
            estimated_seconds = (first_content_idx * 60) / estimated_wpm
            return round(estimated_seconds, 2)
        except:
            return None

    def _compute_concreteness_ratio(self, text):
        if not text or not text.strip():
            return 0.0

        original_words = re.findall(r"\w+", text)
        lowercase_words = [w.lower() for w in original_words]

        if not lowercase_words:
            return 0.0

        content_words_indices = [i for i, w in enumerate(lowercase_words) if w not in self.stopwords_set]
        if not content_words_indices:
            return 0.0

        concrete_score = 0
        for idx in content_words_indices:
            word_lower = lowercase_words[idx]
            word_orig = original_words[idx]

            if re.match(r'^\d+', word_lower):
                concrete_score += 1
            elif any(re.search(pattern, word_lower) for pattern in self.vague_patterns):
                continue
            elif len(word_orig) > 0 and word_orig[0].isupper():
                concrete_score += 1

        ratio = concrete_score / len(content_words_indices) if content_words_indices else 0.0
        return round(min(ratio, 1.0), 2)

    def _compute_long_pauses(self, transcription):
        return 0

    @jwt_required()
    def post(self, recording_id):
        user_id = get_jwt_identity()

        recording = Recording.query.filter_by(id=recording_id, user_id=user_id).first()
        if not recording:
            return make_response({"error": "Recording not found"}, 404)

        transcription = recording.transcription or ""
        duration_seconds = recording.duration_minutes or 1
        duration_minutes = duration_seconds / 60

        words = re.findall(r"\w+", transcription.lower())
        total_words = len(words)

        pace_wpm = round(total_words / duration_minutes, 2) if duration_minutes > 0 else 0

        filler_words_used = [w for w in words if w in self.filler_words_lst]
        filler_count = len(set(filler_words_used))

        hedge_count, hedge_list = self._compute_hedges(transcription)

        time_to_point = self._compute_time_to_point(transcription)

        concreteness_ratio = self._compute_concreteness_ratio(transcription)

        long_pause_count = self._compute_long_pauses(transcription)

        db_words = Word.query.filter_by(user_id=user_id).with_entities(Word.word).all()
        db_vocab = set(w[0].lower() for w in db_words)

        used_advanced_words = [w for w in words if w.lower() in db_vocab]
        vocab_count = len(set(used_advanced_words))

        notes = "Great work! Try to reduce filler words and use more diverse vocabulary."

        metrics_dict = {
            "pace_wpm": pace_wpm,
            "hedge_count": hedge_count,
            "filler_words": filler_count,
            "concreteness_ratio": concreteness_ratio,
            "time_to_point_seconds": time_to_point,
            "long_pause_count": long_pause_count
        }

        topic_text = ""
        if recording.topic_id:
            topic = Topic.query.get(recording.topic_id)
            if topic:
                topic_text = topic.text

        mode_name = "Unknown"
        if recording.mode_id:
            mode = Mode.query.get(recording.mode_id)
            if mode:
                mode_name = mode.name

        framework_slug = recording.framework_slug

        coaching_data = get_coaching_feedback(
            transcription=transcription,
            mode={"name": mode_name},
            topic_text=topic_text,
            framework_slug=framework_slug,
            metrics_dict=metrics_dict
        )

        feedback = Feedback(
            filler_words=filler_count,
            filler_word_list=filler_words_used,
            pace_wpm=pace_wpm,
            vocabulary_count=vocab_count,
            vocabulary_list=list(set(used_advanced_words)),
            hedge_count=hedge_count,
            hedge_list=hedge_list,
            time_to_point_seconds=time_to_point,
            concreteness_ratio=concreteness_ratio,
            long_pause_count=long_pause_count,
            notes=notes,
            recording_id=recording.id,
        )

        if coaching_data:
            feedback.focus_area = coaching_data.get("focus_area")
            feedback.focus_reason = coaching_data.get("focus_reason")
            feedback.landing_strength = coaching_data.get("landing_strength")
            feedback.strongest_moment = coaching_data.get("strongest_moment")
            feedback.coach_notes = coaching_data.get("coach_notes")
            feedback.framework_adherence = coaching_data.get("framework_adherence")

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
    api.add_resource(FeedbackResource, '/feedback/<int:recording_id>')
