import React from "react";

/**
 * Small pill used for filters (difficulty) and mode tabs.
 * `accent` lets a mode tint itself with its own accent_color when active.
 *
 * Text is always the forest ink, never white: mode accent colors sit on the
 * gold/orange scales, which are light even at their darkest shades (checked —
 * white only clears 4.5:1 contrast at shade 800+, forest clears it
 * everywhere). Using ink uniformly means any accent_color the backend sends
 * stays readable without per-color-value contrast checking at render time.
 */
export const Chip = ({
  active = false,
  accent,
  className = "",
  children,
  ...props
}) => {
  const style =
    active && accent ? { backgroundColor: accent, borderColor: accent } : undefined;

  return (
    <button
      style={style}
      className={[
        "inline-flex items-center gap-2 whitespace-nowrap rounded-full border",
        "px-4 py-2 text-sm font-semibold transition-all duration-200 focus-ring",
        active
          ? accent
            ? "text-ink border-transparent shadow-sm"
            : "bg-primary text-on-primary border-transparent shadow-sm"
          : "bg-surface/70 text-ink-soft border-line hover:border-ink-muted hover:text-ink",
        className,
      ].join(" ")}
      {...props}
    >
      {children}
    </button>
  );
};

export default Chip;
