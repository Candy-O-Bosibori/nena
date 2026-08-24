FROM python:3.11-slim

# ffmpeg is a runtime dependency of services/transcription.py (extract_audio,
# get_video_duration shell out to it) -- the slim base image doesn't include it.
RUN apt-get update && apt-get install -y --no-install-recommends ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first and install before copying the rest of the app, so
# Docker's layer cache only re-runs pip install when requirements.txt itself
# changes, not on every code edit.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
