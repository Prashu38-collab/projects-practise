import { useEffect, useRef, useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { get } from "../api";
import { CATEGORIES, CATEGORY_COLORS, CATEGORY_LABELS, formatDuration } from "../utils";
import useStagger from "../hooks/useStagger";

const axisTick = { fill: "#6b6458", fontFamily: "IBM Plex Mono", fontSize: 11 };

export default function Analytics() {
  const [today, setToday] = useState(null);
  const [websites, setWebsites] = useState([]);
  const [daily, setDaily] = useState([]);
  const rootRef = useRef(null);
  useStagger(rootRef, { count: 3 });

  useEffect(() => {
    get("/analytics/today").then(setToday).catch(console.error);
    get("/analytics/websites?limit=8").then(setWebsites).catch(console.error);
    get("/analytics/daily?days=7").then(setDaily).catch(console.error);
  }, []);

  const pieData = (today?.by_category || []).filter((c) => c.seconds > 0);
  const barData = daily.map((day) => ({
    date: day.date.slice(5),
    ...day.by_category,
  }));

  const maxWebsiteSeconds =
    websites.length > 0 ? Math.max(...websites.map((w) => w.seconds)) : 1;

  return (
    <div ref={rootRef}>
      <div className="reveal mb-6">
        <p className="eyebrow mb-2">Signal</p>
        <h1 className="font-display text-4xl font-semibold tracking-tight text-ink">
          Analytics
        </h1>
      </div>

      <div className="grid lg:grid-cols-2 gap-4 mb-4">
        <section className="card reveal p-6">
          <h2 className="eyebrow mb-4">Today by Category</h2>
          {pieData.length === 0 ? (
            <p className="text-ink-faint">No activity recorded today.</p>
          ) : (
            <ResponsiveContainer width="100%" height={240}>
              <PieChart>
                <Pie
                  data={pieData}
                  dataKey="seconds"
                  nameKey="category"
                  innerRadius={52}
                  outerRadius={92}
                  paddingAngle={2}
                  stroke="#fffdf7"
                  strokeWidth={2}
                >
                  {pieData.map((entry) => (
                    <Cell key={entry.category} fill={CATEGORY_COLORS[entry.category]} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value) => formatDuration(Number(value))}
                  contentStyle={{
                    background: "#fffdf7",
                    border: "1px solid #e3dac8",
                    borderRadius: 10,
                    fontFamily: "IBM Plex Mono",
                  }}
                />
                <Legend formatter={(v) => <span style={{ color: "#6b6458" }}>{v}</span>} />
              </PieChart>
            </ResponsiveContainer>
          )}
        </section>

        <section className="card reveal p-6">
          <h2 className="eyebrow mb-4">Last 7 Days</h2>
          <ResponsiveContainer width="100%" height={240}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e3dac8" />
              <XAxis dataKey="date" tick={axisTick} axisLine={false} tickLine={false} />
              <YAxis tick={axisTick} axisLine={false} tickLine={false} />
              <Tooltip
                formatter={(value) => formatDuration(Number(value))}
                contentStyle={{
                  background: "#fffdf7",
                  border: "1px solid #e3dac8",
                  borderRadius: 10,
                  fontFamily: "IBM Plex Mono",
                }}
              />
              <Legend wrapperStyle={{ color: "#6b6458" }} />
              {CATEGORIES.map((category) => (
                <Bar
                  key={category}
                  dataKey={category}
                  stackId="a"
                  fill={CATEGORY_COLORS[category]}
                  name={CATEGORY_LABELS[category]}
                  radius={category === "unknown" ? [4, 4, 0, 0] : [0, 0, 0, 0]}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </section>
      </div>

      <section className="card reveal p-6">
        <h2 className="eyebrow mb-4">Most Used Websites</h2>
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
    </div>
  );
}
