const STORAGE_KEY = "nena-theme"; // "light" | "dark" | "system"

const prefersDark = () =>
  typeof window !== "undefined" &&
  window.matchMedia?.("(prefers-color-scheme: dark)").matches;

const resolve = (pref) => (pref === "system" ? (prefersDark() ? "dark" : "light") : pref);

/** Apply light/dark to <html>. Safe to call before React mounts. */
export const applyTheme = (pref) => {
  const resolved = resolve(pref);
  document.documentElement.classList.toggle("dark", resolved === "dark");
  return resolved;
};

export const getStoredPreference = () => {
  try {
    return localStorage.getItem(STORAGE_KEY) || "system";
  } catch {
    return "system";
  }
};

export const setThemePreference = (pref) => {
  try {
    localStorage.setItem(STORAGE_KEY, pref);
  } catch {
    // localStorage unavailable (private mode, etc.) — theme just won't persist.
  }
  return applyTheme(pref);
};

/** Called once from main.jsx, before ReactDOM renders, to avoid a flash of the
 * wrong theme on load. */
export const initTheme = () => applyTheme(getStoredPreference());
