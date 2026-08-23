/**
 * Number formatting helpers that tolerate whatever the API sends.
 *
 * Postgres AVG() over an integer column comes back as a Decimal, which Flask
 * serializes as a JSON *string* ("1.10"). Calling .toFixed() on that throws, and
 * optional chaining does not help because the property genuinely exists -- it is
 * just a string. These helpers coerce first, so a formatting call can never
 * bring the page down.
 */

/** Coerce to a finite number, or null if it isn't one. */
export const toNumber = (value) => {
  if (value === null || value === undefined || value === "") return null;
  const n = typeof value === "number" ? value : Number(value);
  return Number.isFinite(n) ? n : null;
};

/** Fixed-decimal string, or `fallback` when the value isn't numeric. */
export const fmt = (value, decimals = 1, fallback = "") => {
  const n = toNumber(value);
  return n === null ? fallback : n.toFixed(decimals);
};

/** Rounded integer string, or `fallback` when the value isn't numeric. */
export const fmtInt = (value, fallback = "") => {
  const n = toNumber(value);
  return n === null ? fallback : String(Math.round(n));
};

/** Ratio (0..1) rendered as a whole percentage, e.g. 0.41 -> "41". */
export const fmtPercent = (value, fallback = "") => {
  const n = toNumber(value);
  return n === null ? fallback : String(Math.round(n * 100));
};
