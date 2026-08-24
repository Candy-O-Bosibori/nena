# Nena — Backend

Flask + PostgreSQL API for Nena, a speaking-practice app. Handles auth, topic
content, recording uploads, transcription (AssemblyAI), and LLM coaching
feedback (Anthropic).

## Stack

- **Flask 3** + **Flask-RESTful** — HTTP layer
- **Flask-SQLAlchemy** + **Flask-Migrate** (Alembic) — ORM and schema migrations
- **PostgreSQL** — database (some columns use Postgres-specific types — native
  `Enum`, JSON dialect type — so this must be Postgres, not SQLite, in every
  environment including tests)
- **Flask-JWT-Extended** + **Flask-Bcrypt** — auth (JWT access/refresh tokens,
  bcrypt password hashing)
- **Gunicorn** — production WSGI server (the Flask dev server, `app.run(debug=True)`,
  is used only for local development — see [Running locally](#running-locally))
- **ffmpeg** — audio extraction and duration probing from uploaded recordings
  (a **system** dependency, not a Python package — see [Prerequisites](#prerequisites))
- **pytest** — test suite (19 tests as of this writing: auth, public-endpoint
  access control, recording upload/ownership)

## Prerequisites

- Python 3.11
- PostgreSQL (running locally, or a connection string to a remote instance)
- ffmpeg (`apt install ffmpeg` / `brew install ffmpeg`) — required for the
  recording upload pipeline; the app will error on every upload without it
- API keys: [AssemblyAI](https://www.assemblyai.com/) (transcription),
  [Anthropic](https://console.anthropic.com/) (coaching feedback)

## Setup

```bash
cd Nena_Back
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# edit .env: set DATABASE_URL, SECRET_KEY, JWT_SECRET_KEY, and the two API keys

flask db upgrade         # create/update the schema (also creates the 5 practice modes)
python3 seeds/topics.py  # optional: seed topic content (idempotent -- no-ops if topics already exist)
```

> **Note:** there's also a `seed.py` at the repo root — it's stale (predates
> the current schema, references a `video_url` field that no longer exists,
> and calls `db.drop_all()`). Don't run it. `seeds/topics.py` is the current,
> safe, idempotent one.

### Environment variables

All read from `.env` locally (via `python-dotenv`) or from the process
environment in any deployed setting. See `.env.example` for the full list
with placeholder values.

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | Postgres connection string, e.g. `postgresql://user:pass@host:5432/dbname` |
| `SECRET_KEY` | Flask session secret — set to a real random value outside local dev |
| `JWT_SECRET_KEY` | Signs access/refresh tokens — set to a real random value outside local dev |
| `JWT_ACCESS_TOKEN_EXPIRES_MINUTES` | Access token lifetime (default 15) |
| `JWT_REFRESH_TOKEN_EXPIRES_DAYS` | Refresh token lifetime (default 7) |
| `ASSEMBLYAI_API_KEY` | Transcription |
| `ANTHROPIC_API_KEY` | Coaching feedback generation |
| `TRANSCRIPTION_LANGUAGE` | Language code passed to AssemblyAI (default `en`) |
| `CORS_ORIGINS` | Comma-separated allowed frontend origin(s), e.g. `https://your-frontend.example.com`. Unset/empty locally defaults to `*`; set explicitly in every deployed environment. |

Never commit real values — `.env` is gitignored; `.env.example` holds only
placeholders and is the thing that's actually tracked.

## Running locally

```bash
python3 app.py
```

Starts Flask's built-in dev server on `http://127.0.0.1:5000` with
auto-reload. **Not for production** — see [Docker](#docker) below for the
production entrypoint (gunicorn).

## Running with Docker

```bash
docker build -t nena-backend .
docker run -d --name nena-backend \
  --network host \
  --env-file .env \
  nena-backend
```

`--network host` is a local-dev-only convenience: it lets the container reach
a Postgres instance bound to `127.0.0.1` on the host machine (the default for
most local Postgres installs). In an actual deployment, the database is a
separate networked service (e.g. Railway's managed Postgres), so this flag
isn't needed there — the container just gets a `DATABASE_URL` pointing at a
real host.

Verify it's up:

```bash
curl http://localhost:5000/modes           # 200, public
curl http://localhost:5000/recordings      # 401, requires auth
```

The image runs under `gunicorn` (see the `CMD` in `Dockerfile`), not the
Flask dev server — that's the actual production entrypoint, exercised the
same way locally as it would be in any deployed environment.

## Testing

```bash
python3 -m pytest tests/ -v
```

Tests run against a dedicated `test` schema inside your normal local Postgres
database (no separate test database or extra role privileges required — see
`tests/README.md` for why, and how to point at a different database via
`TEST_DATABASE_URL` if needed). Every table is truncated between tests for
isolation. External services (ffmpeg, AssemblyAI, Anthropic) are mocked —
the suite never makes a real network call or costs money to run.

Coverage as of this writing:
- **`test_auth.py`** — signup, signin, duplicate-email rejection, token refresh
- **`test_public_endpoints.py`** — confirms exactly the 4 intentionally
  anonymous-accessible endpoints (`/modes`, `/topics`, `/topics/random`,
  `/topics/today`) are reachable without auth, and that everything else
  (`/recordings`, `/words`) still requires it — a regression guard against
  accidentally widening or narrowing the wrong endpoint
- **`test_recordings.py`** — upload flow (with external services mocked),
  auth requirement, file-extension validation, per-user ownership isolation

## API overview

All endpoints are JSON in/out unless noted. JWT identity is the stringified
user id (`create_access_token(identity=str(user.id))`); pass it as
`Authorization: Bearer <access_token>`.

| Method | Path | Auth | Notes |
|---|---|---|---|
| POST | `/signup` | — | Create account, returns tokens |
| POST | `/signin` | — | Returns tokens |
| POST | `/refresh` | refresh token | Rotates both tokens |
| GET | `/modes` | — | Public: practice mode list |
| GET | `/topics` | — | Public: all active topics |
| GET | `/topics/random` | — | Public: `?mode=<slug>&difficulty=<easy\|medium\|hard\|random>&tags=<csv>` |
| GET | `/topics/today` | — | Public: deterministic daily pick, e.g. `?mode=daily-reflection` |
| GET/POST | `/recordings` | required | List own recordings / upload a new one (`multipart/form-data`) |
| GET/DELETE | `/recordingById/<id>` | required, owner only | |
| GET | `/feedback/<recording_id>` | required, owner only | |
| GET/POST | `/words` | required | Vocabulary list |
| PATCH/DELETE | `/wordsById/<id>` | required, owner only | |
| GET | `/next-practice` | required | Recommended next topic |
| GET | `/trends` | required | 30-day performance trends |
| GET | `/frameworks` | — | Public: STAR/PREP/etc. reference content |
| GET | `/activity_logs` | required | |
| GET | `/coaching/stream/<recording_id>` | required, owner only | Server-sent events |
| GET/PATCH/DELETE | `/users`, `/userById/<id>` | required | |

`/modes`, `/topics`, `/topics/random`, and `/topics/today` are deliberately
public — they don't use identity for filtering or personalization, so
letting anonymous visitors browse content before signing up doesn't require
any auth changes beyond removing the decorator (see `resources/modes.py`,
`resources/topics.py`). Every other endpoint requires a valid access token.

## Project structure

```
app.py                 # Flask app instance, config, extension wiring, route registration
extensions.py          # bcrypt, jwt objects + JWT error handlers (401s, not 500s, on bad tokens)
models/                # SQLAlchemy models (User, Mode, Topic, Recording, Feedback, Word, ActivityLog)
resources/             # Flask-RESTful resources (one file per API area)
services/               # External integrations: transcription.py (ffmpeg + AssemblyAI), coaching.py (Anthropic)
migrations/             # Alembic migration history
seeds/                  # Topic content seed data + seed.py entrypoint
tests/                   # pytest suite (see Testing above)
Dockerfile, .dockerignore
```

## Deployment

Deployed as a Docker container (see `Dockerfile`) to Railway, alongside a
managed Postgres instance. Migrations (`flask db upgrade`) are run once
against the target database before the app serves traffic; they're not run
automatically on container start. See the deploy runbook (or ask in the
project's planning notes) for the current live URL and Railway project
setup.

Before deploying to a new environment for the first time:

1. Set every variable in [Environment variables](#environment-variables) with
   real values in the host's dashboard/secret store — never commit them.
2. Run `flask db upgrade` against the target database once.
3. Set `CORS_ORIGINS` to the actual deployed frontend origin(s) — the
   wildcard default is fine for local dev, not for a real deployment.
