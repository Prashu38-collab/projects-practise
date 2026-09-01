import { useEffect, useRef, useState } from "react";
import { get, patch } from "../api";
import CategoryPicker from "../components/CategoryPicker";
import GravityGrid from "../components/GravityGrid";
import {
  CATEGORIES,
  CATEGORY_COLORS,
  CATEGORY_LABELS,
  formatDuration,
} from "../utils";
import useStagger from "../hooks/useStagger";

function categorySeconds(summary, category) {
  const entry = (summary?.by_category || []).find((c) => c.category === category);
  return entry ? entry.seconds : 0;
}

export default function Dashboard() {
  const [today, setToday] = useState(null);
  const [websites, setWebsites] = useState([]);
  const [review, setReview] = useState([]);
  const rootRef = useRef(null);
  useStagger(rootRef, { count: 8 });

  async function load() {
    try {
      const [todayData, websiteData, reviewData] = await Promise.all([
        get("/analytics/today"),
        get("/analytics/websites?limit=5"),
        get("/activities/review"),
      ]);
      setToday(todayData);
      setWebsites(websiteData);
      setReview(reviewData);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function classify(id, category) {
    await patch(`/activities/${id}/category`, { category });
    load();
  }

  const maxWebsiteSeconds =
    websites.length > 0 ? Math.max(...websites.map((w) => w.seconds)) : 1;
  const dateLabel = new Date().toLocaleDateString(undefined, {
    weekday: "long",
    month: "long",
    day: "numeric",
  });

  return (
    <div ref={rootRef}>
      <div className="reveal mb-8">
        <p className="eyebrow mb-2">{dateLabel}</p>
        <h1 className="font-display text-4xl sm:text-5xl font-semibold tracking-tight text-ink">
          How did you spend it?
        </h1>
        <p className="mt-2 text-ink-soft max-w-xl">
          A ledger of today&rsquo;s browsing — the focused, the fun, and the
          undecided.
        </p>
      </div>

      <GravityGrid className="grid-cols-2 md:grid-cols-3 mb-6">
        {CATEGORIES.map((category) => {
          const seconds = categorySeconds(today, category);
          const isReview = category === "unknown";
          return (
            <div
              key={category}
              className="card p-5"
              style={{ borderTop: `3px solid ${CATEGORY_COLORS[category]}` }}
            >
              <div className="eyebrow">{CATEGORY_LABELS[category]}</div>
              <div
                className="stat-value mt-2 text-3xl"
                style={{ color: CATEGORY_COLORS[category] }}
              >
                {formatDuration(seconds)}
              </div>
              <div className="mt-1 text-xs text-ink-faint">
                {isReview && seconds > 0 ? "needs your call" : "\u00A0"}
              </div>
            </div>
          );
        })}
      </GravityGrid>

      <div className="grid md:grid-cols-2 gap-4">
        <section className="card reveal p-6">
          <h2 className="eyebrow mb-4">Top Websites</h2>
          {websites.length === 0 ? (
            <p className="text-ink-faint">No data yet.</p>
          ) : (
            <ul className="space-y-3">
              {websites.map((website) => (
                <li key={website.domain} className="flex items-center gap-3">
                  <span className="w-1/2 truncate text-ink">
                    {website.domain || "(no domain)"}
                  </span>
                  <div className="flex-1 h-2 rounded-full bg-paper-deep overflow-hidden">
                    <div
                      className="h-full rounded-full bg-accent transition-all duration-700"
                      style={{
                        width: `${Math.max(4, (website.seconds / maxWebsiteSeconds) * 100)}%`,
                      }}
                    />
                  </div>
                  <span className="stat-value text-sm text-ink-soft tabular-nums">
                    {formatDuration(website.seconds)}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="card reveal p-6">
          <h2 className="eyebrow mb-4">Needs Review</h2>
          {review.length === 0 ? (
            <div className="text-ink-faint flex flex-col items-center py-6 text-center">
              <span className="font-display text-3xl mb-2 text-ink-faint">✓</span>
              <p>Nothing pending. Everything is accounted for.</p>
            </div>
          ) : (
            <ul className="space-y-4">
              {review.slice(0, 5).map((activity) => (
                <li key={activity.id}>
                  <div className="flex items-baseline justify-between gap-2">
                    <div className="text-sm font-medium text-ink truncate">
                      {activity.title}
                    </div>
                    <div className="text-xs text-ink-faint whitespace-nowrap">
                      {formatDuration(activity.duration)}
                    </div>
                  </div>
                  <div className="mt-1.5">
                    <CategoryPicker onPick={(c) => classify(activity.id, c)} />
                  </div>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  );
}
