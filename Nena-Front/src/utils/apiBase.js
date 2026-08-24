// Single source of truth for the backend's base URL. Vite bakes
// import.meta.env.VITE_* into the build at build time, so this becomes a
// per-environment value (local dev, CI, production) rather than something
// hardcoded per file. Falls back to the old hardcoded local value so an
// unset env var doesn't silently break local dev.
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:5000";
