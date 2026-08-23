"""Isolated AssemblyAI test -- no Flask, no DB, no app code."""
import os, sys
from dotenv import load_dotenv
load_dotenv("/home/candy/MyProjects/nena/Nena_Back/.env")
import assemblyai as aai

key = os.getenv("ASSEMBLYAI_API_KEY")
print("1. API key loaded:", bool(key), "(len %s)" % (len(key) if key else 0))
aai.settings.api_key = key

target = sys.argv[1] if len(sys.argv) > 1 else "https://assembly.ai/wildfires.mp3"
print("2. transcribing:", target)

cfg = aai.TranscriptionConfig(punctuate=False, disfluencies=True, language_code="en")
t = aai.Transcriber().transcribe(target, config=cfg)

print("3. status    :", t.status)
print("   error     :", t.error)
print("   audio secs:", getattr(t, "audio_duration", None))
words = getattr(t, "words", None)
print("   words     :", len(words) if words else 0)
print("   text      :", repr(t.text)[:200] if t.text else "(EMPTY)")
print()
print("VERDICT:", "AssemblyAI WORKS" if (t.text or "").strip() else "returned EMPTY text")
