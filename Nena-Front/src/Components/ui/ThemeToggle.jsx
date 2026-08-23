import React from "react";
import { FiSun, FiMoon, FiMonitor } from "react-icons/fi";
import { useTheme } from "../../useTheme";

const OPTIONS = [
  { value: "light", label: "Light", Icon: FiSun },
  { value: "system", label: "Match system", Icon: FiMonitor },
  { value: "dark", label: "Dark", Icon: FiMoon },
];

/** Three-way segmented control: light / system / dark. */
export const ThemeToggle = ({ className = "" }) => {
  const { preference, setTheme } = useTheme();

  return (
    <div
      role="radiogroup"
      aria-label="Theme"
      className={`inline-flex items-center gap-0.5 rounded-full border border-line bg-cream p-1 ${className}`}
    >
      {OPTIONS.map(({ value, label, Icon }) => {
        const active = preference === value;
        return (
          <button
            key={value}
            type="button"
            role="radio"
            aria-checked={active}
            aria-label={label}
            title={label}
            onClick={() => setTheme(value)}
            className={[
              "flex h-7 w-7 items-center justify-center rounded-full transition-all duration-200 focus-ring",
              active
                ? "bg-primary text-on-primary shadow-sm"
                : "text-ink-muted hover:text-ink",
            ].join(" ")}
          >
            <Icon size={14} />
          </button>
        );
      })}
    </div>
  );
};

export default ThemeToggle;
