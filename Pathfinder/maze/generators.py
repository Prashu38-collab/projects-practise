"""
Maze Generation Algorithms
Includes Recursive Division, Random Walls & Weights, and Prim's Maze.
"""

import random

def generate_random_maze(grid, wall_density=0.25, weight_density=0.15):
    """Randomly places walls and weights across the grid."""
    grid.clear_visualization()
    
    for r in range(grid.rows):
        for c in range(grid.cols):
            node = grid.grid[r][c]
            if node.is_start() or node.is_end():
                continue
                
            rand_val = random.random()
            if rand_val < wall_density:
                node.make_wall()
                yield {"type": "maze_step", "node": node}
            elif rand_val < wall_density + weight_density:
                node.make_weight()
                yield {"type": "maze_step", "node": node}
            else:
                node.make_empty()

def generate_recursive_division(grid):
    """Generates a structured maze using Recursive Division algorithm."""
    grid.clear_visualization()
    
    # First, build outer border walls if desired or clear
    for r in range(grid.rows):
        for c in range(grid.cols):
            node = grid.grid[r][c]
            if not node.is_start() and not node.is_end():
                node.make_empty()

    def divide(row_start, row_end, col_start, col_end):
        height = row_end - row_start
        width = col_end - col_start

        if height < 3 or width < 3:
            return

        # Choose division orientation (horizontal vs vertical)
        horizontal = (height > width) if height != width else (random.random() < 0.5)

        if horizontal:
            # Pick a wall row (must be odd index to align walls)
            possible_rows = [r for r in range(row_start + 1, row_end) if r % 2 == 0]
            if not possible_rows:
                return
            wall_r = random.choice(possible_rows)

            # Pick a passage column gap
            possible_cols = [c for c in range(col_start, col_end + 1) if c % 2 != 0]
            gap_c = random.choice(possible_cols) if possible_cols else col_start

            for c in range(col_start, col_end + 1):
                if c != gap_c:
                    node = grid.grid[wall_r][c]
                    if not node.is_start() and not node.is_end():
                        node.make_wall()
                        yield node

            yield from divide(row_start, wall_r - 1, col_start, col_end)
            yield from divide(wall_r + 1, row_end, col_start, col_end)

        else:
            # Pick a wall column (even index)
            possible_cols = [c for c in range(col_start + 1, col_end) if c % 2 == 0]
            if not possible_cols:
                return
            wall_c = random.choice(possible_cols)

            # Pick a passage row gap
            possible_rows = [r for r in range(row_start, row_end + 1) if r % 2 != 0]
            gap_r = random.choice(possible_rows) if possible_rows else row_start

            for r in range(row_start, row_end + 1):
                if r != gap_r:
                    node = grid.grid[r][wall_c]
                    if not node.is_start() and not node.is_end():
                        node.make_wall()
                        yield node

            yield from divide(row_start, row_end, col_start, wall_c - 1)
            yield from divide(row_start, row_end, wall_c + 1, col_end)

    for wall_node in divide(0, grid.rows - 1, 0, grid.cols - 1):
        yield {"type": "maze_step", "node": wall_node}


def generate_prims_maze(grid):
    """Generates a perfect maze using Randomized Prim's Algorithm."""
    grid.clear_visualization()

    # Step 1: Fill entire grid with walls except start and end
    for r in range(grid.rows):
        for c in range(grid.cols):
            node = grid.grid[r][c]
            if not node.is_start() and not node.is_end():
                node.make_wall()

    # Frontiers list
    start_r, start_c = grid.start_node.row, grid.start_node.col
    walls = []

    def add_walls(r, c):
        for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid.rows and 0 <= nc < grid.cols:
                if grid.grid[nr][nc].is_wall():
                    walls.append((nr, nc, r, c))

    add_walls(start_r, start_c)

    while walls:
        idx = random.randint(0, len(walls) - 1)
        nr, nc, pr, pc = walls.pop(idx)

        node = grid.grid[nr][nc]
        if node.is_wall():
            node.make_empty()
            yield {"type": "maze_step", "node": node}

            # Connect with parent passage cell
            mr, mc = (nr + pr) // 2, (nc + pc) // 2
            mid_node = grid.grid[mr][mc]
            if not mid_node.is_start() and not mid_node.is_end():
                mid_node.make_empty()
                yield {"type": "maze_step", "node": mid_node}

            add_walls(nr, nc)
