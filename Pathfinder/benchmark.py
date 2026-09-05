"""
Algorithm Comparison Engine
Runs two selected pathfinding algorithms on identical dual grid clones
and generates side-by-side comparative benchmarking analytics.
"""

import copy
import time
from grid import Grid
from ui.theme import (
    COLOR_PANEL_BG, COLOR_PANEL_BORDER, COLOR_TEXT_BRIGHT, COLOR_TEXT_MUTED,
    COLOR_SUCCESS, COLOR_PRIMARY, COLOR_WARNING, COLOR_DANGER, get_font
)

class BenchmarkEngine:
    def __init__(self, original_grid):
        self.original_grid = original_grid
        self.grid_a = None
        self.grid_b = None
        
        self.algo_a_name = "A* Search"
        self.algo_b_name = "Dijkstra's Algorithm"
        
        self.stats_a = {"name": "", "visited": 0, "path_length": 0, "path_cost": 0, "time_ms": 0.0, "found": False}
        self.stats_b = {"name": "", "visited": 0, "path_length": 0, "path_cost": 0, "time_ms": 0.0, "found": False}

    def setup_comparison(self, algo_a_name, algo_b_name):
        self.algo_a_name = algo_a_name
        self.algo_b_name = algo_b_name

    def run_benchmark(self, algo_func_a, algo_func_b, allow_diagonals=False):
        """Executes both algorithms instantly on cloned grid instances and measures performance metrics."""
        # 1. Clone Grid for Algorithm A
        self.grid_a = Grid(self.original_grid.rows, self.original_grid.cols, self.original_grid.node_size)
        self._copy_grid_state(self.original_grid, self.grid_a)

        # 2. Clone Grid for Algorithm B
        self.grid_b = Grid(self.original_grid.rows, self.original_grid.cols, self.original_grid.node_size)
        self._copy_grid_state(self.original_grid, self.grid_b)

        # 3. Benchmark Algo A
        start_t = time.perf_counter()
        gen_a = algo_func_a(self.grid_a, allow_diagonals=allow_diagonals)
        res_a = None
        for step in gen_a:
            if step["type"] == "complete":
                res_a = step
        end_t = time.perf_counter()
        
        time_a = (end_t - start_t) * 1000.0
        self.stats_a = {
            "name": self.algo_a_name,
            "visited": res_a["visited_count"] if res_a else 0,
            "path_length": res_a["path_length"] if res_a else 0,
            "path_cost": res_a["path_cost"] if res_a else 0,
            "time_ms": time_a,
            "found": res_a["found"] if res_a else False
        }

        # 4. Benchmark Algo B
        start_t = time.perf_counter()
        gen_b = algo_func_b(self.grid_b, allow_diagonals=allow_diagonals)
        res_b = None
        for step in gen_b:
            if step["type"] == "complete":
                res_b = step
        end_t = time.perf_counter()

        time_b = (end_t - start_t) * 1000.0
        self.stats_b = {
            "name": self.algo_b_name,
            "visited": res_b["visited_count"] if res_b else 0,
            "path_length": res_b["path_length"] if res_b else 0,
            "path_cost": res_b["path_cost"] if res_b else 0,
            "time_ms": time_b,
            "found": res_b["found"] if res_b else False
        }

    def _copy_grid_state(self, src_grid, dst_grid):
        for r in range(src_grid.rows):
            for c in range(src_grid.cols):
                src_n = src_grid.grid[r][c]
                dst_n = dst_grid.grid[r][c]
                dst_n.type = src_n.type
                dst_n.weight = src_n.weight
                if src_n.is_start():
                    dst_grid.start_node = dst_n
                elif src_n.is_end():
                    dst_grid.end_node = dst_n

    def draw_modal(self, surface, rect):
        """Renders the comparison report panel."""
        import pygame
        pygame.draw.rect(surface, COLOR_PANEL_BG, rect, border_radius=12)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, rect, width=2, border_radius=12)

        font_title = get_font(size=20, bold=True)
        font_bold = get_font(size=14, bold=True)
        font_reg = get_font(size=13, bold=False)

        # Title Header
        t_surf = font_title.render("Algorithm Benchmark Comparison", True, COLOR_TEXT_BRIGHT)
        surface.blit(t_surf, (rect.x + 30, rect.y + 25))

        col1_x = rect.x + 40
        col2_x = rect.x + 380

        # Draw Side A Summary
        self._draw_algo_card(surface, col1_x, rect.y + 70, 300, 220, self.stats_a, COLOR_PRIMARY)
        
        # Draw Side B Summary
        self._draw_algo_card(surface, col2_x, rect.y + 70, 300, 220, self.stats_b, COLOR_SUCCESS)

        # Winner Analysis
        analysis_y = rect.y + 310
        winner_text = self._compute_winner_summary()
        w_surf = font_bold.render(winner_text, True, COLOR_WARNING)
        surface.blit(w_surf, (rect.x + 40, analysis_y))

    def _draw_algo_card(self, surface, x, y, width, height, stats, accent_color):
        import pygame
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (20, 29, 45), card_rect, border_radius=8)
        pygame.draw.rect(surface, accent_color, card_rect, width=2, border_radius=8)

        font_header = get_font(size=16, bold=True)
        font_reg = get_font(size=13, bold=False)
        font_val = get_font(size=14, bold=True)

        # Header Name
        h_surf = font_header.render(stats["name"], True, accent_color)
        surface.blit(h_surf, (x + 15, y + 15))

        metrics = [
            ("Status:", "Path Found" if stats["found"] else "No Path", COLOR_SUCCESS if stats["found"] else COLOR_DANGER),
            ("Visited Nodes:", f"{stats['visited']}", COLOR_TEXT_BRIGHT),
            ("Path Length:", f"{stats['path_length']} nodes", COLOR_TEXT_BRIGHT),
            ("Path Cost:", f"{stats['path_cost']:.1f}", COLOR_WARNING),
            ("Execution Time:", f"{stats['time_ms']:.2f} ms", COLOR_TEXT_BRIGHT)
        ]

        for i, (label, val, color) in enumerate(metrics):
            ly = y + 50 + i * 30
            l_surf = font_reg.render(label, True, COLOR_TEXT_MUTED)
            v_surf = font_val.render(val, True, color)
            surface.blit(l_surf, (x + 15, ly))
            surface.blit(v_surf, (x + 160, ly))

    def _compute_winner_summary(self):
        if not self.stats_a["found"] or not self.stats_b["found"]:
            return "Benchmark Note: One or both algorithms could not locate a valid path."

        visited_diff = abs(self.stats_a["visited"] - self.stats_b["visited"])
        if self.stats_a["visited"] < self.stats_b["visited"]:
            efficiency = (visited_diff / max(1, self.stats_b["visited"])) * 100
            return f"Summary: {self.stats_a['name']} was more efficient, exploring {efficiency:.1f}% fewer nodes than {self.stats_b['name']}."
        elif self.stats_b["visited"] < self.stats_a["visited"]:
            efficiency = (visited_diff / max(1, self.stats_a["visited"])) * 100
            return f"Summary: {self.stats_b['name']} was more efficient, exploring {efficiency:.1f}% fewer nodes than {self.stats_a['name']}."
        else:
            return "Summary: Both algorithms explored an identical number of grid nodes."
