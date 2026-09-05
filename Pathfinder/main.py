"""
Pathfinding Visualizer Application
Main Entry Point & Event Loop using Pygame.
"""

import sys
import time
import pygame

from ui.theme import (
    WINDOW_WIDTH, WINDOW_HEIGHT, TOP_BAR_HEIGHT, BOTTOM_BAR_HEIGHT,
    GRID_ROWS, GRID_COLS, NODE_SIZE, COLOR_BG_DARK, COLOR_PANEL_BG,
    COLOR_PANEL_BORDER, COLOR_TEXT_BRIGHT, COLOR_TEXT_MUTED, COLOR_PRIMARY,
    COLOR_SUCCESS, COLOR_DANGER, COLOR_WARNING, get_font
)
from grid import Grid, NodeType
from ui.components import Button, Dropdown, Slider, ToggleSwitch, StatsCard
from benchmark import BenchmarkEngine

# Import Pathfinding Algorithms
from algorithms.bfs import solve_bfs
from algorithms.dfs import solve_dfs
from algorithms.dijkstra import solve_dijkstra
from algorithms.astar import solve_astar
from algorithms.greedy import solve_greedy
from algorithms.bidirectional import solve_bidirectional

# Import Maze Generators
from maze.generators import generate_recursive_division, generate_random_maze, generate_prims_maze

ALGO_MAP = {
    "A* Search": solve_astar,
    "Dijkstra's Algorithm": solve_dijkstra,
    "Breadth-First Search (BFS)": solve_bfs,
    "Depth-First Search (DFS)": solve_dfs,
    "Greedy Best-First Search": solve_greedy,
    "Bidirectional BFS": solve_bidirectional
}

MAZE_MAP = {
    "Recursive Division": generate_recursive_division,
    "Random Wall & Weight": generate_random_maze,
    "Prim's Maze": generate_prims_maze
}

class PathfindingApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Interactive Pathfinding Visualizer")
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Calculate Grid Positioning centered in screen
        grid_width = GRID_COLS * NODE_SIZE
        grid_height = GRID_ROWS * NODE_SIZE
        offset_x = (WINDOW_WIDTH - grid_width) // 2
        offset_y = TOP_BAR_HEIGHT + (WINDOW_HEIGHT - TOP_BAR_HEIGHT - BOTTOM_BAR_HEIGHT - grid_height) // 2
        
        self.grid = Grid(GRID_ROWS, GRID_COLS, NODE_SIZE, offset_x, offset_y)
        self.benchmark_engine = BenchmarkEngine(self.grid)

        # Application State
        self.current_tool = "WALL"  # WALL, WEIGHT, START, END, ERASE
        self.is_visualizing = False
        self.is_generating_maze = False
        self.allow_diagonals = False
        self.speed_delay_ms = 10     # Delay between algorithm steps
        
        self.active_generator = None
        self.visualization_start_time = 0
        self.show_benchmark_modal = False
        
        # Dragging state
        self.is_mouse_down = False
        self.drag_node_type = None

        # Build UI Components
        self._setup_ui_components()

    def _setup_ui_components(self):
        # 1. Algorithm Selection Dropdown
        algo_names = list(ALGO_MAP.keys())
        self.algo_dropdown = Dropdown(20, 15, 210, 36, algo_names, default_index=0)

        # 2. Maze Selection Dropdown
        maze_names = list(MAZE_MAP.keys())
        self.maze_dropdown = Dropdown(240, 15, 180, 36, maze_names, default_index=0)

        # 3. Tool Selector Buttons
        self.btn_wall = Button(430, 15, 75, 36, "Wall", callback=lambda: self._set_tool("WALL"))
        self.btn_weight = Button(510, 15, 85, 36, "Weight", callback=lambda: self._set_tool("WEIGHT"))
        self.btn_start = Button(600, 15, 75, 36, "Start", callback=lambda: self._set_tool("START"))
        self.btn_end = Button(680, 15, 75, 36, "End", callback=lambda: self._set_tool("END"))
        self.btn_erase = Button(760, 15, 75, 36, "Erase", callback=lambda: self._set_tool("ERASE"))

        # Highlight default tool
        self.btn_wall.is_active = True

        # 4. Action Buttons
        self.btn_visualize = Button(845, 15, 120, 36, "Visualize", callback=self.start_visualization, bg_color=COLOR_SUCCESS, hover_color=(5, 150, 105))
        self.btn_maze = Button(970, 15, 95, 36, "Build Maze", callback=self.generate_selected_maze, bg_color=COLOR_PRIMARY)
        self.btn_clear_path = Button(1070, 15, 90, 36, "Clear Path", callback=self.clear_path)
        self.btn_reset_grid = Button(1165, 15, 80, 36, "Reset", callback=self.reset_grid, bg_color=COLOR_DANGER, hover_color=(220, 38, 38))

        # 5. Diagonal Toggle & Benchmark Button
        self.toggle_diag = ToggleSwitch(1255, 10, "Diag", default_state=False, on_toggle=self._toggle_diagonal)
        self.btn_benchmark = Button(1255, 35, 90, 26, "Compare", callback=self.toggle_benchmark_modal, bg_color=COLOR_WARNING, hover_color=(217, 119, 6))

        # 6. Speed Control Slider
        self.slider_speed = Slider(20, WINDOW_HEIGHT - 32, 180, 0, 50, self.speed_delay_ms, label="Delay", on_change=self._set_speed)

        # 7. Stats Card HUD
        self.stats_card = StatsCard(220, WINDOW_HEIGHT - BOTTOM_BAR_HEIGHT + 4, WINDOW_WIDTH - 240, BOTTOM_BAR_HEIGHT - 8)

    def _set_tool(self, tool_name):
        self.current_tool = tool_name
        self.btn_wall.is_active = (tool_name == "WALL")
        self.btn_weight.is_active = (tool_name == "WEIGHT")
        self.btn_start.is_active = (tool_name == "START")
        self.btn_end.is_active = (tool_name == "END")
        self.btn_erase.is_active = (tool_name == "ERASE")

    def _toggle_diagonal(self, state):
        self.allow_diagonals = state

    def _set_speed(self, val):
        self.speed_delay_ms = val

    def clear_path(self):
        if self.is_visualizing:
            return
        self.grid.clear_visualization()
        self.stats_card.update_stats("Ready", 0, 0, 0, 0.0)

    def reset_grid(self):
        if self.is_visualizing:
            return
        self.grid.reset_grid()
        self.stats_card.update_stats("Ready", 0, 0, 0, 0.0)

    def start_visualization(self):
        if self.is_visualizing or self.is_generating_maze:
            return

        self.grid.clear_visualization()
        selected_algo_name = self.algo_dropdown.get_selected()
        algo_func = ALGO_MAP[selected_algo_name]

        self.active_generator = algo_func(self.grid, allow_diagonals=self.allow_diagonals)
        self.is_visualizing = True
        self.visualization_start_time = time.perf_counter()
        self.stats_card.update_stats(f"Running {selected_algo_name}...", 0, 0, 0, 0.0)

    def generate_selected_maze(self):
        if self.is_visualizing or self.is_generating_maze:
            return

        selected_maze_name = self.maze_dropdown.get_selected()
        maze_func = MAZE_MAP[selected_maze_name]

        self.active_generator = maze_func(self.grid)
        self.is_generating_maze = True
        self.stats_card.update_stats(f"Generating {selected_maze_name}...", 0, 0, 0, 0.0)

    def toggle_benchmark_modal(self):
        if self.is_visualizing:
            return
        self.show_benchmark_modal = not self.show_benchmark_modal
        if self.show_benchmark_modal:
            algo_a = self.algo_dropdown.get_selected()
            # Pick a different secondary algorithm for instant comparison
            all_algos = list(ALGO_MAP.keys())
            algo_b = "Dijkstra's Algorithm" if algo_a != "Dijkstra's Algorithm" else "A* Search"
            
            self.benchmark_engine.setup_comparison(algo_a, algo_b)
            self.benchmark_engine.run_benchmark(ALGO_MAP[algo_a], ALGO_MAP[algo_b], allow_diagonals=self.allow_diagonals)

    def handle_cell_interaction(self, node, button_event=1):
        if not node or self.is_visualizing or self.is_generating_maze or self.show_benchmark_modal:
            return

        # Right-click always erases
        if button_event == 3 or self.current_tool == "ERASE":
            if not node.is_start() and not node.is_end():
                node.make_empty()
            return

        if self.current_tool == "WALL":
            if not node.is_start() and not node.is_end():
                node.make_wall()
        elif self.current_tool == "WEIGHT":
            if not node.is_start() and not node.is_end():
                node.make_weight()
        elif self.current_tool == "START":
            if not node.is_end() and not node.is_wall():
                self.grid.set_start(node.row, node.col)
        elif self.current_tool == "END":
            if not node.is_start() and not node.is_wall():
                self.grid.set_end(node.row, node.col)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Check Benchmark Modal close click
            if self.show_benchmark_modal:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    modal_rect = pygame.Rect((WINDOW_WIDTH - 720) // 2, (WINDOW_HEIGHT - 380) // 2, 720, 380)
                    if not modal_rect.collidepoint(event.pos):
                        self.show_benchmark_modal = False
                elif event.type == pygame.KEYDOWN and event.key in (pygame.K_ESCAPE, pygame.K_b):
                    self.show_benchmark_modal = False
                continue

            # Pass UI events to dropdowns and buttons first
            if self.algo_dropdown.handle_event(event):
                continue
            if self.maze_dropdown.handle_event(event):
                continue
            if self.slider_speed.handle_event(event):
                continue
            if self.toggle_diag.handle_event(event):
                continue

            # Toolbar Buttons
            if (self.btn_wall.handle_event(event) or self.btn_weight.handle_event(event) or
                self.btn_start.handle_event(event) or self.btn_end.handle_event(event) or
                self.btn_erase.handle_event(event) or self.btn_visualize.handle_event(event) or
                self.btn_maze.handle_event(event) or self.btn_clear_path.handle_event(event) or
                self.btn_reset_grid.handle_event(event) or self.btn_benchmark.handle_event(event)):
                continue

            # Keyboard Shortcuts
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.start_visualization()
                elif event.key == pygame.K_c:
                    self.clear_path()
                elif event.key == pygame.K_r:
                    self.reset_grid()
                elif event.key == pygame.K_m:
                    self.generate_selected_maze()
                elif event.key == pygame.K_d:
                    self.allow_diagonals = not self.allow_diagonals
                    self.toggle_diag.state = self.allow_diagonals
                elif event.key == pygame.K_b:
                    self.toggle_benchmark_modal()

            # Mouse Grid Painting & Dragging
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    self.is_mouse_down = True
                    node = self.grid.get_node_at_pixel(*event.pos)
                    if node:
                        self.handle_cell_interaction(node, button_event=event.button)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):
                    self.is_mouse_down = False

            elif event.type == pygame.MOUSEMOTION and self.is_mouse_down:
                node = self.grid.get_node_at_pixel(*event.pos)
                if node:
                    self.handle_cell_interaction(node)

        return True

    def update_generator(self):
        """Advances active algorithm generator or maze generator frame by frame."""
        if not self.active_generator:
            return

        try:
            step = next(self.active_generator)
            step_type = step.get("type")

            if step_type == "visit":
                elapsed = (time.perf_counter() - self.visualization_start_time) * 1000.0
                self.stats_card.update_stats(
                    f"Exploring...",
                    visited=step.get("visited_count", 0),
                    path_len=0,
                    cost=0,
                    exec_time=elapsed
                )

            elif step_type == "path":
                elapsed = (time.perf_counter() - self.visualization_start_time) * 1000.0
                self.stats_card.update_stats(
                    "Reconstructing Path...",
                    visited=step.get("visited_count", 0),
                    path_len=step.get("path_length", 0),
                    cost=step.get("path_cost", 0),
                    exec_time=elapsed
                )

            elif step_type == "complete":
                elapsed = (time.perf_counter() - self.visualization_start_time) * 1000.0
                status_str = "Path Found!" if step.get("found") else "No Path Found!"
                self.stats_card.update_stats(
                    status_str,
                    visited=step.get("visited_count", 0),
                    path_len=step.get("path_length", 0),
                    cost=step.get("path_cost", 0),
                    exec_time=elapsed
                )
                self.is_visualizing = False
                self.is_generating_maze = False
                self.active_generator = None

        except StopIteration:
            self.is_visualizing = False
            self.is_generating_maze = False
            self.active_generator = None

    def draw(self):
        self.screen.fill(COLOR_BG_DARK)

        # Draw Main Grid
        self.grid.draw(self.screen)

        # Draw Top Control Panel Bar
        top_bar_rect = pygame.Rect(0, 0, WINDOW_WIDTH, TOP_BAR_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, top_bar_rect)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, top_bar_rect, width=1)

        # Render Tool Palette Labels
        font_sub = get_font(size=11, bold=True)
        lbl_tools = font_sub.render("DRAWING TOOLS", True, COLOR_TEXT_MUTED)
        lbl_actions = font_sub.render("ACTIONS", True, COLOR_TEXT_MUTED)
        self.screen.blit(lbl_tools, (430, 2))
        self.screen.blit(lbl_actions, (845, 2))

        # Draw UI Buttons & Toggles
        self.btn_wall.draw(self.screen)
        self.btn_weight.draw(self.screen)
        self.btn_start.draw(self.screen)
        self.btn_end.draw(self.screen)
        self.btn_erase.draw(self.screen)

        self.btn_visualize.draw(self.screen)
        self.btn_maze.draw(self.screen)
        self.btn_clear_path.draw(self.screen)
        self.btn_reset_grid.draw(self.screen)
        self.btn_benchmark.draw(self.screen)

        self.toggle_diag.draw(self.screen)

        # Draw Bottom Bar Panel
        bottom_bar_rect = pygame.Rect(0, WINDOW_HEIGHT - BOTTOM_BAR_HEIGHT, WINDOW_WIDTH, BOTTOM_BAR_HEIGHT)
        pygame.draw.rect(self.screen, COLOR_PANEL_BG, bottom_bar_rect)
        pygame.draw.rect(self.screen, COLOR_PANEL_BORDER, bottom_bar_rect, width=1)

        self.slider_speed.draw(self.screen)
        self.stats_card.draw(self.screen)

        # Render Dropdowns on top of bar to ensure open popups overlay grid
        self.algo_dropdown.draw(self.screen)
        self.maze_dropdown.draw(self.screen)

        # Draw Benchmark Modal Overlay if open
        if self.show_benchmark_modal:
            modal_rect = pygame.Rect((WINDOW_WIDTH - 720) // 2, (WINDOW_HEIGHT - 380) // 2, 720, 380)
            self.benchmark_engine.draw_modal(self.screen, modal_rect)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            
            if self.is_visualizing or self.is_generating_maze:
                self.update_generator()
                if self.speed_delay_ms > 0:
                    pygame.time.delay(self.speed_delay_ms)

            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = PathfindingApp()
    app.run()
