import { useEffect, useRef, useState } from "react";
import { del, get, patch } from "../api";
import {
  CATEGORIES,
  CATEGORY_COLORS,
  CATEGORY_LABELS,
  formatDateTime,
  formatDuration,
} from "../utils";
import useStagger from "../hooks/useStagger";

export default function Activities() {
  const [activities, setActivities] = useState([]);
  const rootRef = useRef(null);
  useStagger(rootRef, { count: 12 });

  async function load() {
    try {
      setActivities(await get("/activities"));
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function changeCategory(id, category) {
    await patch(`/activities/${id}/category`, { category });
    load();
  }

  async function remove(id) {
    await del(`/activities/${id}`);
    load();
  }

  if (activities.length === 0) {
    return (
      <div ref={rootRef} className="card reveal p-10 text-center text-ink-faint">
        No activity recorded yet. Load the extension and browse for a while.
      </div>
    );
  }

  return (
    <div ref={rootRef}>
      <div className="reveal mb-6">
        <p className="eyebrow mb-2">Ledger</p>
        <h1 className="font-display text-4xl font-semibold tracking-tight text-ink">
          Activities
        </h1>
      </div>

      <div className="card reveal overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-paper-deep/60 text-left">
            <tr className="eyebrow">
              <th className="px-5 py-3 font-medium">Title</th>
              <th className="px-5 py-3 font-medium">Website</th>
              <th className="px-5 py-3 font-medium">Started</th>
              <th className="px-5 py-3 font-medium text-right">Duration</th>
              <th className="px-5 py-3 font-medium">Category</th>
              <th className="px-5 py-3 font-medium text-right"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-line">
            {activities.map((activity) => (
              <tr key={activity.id} className="hover:bg-paper/60 transition-colors">
                <td className="px-5 py-3 text-ink max-w-[20rem] truncate font-display">
                  {activity.title}
                </td>
                <td className="px-5 py-3 text-ink-soft font-mono text-xs">
                  {activity.domain}
                </td>
                <td className="px-5 py-3 text-ink-soft whitespace-nowrap font-mono text-xs">
                  {formatDateTime(activity.started_at)}
                </td>
                <td className="px-5 py-3 text-right text-ink font-mono tabular-nums">
                  {formatDuration(activity.duration)}
                </td>
                <td className="px-5 py-3">
                  <span
                    className="inline-block w-2 h-2 rounded-full mr-2"
                    style={{ background: CATEGORY_COLORS[activity.category] }}
                  />
                  <select
                    value={activity.category}
                    onChange={(e) => changeCategory(activity.id, e.target.value)}
                    className="font-display text-sm border border-line rounded-md px-2 py-1 bg-card"
                    style={{ color: CATEGORY_COLORS[activity.category] }}
                  >
                    {CATEGORIES.map((category) => (
                      <option key={category} value={category}>
                        {CATEGORY_LABELS[category]}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="px-5 py-3 text-right">
                  <button
                    type="button"
                    onClick={() => remove(activity.id)}
                    className="font-mono text-xs text-ink-faint hover:text-red-600 transition-colors"
                  >
                    delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
