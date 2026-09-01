import { CATEGORIES, CATEGORY_COLORS, CATEGORY_LABELS } from "../utils";

export default function CategoryPicker({ value, onPick }) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {CATEGORIES.map((category) => (
        <button
          key={category}
          type="button"
          onClick={() => onPick(category)}
          style={{
            color: value === category ? "#fff" : CATEGORY_COLORS[category],
            borderColor: value === category ? CATEGORY_COLORS[category] : "var(--line)",
            backgroundColor: value === category ? CATEGORY_COLORS[category] : "transparent",
            boxShadow:
              value === category
                ? `0 4px 12px -4px ${CATEGORY_COLORS[category]}`
                : "none",
          }}
          className={`px-3 py-1 rounded-full text-xs font-medium border transition-all hover:-translate-y-0.5 ${
            value !== category ? "hover:bg-paper-deep" : ""
          }`}
        >
          {CATEGORY_LABELS[category]}
        </button>
      ))}
    </div>
  );
}