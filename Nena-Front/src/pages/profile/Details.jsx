import React from 'react'
import { CiEdit } from "react-icons/ci";

const initialsOf = (name = "") =>
  name
    .split(" ")
    .filter(Boolean)
    .slice(0, 2)
    .map((n) => n[0]?.toUpperCase())
    .join("");

const Row = ({ label, value, onEdit }) => (
  <div className="flex items-center justify-between py-4">
    <div className="min-w-0">
      <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-ink-muted">{label}</p>
      <p className="mt-1 truncate text-base text-ink">{value}</p>
    </div>
    <button
      type="button"
      onClick={onEdit}
      aria-label={`Edit ${label.toLowerCase()}`}
      className="shrink-0 rounded-full p-2 text-ink-muted transition-colors hover:bg-cream hover:text-primary-700 focus-ring"
    >
      <CiEdit className="h-5 w-5" />
    </button>
  </div>
);

export const Details = ({ user, setShowNameModal, setShowPasswordModal, setShowEmailModal }) => {
  return (
    <div className="rounded-2xl border border-line bg-surface px-6 py-6">
      <div className="flex items-center gap-4 pb-5 border-b border-line">
        <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-primary text-lg font-bold text-on-primary">
          {initialsOf(user.name) || "?"}
        </span>
        <div className="min-w-0">
          <p className="truncate text-lg font-bold text-ink">{user.name || "—"}</p>
          <p className="truncate text-sm text-ink-muted">{user.email || "—"}</p>
        </div>
      </div>

      <div className="divide-y divide-line">
        <Row label="Name" value={user.name || "—"} onEdit={() => setShowNameModal(true)} />
        <Row label="Email" value={user.email || "—"} onEdit={() => setShowEmailModal(true)} />
        <Row label="Password" value="••••••••" onEdit={() => setShowPasswordModal(true)} />
      </div>
    </div>
  );
};
