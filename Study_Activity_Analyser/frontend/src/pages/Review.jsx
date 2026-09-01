import { useEffect, useRef, useState } from "react";
import { get, patch } from "../api";
import CategoryPicker from "../components/CategoryPicker";
import { formatDateTime, formatDuration } from "../utils";
import useStagger from "../hooks/useStagger";

export default function Review() {
  const [items, setItems] = useState([]);
  const [message, setMessage] = useState("");
  const rootRef = useRef(null);
  useStagger(rootRef, { count: 6 });

  async function load() {
    try {
      setItems(await get("/activities/review"));
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function classify(id, category) {
    await patch(`/activities/${id}/category`, { category });
    setMessage(`Classified activity #${id} as "${category}".`);
    load();
  }

  return (
    <div ref={rootRef}>
      <div className="reveal mb-6">
        <p className="eyebrow mb-2">Triage</p>
        <h1 className="font-display text-4xl font-semibold tracking-tight text-ink">
          Needs Review
        </h1>
        <p className="mt-2 text-ink-soft max-w-xl">
          These defied simple rules. Your call teaches the system.
        </p>
      </div>

      {message ? (
        <p className="reveal mb-4 font-display text-accent">{message}</p>
      ) : null}

      {items.length === 0 ? (
        <div className="card reveal p-10 text-center text-ink-faint flex flex-col items-center">
          <span className="font-display text-4xl mb-2">✓</span>
          <p>Review queue is empty — nothing uncertain right now.</p>
        </div>
      ) : (
        <div className="space-y-4">
          {items.map((activity) => (
            <div key={activity.id} className="card reveal p-6">
              <div className="flex items-baseline justify-between gap-4 flex-wrap">
                <div className="min-w-0">
                  <div className="font-display text-lg font-medium text-ink truncate">
                    {activity.title}
                  </div>
                  <div className="font-mono text-xs text-ink-faint mt-1">
                    {activity.domain} · {formatDateTime(activity.started_at)} ·{" "}
                    {formatDuration(activity.duration)}
                  </div>
                </div>
              </div>
              <div className="mt-4">
                <CategoryPicker onPick={(c) => classify(activity.id, c)} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
