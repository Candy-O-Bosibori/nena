import os
import subprocess

import assemblyai as aai

aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")


def extract_audio(video_path, output_dir=None):
    if output_dir is None:
        output_dir = "static/audio"
    os.makedirs(output_dir, exist_ok=True)
    audio_path = os.path.join(output_dir, os.path.splitext(os.path.basename(video_path))[0] + ".mp3")

    command = [
        "ffmpeg", "-i", video_path, "-vn", "-acodec", "libmp3lame", "-ar", "44100", "-ac", "2", "-y", audio_path
    ]
    subprocess.run(command, check=True)

    return audio_path


def transcribe_audio(audio_path):
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
        audio_path,
        config=aai.TranscriptionConfig(
            punctuate=False,
            disfluencies=True
        )
    )
    return transcript.text


def get_video_duration(filepath):
    """Returns duration in seconds."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "format=duration", "-of",
             "default=noprint_wrappers=1:nokey=1", filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0 or not result.stdout.strip():
            raise ValueError("ffprobe failed")
        duration_seconds = float(result.stdout.strip())
        return duration_seconds
    except Exception as e:
        print(f"Error getting video duration: {e}")
        return 0  # fallback so DB insert doesn't fail
