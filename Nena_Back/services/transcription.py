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


def measure_audio_level(audio_path):
    """Return mean/max volume in dBFS, or (None, None) if it can't be measured.

    Used to tell "the mic captured nothing" apart from "speech was not recognised" --
    both otherwise surface as an empty transcript.
    """
    try:
        result = subprocess.run(
            ["ffmpeg", "-i", audio_path, "-af", "volumedetect", "-f", "null", "-"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        mean = peak = None
        for line in result.stderr.splitlines():
            if "mean_volume:" in line:
                mean = float(line.split("mean_volume:")[1].strip().split()[0])
            elif "max_volume:" in line:
                peak = float(line.split("max_volume:")[1].strip().split()[0])
        return mean, peak
    except Exception as e:
        print(f"Could not measure audio level: {e}")
        return None, None


def probe_audio(audio_path):
    """Return a dict of stream properties via ffprobe (codec, rate, channels...)."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries",
             "stream=codec_name,sample_rate,channels,bit_rate,duration",
             "-of", "default=noprint_wrappers=1", audio_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        info = {}
        for line in result.stdout.splitlines():
            if "=" in line:
                k, v = line.split("=", 1)
                info[k.strip()] = v.strip()
        return info
    except Exception as e:
        print(f"[TRANSCRIBE] ffprobe failed: {e}")
        return {}


def transcribe_audio(audio_path):
    bar = "=" * 68
    print("\n" + bar)
    print("[TRANSCRIBE] START")
    print(bar)

    # --- 1. The file we are about to send -------------------------------------
    try:
        size = os.path.getsize(audio_path)
    except OSError:
        size = -1
    print(f"[TRANSCRIBE] file      : {audio_path}")
    print(f"[TRANSCRIBE] size      : {size} bytes ({size/1024:.1f} KB)")

    info = probe_audio(audio_path)
    print(f"[TRANSCRIBE] codec     : {info.get('codec_name')}")
    print(f"[TRANSCRIBE] sample_rt : {info.get('sample_rate')} Hz")
    print(f"[TRANSCRIBE] channels  : {info.get('channels')}")
    print(f"[TRANSCRIBE] duration  : {info.get('duration')} s")

    # --- 2. Is there actually speech-like audio in it? -------------------------
    # (volumedetect only -- silencedetect used to run here too, but it fed
    # nothing except a log line, at the cost of a second full decode pass.)
    mean_db, peak_db = measure_audio_level(audio_path)
    print(f"[TRANSCRIBE] mean vol  : {mean_db} dB")
    print(f"[TRANSCRIBE] peak vol  : {peak_db} dB")

    # Keep a copy so you can listen to exactly what was sent.
    debug_dir = os.getenv("TRANSCRIPTION_DEBUG_DIR")
    if debug_dir:
        try:
            import shutil as _shutil
            os.makedirs(debug_dir, exist_ok=True)
            dest = os.path.join(debug_dir, os.path.basename(audio_path))
            _shutil.copy(audio_path, dest)
            print(f"[TRANSCRIBE] saved copy: {dest}   <-- play this back yourself")
        except Exception as e:
            print(f"[TRANSCRIBE] could not save debug copy: {e}")

    if mean_db is not None and peak_db is not None and peak_db < -50:
        print("[TRANSCRIBE] ABORT: audio is effectively silent")
        print(bar + "\n")
        raise RuntimeError(
            f"Audio is effectively silent (peak {peak_db}dB) -- the microphone "
            f"captured no sound. Check the mic input and OS input volume."
        )

    # --- 3. What we send to AssemblyAI ----------------------------------------
    language = os.getenv("TRANSCRIPTION_LANGUAGE", "en")
    key = aai.settings.api_key or ""
    print(f"[TRANSCRIBE] --> AssemblyAI  language={language!r} punctuate=False "
          f"disfluencies=True")
    print(f"[TRANSCRIBE] api key   : {'set (…' + key[-4:] + ')' if key else 'MISSING!'}")

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(
        audio_path,
        config=aai.TranscriptionConfig(
            punctuate=False,
            disfluencies=True,
            # Pin the language: auto-detect has mis-identified short English clips
            # as other languages, producing gibberish transcripts.
            language_code=language,
        )
    )

    # --- 4. What AssemblyAI returned ------------------------------------------
    text = transcript.text or ""
    words = getattr(transcript, "words", None) or []
    print(f"[TRANSCRIBE] <-- AssemblyAI")
    print(f"[TRANSCRIBE] job id    : {getattr(transcript, 'id', None)}")
    print(f"[TRANSCRIBE] status    : {transcript.status}")
    print(f"[TRANSCRIBE] error     : {transcript.error}")
    print(f"[TRANSCRIBE] audio secs: {getattr(transcript, 'audio_duration', None)}")
    print(f"[TRANSCRIBE] confidence: {getattr(transcript, 'confidence', None)}")
    print(f"[TRANSCRIBE] word count: {len(words)}")
    print(f"[TRANSCRIBE] text      : {text[:400]!r}" if text
          else "[TRANSCRIBE] text      : (EMPTY -- no speech recognised)")

    if transcript.status == aai.TranscriptStatus.error:
        print("[TRANSCRIBE] RESULT: FAILED")
        print(bar + "\n")
        raise RuntimeError(f"AssemblyAI transcription failed: {transcript.error}")

    if not text.strip():
        print("[TRANSCRIBE] RESULT: EMPTY -- AssemblyAI accepted the audio but found "
              "no speech in it.")
        print("[TRANSCRIBE]         The audio itself is the problem, not the API. "
              "Play the saved copy above.")
    else:
        print(f"[TRANSCRIBE] RESULT: OK -- {len(words)} words")

    print(bar + "\n")
    return text


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
