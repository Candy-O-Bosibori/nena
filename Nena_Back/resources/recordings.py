import os
import subprocess

from flask import request, make_response, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.utils import secure_filename

from models import db, Recording
from services.transcription import extract_audio, transcribe_audio, get_video_duration

UPLOAD_FOLDER = 'static/uploads'  # Folder to store videos
ALLOWED_EXTENSIONS = {'webm', 'mp4', 'mov'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


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

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            audio_path = extract_audio(filepath)
            transcription = None
            try:
                transcription = transcribe_audio(audio_path)
            except Exception as e:
                print(f"Transcription failed: {e}")
                transcription = None

            mp4_path = os.path.splitext(filepath)[0] + ".mp4"
            subprocess.run([
                "ffmpeg", "-i", filepath,
                "-c:v", "libx264", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", "-y", mp4_path
            ], check=True)
            video_url = f"/{UPLOAD_FOLDER}/{os.path.basename(mp4_path)}"

            new_recording = Recording(
                video_url=video_url,
                transcription=transcription,
                duration_minutes=get_video_duration(mp4_path),
                user_id=user_id,
                mode_id=mode_id
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

            return {"message": "Recording uploaded successfully", "video_url": video_url}, 201

        return {"error": "Invalid file format"}, 400


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

        if recording.video_url:
            filepath = recording.video_url.lstrip('/')
            if os.path.exists(filepath):
                os.remove(filepath)

        db.session.delete(recording)
        db.session.commit()
        return {"message": "Recording deleted successfully"}, 200


def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


def register(api, app):
    api.add_resource(Recordings, '/recordings')
    api.add_resource(RecordingById, '/recordingById/<int:recording_id>')
    app.add_url_rule('/uploads/<path:filename>', 'uploaded_file', uploaded_file)
