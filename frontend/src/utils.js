export const CATEGORIES = [
  "study",
  "work",
  "social",
  "entertainment",
  "other",
  "unknown",
];

export const CATEGORY_LABELS = {
  study: "Study",
  work: "Work",
  social: "Social",
  entertainment: "Entertainment",
  other: "Other",
  unknown: "Unknown",
};

export const CATEGORY_COLORS = {
  study: "#2545d6",
  work: "#1f8a70",
  social: "#d6458a",
  entertainment: "#d97706",
  other: "#7a5cd6",
  unknown: "#9a9184",
};

export function formatDuration(seconds) {
  const s = Math.round(Number(seconds) || 0);
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  if (h > 0) return `${h}h ${m}m`;
  if (m > 0) return `${m}m`;
  return `${s}s`;
}

export function formatDateTime(iso) {
  return new Date(iso).toLocaleString();
}