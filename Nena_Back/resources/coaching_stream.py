"""Streaming coaching feedback endpoint."""
import json

from flask import Response, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource

from models import db, Recording, Feedback, Mode, Topic
from services.coaching import stream_coaching_feedback


class CoachingStream(Resource):
    """Stream LLM coaching feedback in real-time."""

    @jwt_required()
    def get(self, recording_id):
        """Stream coaching feedback for a recording.

        Returns Server-Sent Events (SSE) stream of:
        1. Text chunks from Claude (real-time words)
        2. Final parsed JSON coaching data

        Args:
            recording_id (int): ID of the recording to coach

        Returns:
            Response: SSE stream with chunks + final JSON
        """
        user_id = get_jwt_identity()

        recording = Recording.query.filter_by(id=recording_id, user_id=user_id).first()
        if not recording:
            return make_response({"error": "Recording not found"}, 404)

        transcription = recording.transcription or ""
        if not transcription:
            return make_response({"error": "No transcription available"}, 400)

        # Get related data
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

        # Compute metrics (reuse existing computation)
        import re
        from resources.feedback import FeedbackResource

        fr = FeedbackResource()
        words = re.findall(r"\w+", transcription.lower())
        total_words = len(words)
        duration_seconds = recording.duration_minutes or 1
        duration_minutes = duration_seconds / 60

        metrics_dict = {
            "pace_wpm": round(total_words / duration_minutes, 2) if duration_minutes > 0 else 0,
            "hedge_count": fr._compute_hedges(transcription)[0],
            "filler_words": len(set([w for w in words if w in fr.filler_words_lst])),
            "concreteness_ratio": fr._compute_concreteness_ratio(transcription),
            "time_to_point_seconds": fr._compute_time_to_point(transcription),
            "long_pause_count": 0,
        }

        def event_stream():
            """Generate SSE events."""
            full_text = ""

            for chunk in stream_coaching_feedback(
                transcription=transcription,
                mode={"name": mode_name},
                topic_text=topic_text,
                framework_slug=framework_slug,
                metrics_dict=metrics_dict
            ):
                if isinstance(chunk, str):
                    # Text chunk from streaming
                    full_text += chunk
                    yield f"data: {json.dumps({'type': 'text', 'chunk': chunk})}\n\n"

                elif isinstance(chunk, dict):
                    # Final parsed JSON
                    yield f"data: {json.dumps({'type': 'complete', 'data': chunk})}\n\n"

            yield "data: [DONE]\n\n"

        return Response(event_stream(), mimetype="text/event-stream")


def register(api):
    """Register streaming coaching endpoint."""
    api.add_resource(CoachingStream, '/coaching/stream/<int:recording_id>')
