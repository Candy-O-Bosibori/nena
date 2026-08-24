# Nena

Nena is a speaking-practice app: pick a prompt (or let it pick one for you),
record yourself answering it, and get structured coaching feedback — pace,
filler words, hedging, concreteness, and how well you followed a chosen
framework (STAR, PREP, etc.).

Anyone can browse modes and topics and try a recording without an account;
an account is only required to save a recording and get feedback on it.

## Repo layout

This is a monorepo with two independently deployable pieces:

```
Nena_Back/    Flask + PostgreSQL API — auth, topics, recordings, transcription, coaching
Nena-Front/   React + Vite client
```

Each has its own README with full setup, environment variables, testing, and
deployment details:

- **[Nena_Back/README.md](Nena_Back/README.md)** — backend setup, API
  reference, Docker, testing
- **[Nena-Front/README.md](Nena-Front/README.md)** — frontend setup, routing
  model, testing

## Quickstart

Both pieces need to be running for the app to work end-to-end.

```bash
# Terminal 1 — backend
cd Nena_Back
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in DATABASE_URL, secrets, API keys
flask db upgrade
python3 seeds/topics.py  # optional: seed topic content (idempotent -- no-ops if topics already exist)
python3 app.py            # http://127.0.0.1:5000

# Terminal 2 — frontend
cd Nena-Front
npm install
cp .env.example .env    # defaults to the backend above; edit if needed
npm run dev              # http://localhost:5173
```

Requires PostgreSQL and ffmpeg installed locally, plus AssemblyAI and
Anthropic API keys — see [Nena_Back/README.md](Nena_Back/README.md#prerequisites)
for details.

## Architecture at a glance

- **Auth**: JWT access (short-lived) + refresh (long-lived) tokens, stored in
  the browser's `localStorage`. No server-side session store — the backend
  is stateless aside from the database.
- **Anonymous browsing**: a handful of read-only endpoints (modes, topics)
  don't require auth, so the app has a real landing/browse experience before
  asking anyone to sign up. Submitting a recording is the one hard wall,
  since it needs a real account to attach the recording to.
- **Recording pipeline**: browser `MediaRecorder` → upload → `ffmpeg` audio
  extraction → AssemblyAI transcription → rule-based metrics (pace, fillers,
  hedges) → Anthropic-generated coaching notes — all synchronous within a
  single request, by design (an earlier async/background version made the
  UX worse, since the user still had to wait and then separately refresh to
  see results).
- **Deployment**: the backend runs as a Docker container (see
  `Nena_Back/Dockerfile`); the frontend builds to a static site with no
  server runtime required. See each subproject's README for deploy specifics.

## Testing

- Backend: `cd Nena_Back && python3 -m pytest tests/ -v` — auth, endpoint
  access control, recording upload/ownership, with external services
  (ffmpeg/AssemblyAI/Anthropic) mocked out.
- Frontend: `cd Nena-Front && node e2e/smoke.spec.js` — one end-to-end
  Playwright smoke test against real running dev servers.

Run the backend suite before any deploy; the frontend smoke test isn't part
of CI yet but is cheap enough to run manually before a release.
