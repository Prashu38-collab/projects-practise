import { NavLink, Outlet, useLocation } from "react-router-dom";
import { useEffect } from "react";

const links = [
  { to: "/", label: "Dashboard", end: true },
  { to: "/activities", label: "Activities", end: false },
  { to: "/review", label: "Review", end: false },
  { to: "/analytics", label: "Analytics", end: false },
];

export default function Layout() {
  const location = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [location.pathname]);

  return (
    <div className="min-h-screen">
      <header className="sticky top-0 z-20 backdrop-blur-md bg-paper/85 border-b border-line">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between gap-6">
          <div className="flex items-baseline gap-3">
            <span className="font-display font-bold text-xl tracking-tight text-ink">
              Study<span className="text-amber">·</span>Activity
            </span>
            <span className="eyebrow hidden sm:inline">Analyzer</span>
          </div>

          <nav className="flex gap-1 flex-wrap justify-end">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.end}
                className={({ isActive }) =>
                  `relative px-3 py-1.5 text-sm font-display font-medium transition-colors ${
                    isActive ? "text-accent" : "text-ink-soft hover:text-ink"
                  }`
                }
              >
                {({ isActive }) => (
                  <>
                    {link.label}
                    <span
                      className={`absolute left-3 right-3 -bottom-0.5 h-0.5 rounded-full bg-accent transition-transform origin-left ${
                        isActive ? "scale-x-100" : "scale-x-0"
                      }`}
                    />
                  </>
                )}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <Outlet />
      </main>
    </div>
  );
}
