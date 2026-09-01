import { useLayoutEffect, useRef, useState, Children, cloneElement } from "react";

// Renders the gravitational-field choreography for a grid of cards.
//
//   <GravityGrid count={6}>
//     <div>...</div>   x N   (each child gets .gravity-cell)
//   </GravityGrid>
//
// On mount each cell is given a direction toward the grid center via
// --gx/--gy and animates in with .warp-in. On hover a magnetic pull follows
// the cursor via --mx/--my.
export default function GravityGrid({ children, className = "", gap = 96 }) {
  const fieldRef = useRef(null);
  const [phase, setPhase] = useState("spin-up");

  const cellCount = Children.count(children);

  useLayoutEffect(() => {
    const raf = requestAnimationFrame(() => setPhase("entered"));
    return () => cancelAnimationFrame(raf);
  }, []);

  // Compute direction offsets toward the center for each child.
  useLayoutEffect(() => {
    if (phase !== "entered") return;
    const field = fieldRef.current;
    if (!field) return;
    // re-measure on counts change only the first time
    const cells = Array.from(field.querySelectorAll(".gravity-cell"));
    if (cells.length === 0) return;

    const fieldRect = field.getBoundingClientRect();
    const cx = fieldRect.left + fieldRect.width / 2;
    const cy = fieldRect.top + fieldRect.height / 2;

    cells.forEach((cell, i) => {
      const r = cell.getBoundingClientRect();
      const cellCx = r.left + r.width / 2;
      const cellCy = r.top + r.height / 2;

      let dx = cx - cellCx;
      let dy = cy - cellCy - gap; // pull slightly above center for a sink feel
      const mag = Math.hypot(dx, dy) || 1;
      dx = (dx / mag) * 70;
      dy = (dy / mag) * 70;

      cell.style.setProperty("--gx", `${dx}px`);
      cell.style.setProperty("--gy", `${dy}px`);
      cell.style.animationDelay = `${i * 70}ms`;
    });
  }, [phase, cellCount, gap]);

  // Live magnetic pull per cell.
  useLayoutEffect(() => {
    if (phase !== "entered") return;
    const field = fieldRef.current;
    if (!field) return;
    const cells = Array.from(field.querySelectorAll(".gravity-cell"));

    const onMove = (e) => {
      for (const cell of cells) {
        const r = cell.getBoundingClientRect();
        const cellCx = r.left + r.width / 2;
        const cellCy = r.top + r.height / 2;
        let mx = (e.clientX - cellCx) * 0.12;
        let my = (e.clientY - cellCy) * 0.12;
        mx = Math.max(-16, Math.min(16, mx));
        my = Math.max(-12, Math.min(12, my));
        cell.style.setProperty("--mx", `${mx}px`);
        cell.style.setProperty("--my", `${my}px`);
      }
    };
    const onLeave = () => {
      for (const cell of cells) {
        cell.style.setProperty("--mx", "0px");
        cell.style.setProperty("--my", "0px");
      }
    };

    field.addEventListener("mousemove", onMove);
    field.addEventListener("mouseleave", onLeave);
    return () => {
      field.removeEventListener("mousemove", onMove);
      field.removeEventListener("mouseleave", onLeave);
    };
  }, [phase]);

  const kids = Children.map(children, (child, i) =>
    cloneElement(child, {
      className: `${child.props.className || ""} gravity-cell warp-in ${
        phase === "entered" ? "magnetic" : ""
      } settled`.trim(),
      style: { ...(child.props.style || {}), animationDelay: `${i * 70}ms` },
    })
  );

  return (
    <div className="gravity-viewport">
      <div ref={fieldRef} className={`gravity-field grid gap-3 ${className}`}>
        {kids}
      </div>
    </div>
  );
}
