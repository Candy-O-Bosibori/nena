# Nena — Frontend

React + Vite client for Nena, a speaking-practice app: pick a prompt, record
yourself answering it, get coaching feedback on pace, filler words, and
structure.

## Stack

- **React** + **Vite** — app shell and build tooling
- **React Router** — routing, incl. anonymous-vs-authenticated route gating
- **Tailwind CSS v4** — styling via design tokens in `src/index.css` (`@theme` block) —
  not `tailwind.config.js`, which only configures plugins/content globs here
- **Headless UI** — accessible dropdown/accordion primitives (difficulty
  picker, framework list)
- **Axios** — API client (`src/api/api.js`) with automatic token-refresh-and-retry
  on 401
- **react-toastify** — the app-wide toast/notification standard (not `react-hot-toast`,
  which isn't wired up anywhere)
- **MediaRecorder API** (browser-native) — audio capture in the practice flow

## Prerequisites

- Node.js
- A running instance of the backend (`../Nena_Back`) — see its README

## Setup

```bash
cd Nena-Front
npm install

cp .env.example .env
# edit .env if the backend isn't at the default http://127.0.0.1:5000
```

### Environment variables

| Variable | Purpose |
|---|---|
| `VITE_API_BASE_URL` | Base URL of the backend API. Read at **build time** — Vite bakes `import.meta.env.VITE_*` into the static output, so this becomes a per-environment build setting (local/staging/production), not something the running app can change at runtime. |

`.env` is gitignored; `.env.example` holds the local-dev default and is the
tracked template. Every API call in the app resolves this through one shared
module, `src/utils/apiBase.js` — if you're adding a new API call, import
`API_BASE_URL` from there rather than hardcoding a host.

## Running locally

```bash
npm run dev
```

Starts the Vite dev server (default `http://localhost:5173`, or the next
free port if that's taken) with hot module reload, talking to whatever
backend `VITE_API_BASE_URL` points at.

## Building for production

```bash
npm run build
```

Outputs a static site to `dist/` — plain HTML/CSS/JS, no server-side
runtime required. Preview the production build locally with:

```bash
npm run preview
```

## Testing

```bash
node e2e/smoke.spec.js
```

One end-to-end smoke test (Playwright): signs up a fresh account, confirms
landing on `/overview`, confirms modes and topic content render, confirms no
console errors. Requires both the backend and `npm run dev` running first
(see `e2e/smoke.spec.js` for the full requirements and an optional
`PLAYWRIGHT_PATH` env var if Playwright isn't installed as a project
dependency yet).

This is intentionally a thin smoke check, not a full test suite — see the
backend's `tests/` for the more thorough coverage (auth, ownership,
endpoint access control), which is where most real regressions are caught
before they'd ever reach the UI layer.

## Anonymous vs. authenticated routes

Not every page requires an account. `src/routes.jsx` marks each route with
`isAuthenticated: true | false`; `App.jsx` reads that flag to decide whether
to wrap the route in `AuthWrapper` (which redirects to `/signin` if there's
no valid token) or render it directly.

- **Public** (`isAuthenticated: false`): `/`, `/overview`, `/practice/:modeSlug`,
  `/signin`, `/signup` — a visitor can browse modes, spin for a topic, and
  even record themselves without an account.
- **Requires an account**: `/feedback`, `/recording`, `/profile`, `/vocab` —
  anything that reads or writes user-specific data.

Submitting a recording for feedback always requires an account (a `Recording`
row needs a real `user_id`). An anonymous visitor who tries is shown a
sign-up prompt instead of a raw 401; if they sign up or sign in from that
prompt, their in-progress recording is preserved (via IndexedDB, see
`src/utils/draftRecording.js`) and they're returned to the same practice
page to finish submitting — the recording is never silently lost.

## Project structure

```
src/
  api/api.js              # Axios instance, request/response interceptors, token refresh
  AuthWraper.jsx           # Route guard for authenticated-only pages
  Components/              # Shared UI (Button, ThemeToggle, Layout, SideBar, CircularTimer, ...)
  pages/                    # One folder per route (overview, practice, feedback, profile, vocab, login, signup)
  utils/
    apiBase.js               # Single source of truth for the backend base URL
    draftRecording.js         # IndexedDB persistence for in-progress recordings across sign-up
    format.js                  # Display formatting helpers
  routes.jsx                # Route table incl. auth requirements
  index.css                  # Tailwind v4 design tokens (colors, fonts) via @theme
e2e/smoke.spec.js           # End-to-end smoke test (see Testing above)
```

## Deployment

Built as a static site (`npm run build` → `dist/`) — no Node runtime needed
in production, no Docker required for this piece. `VITE_API_BASE_URL` must
be set to the deployed backend's real URL at build time in whatever CI/host
builds it. See the backend README's Deployment section for the paired
backend deploy (Railway, containerized).
