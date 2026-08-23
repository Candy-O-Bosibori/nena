import React from "react";

/**
 * Shared button. Variants map to Nena's palette so pages never hand-roll
 * colours; sizes keep every tap target at least 44px tall on touch.
 *
 * Gold (--color-primary) is too light to use as text or as white-on-fill:
 * white-on-gold is ~1.6:1 contrast (checked, fails WCAG AA badly), and gold
 * text on anything light is similarly unreadable. Fill buttons use
 * `text-on-primary` (resolves to the forest ink, 7.8:1); any hover/link text
 * that used to say `text-primary` should say `text-primary-700` instead.
 */
const VARIANTS = {
  primary:
    "bg-primary text-on-primary shadow-sm hover:bg-primary-hover active:scale-[0.98]",
  secondary:
    "bg-surface text-ink border border-line hover:border-ink-muted active:scale-[0.98]",
  ghost:
    "bg-transparent text-ink-soft hover:bg-primary-soft hover:text-primary-700",
  danger:
    "bg-surface text-danger border border-danger/30 hover:bg-danger/5 active:scale-[0.98]",
};

const SIZES = {
  sm: "text-sm px-4 py-2 rounded-xl",
  md: "text-sm px-5 py-3 rounded-2xl",
  lg: "text-base px-8 py-4 rounded-full",
};

export const Button = ({
  variant = "primary",
  size = "md",
  className = "",
  disabled,
  children,
  ...props
}) => (
  <button
    disabled={disabled}
    className={[
      "inline-flex items-center justify-center gap-2 font-semibold",
      "transition-all duration-200 focus-ring",
      "disabled:opacity-40 disabled:pointer-events-none",
      VARIANTS[variant] || VARIANTS.primary,
      SIZES[size] || SIZES.md,
      className,
    ].join(" ")}
    {...props}
  >
    {children}
  </button>
);

export default Button;
