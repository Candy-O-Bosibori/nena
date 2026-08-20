import os
import shutil
import tempfile

from flask import request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.utils import secure_filename

from models import db, Recording
from services.transcription import extract_audio, transcribe_audio, get_video_duration

ALLOWED_EXTENSIONS = {'webm', 'mp4', 'mov'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class Recordings(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        recordings = Recording.query.filter_by(user_id=user_id).all()
        response_dict = [rec.to_dict(rules=('-user',)) for rec in recordings]
        return make_response(response_dict, 200)

    @jwt_required()
    def post(self):
        from resources.feedback import FeedbackResource

        user_id = get_jwt_identity()

        if 'video' not in request.files:
            return {"error": "No video file provided"}, 400

        file = request.files['video']
        mode_id = request.form.get('mode_id')
        topic_id = request.form.get('topic_id')
        framework_slug = request.form.get('framework_slug')

        if not file or not allowed_file(file.filename):
            return {"error": "Invalid file format"}, 400

        temp_dir = None
        try:
            temp_dir = tempfile.mkdtemp()

            filename = secure_filename(file.filename)
            filepath = os.path.join(temp_dir, filename)
            file.save(filepath)

            audio_path = extract_audio(filepath, output_dir=temp_dir)
            transcription = None
            try:
                transcription = transcribe_audio(audio_path)
            except Exception as e:
                print(f"Transcription failed: {e}")
                transcription = None

            duration_seconds = get_video_duration(filepath)

            new_recording = Recording(
                transcription=transcription,
                duration_minutes=duration_seconds,
                user_id=user_id,
                mode_id=mode_id,
                topic_id=topic_id if topic_id else None,
                framework_slug=framework_slug if framework_slug else None
            )
            try:
                db.session.add(new_recording)
                db.session.commit()
                feedback_resource = FeedbackResource()
                feedback_resource.post(new_recording.id)
            except Exception as e:
                db.session.rollback()
                print(f"DB error: {e}")
                return {"error": "Database insert failed"}, 500

            return {"message": "Recording uploaded successfully", "recording_id": new_recording.id}, 201

        finally:
            if temp_dir and os.path.exists(temp_dir):
                shutil.rmtree(temp_dir, ignore_errors=True)


class RecordingById(Resource):
    @jwt_required()
    def get(self, recording_id):
        user_id = get_jwt_identity()
        recording = Recording.query.filter_by(id=recording_id, user_id=user_id).first()
        if not recording:
            return {"error": "Recording not found"}, 404
        return make_response(recording.to_dict(), 200)

    @jwt_required()
    def delete(self, recording_id):
        user_id = get_jwt_identity()
        recording = Recording.query.filter_by(id=recording_id, user_id=user_id).first()
        if not recording:
            return {"error": "Recording not found"}, 404

        db.session.delete(recording)
        db.session.commit()
        return {"message": "Recording deleted successfully"}, 200


def register(api, app):
    api.add_resource(Recordings, '/recordings')
    api.add_resource(RecordingById, '/recordingById/<int:recording_id>')
