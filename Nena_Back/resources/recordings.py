import os
import shutil
import tempfile
import threading
import traceback

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
        # Opt back into mode + feedback; the Feedback page renders rec.mode.name
        # and the per-recording feedback metrics. Their own rules stop the nesting.
        response_dict = [rec.to_dict(rules=('mode', 'feedback')) for rec in recordings]
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

            print("\n" + "#" * 68)
            print(f"[UPLOAD] new recording from user {user_id}")
            print(f"[UPLOAD] uploaded file : {filename}")
            print(f"[UPLOAD] bytes received: {os.path.getsize(filepath)}")
            print(f"[UPLOAD] mode_id={mode_id} topic_id={topic_id} "
                  f"framework={framework_slug}")
            print("#" * 68)

            audio_path = extract_audio(filepath, output_dir=temp_dir)

            # Duration (ffprobe metadata read) doesn't depend on transcription
            # or vice versa -- run it on a side thread so it overlaps with the
            # AssemblyAI wait instead of adding to the total.
            duration_result = {}
            duration_thread = threading.Thread(
                target=lambda: duration_result.update(seconds=get_video_duration(filepath))
            )
            duration_thread.start()

            transcription = None
            transcription_error = None
            try:
                transcription = transcribe_audio(audio_path)
                if not (transcription or "").strip():
                    transcription_error = (
                        "No speech was recognised in the recording. Check that the "
                        "correct microphone is selected and that it is not muted."
                    )
            except Exception as e:
                traceback.print_exc()
                print(f"Transcription failed: {e}")
                transcription = None
                transcription_error = str(e)

            duration_thread.join()
            duration_seconds = duration_result.get("seconds", 0)

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
            except Exception as e:
                db.session.rollback()
                print(f"DB error saving recording: {e}")
                return {"error": "Database insert failed"}, 500

            # Feedback runs after the recording is safely committed and in its own
            # try: a failure here must not roll back the saved recording (it can't --
            # the commit already happened) nor be reported as a DB error.
            feedback_ok = False
            print(f"[FEEDBACK] generating for recording {new_recording.id} "
                  f"(transcription: {len(transcription or '')} chars)")
            try:
                fb = FeedbackResource().generate_for_recording(new_recording.id, user_id)
                feedback_ok = True
                if fb is not None:
                    print(f"[FEEDBACK] pace_wpm={fb.pace_wpm} fillers={fb.filler_words} "
                          f"hedges={fb.hedge_count} concreteness={fb.concreteness_ratio}")
                    print(f"[FEEDBACK] coach_notes: "
                          f"{'yes' if fb.coach_notes else 'none (LLM returned nothing)'}")
                print(f"[FEEDBACK] OK")
            except Exception as e:
                traceback.print_exc()
                print(f"[FEEDBACK] FAILED for recording {new_recording.id}: {e}")

            print("\n" + "#" * 68)
            print(f"[UPLOAD] SUMMARY recording_id={new_recording.id}")
            print(f"[UPLOAD]   transcription: "
                  f"{'OK' if (transcription or '').strip() else 'EMPTY'}")
            print(f"[UPLOAD]   feedback     : {'OK' if feedback_ok else 'FAILED'}")
            print("#" * 68 + "\n")

            return {
                "message": "Recording uploaded successfully",
                "recording_id": new_recording.id,
                "id": new_recording.id,
                "transcription_ok": bool((transcription or "").strip()),
                "transcription_error": transcription_error,
                "feedback_ok": feedback_ok,
            }, 201

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
