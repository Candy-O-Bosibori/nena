import { useCallback, useEffect, useState } from "react";
import { getStoredPreference, setThemePreference } from "./theme";

/** preference: "light" | "dark" | "system". resolved: "light" | "dark" (what's
 * actually applied right now, useful for icon state). */
export const useTheme = () => {
  const [preference, setPreference] = useState(getStoredPreference);
  const [resolved, setResolved] = useState(
    () => document.documentElement.classList.contains("dark")
      ? "dark"
      : "light"
  );

  const setTheme = useCallback((pref) => {
    setPreference(pref);
    setResolved(setThemePreference(pref));
  }, []);

  const toggle = useCallback(() => {
    setTheme(resolved === "dark" ? "light" : "dark");
  }, [resolved, setTheme]);

  // If the user is on "system", keep resolved in sync with OS changes.
  useEffect(() => {
    if (preference !== "system") return;
    const mql = window.matchMedia("(prefers-color-scheme: dark)");
    const onChange = () => setResolved(setThemePreference("system"));
    mql.addEventListener("change", onChange);
    return () => mql.removeEventListener("change", onChange);
  }, [preference]);

  return { preference, resolved, setTheme, toggle };
};

export default useTheme;
