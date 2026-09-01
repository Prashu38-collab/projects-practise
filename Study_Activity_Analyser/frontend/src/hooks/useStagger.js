import { useEffect } from "react";

// After the route mounts, tag children with staggered reveal delays.
// Elements with class="reveal" get a progressive animation-delay via the
// --reveal-gap variable so cards cascade in on page load.
export default function useStagger(containerRef, { count = 8, gap = 80 } = {}) {
  useEffect(() => {
    const node = containerRef.current;
    if (!node) return;
    const items = node.querySelectorAll(".reveal");
    items.forEach((el, i) => {
      el.style.animationDelay = `${(i % count) * gap}ms`;
    });
  }, [containerRef, count, gap]);
}
