"""
Grid and Node data structures for Pathfinding Visualizer.
Manages grid state, cell types, neighbor logic, and rendering.
"""

import math
import pygame
from ui.theme import (
    COLOR_EMPTY, COLOR_WALL, COLOR_WEIGHT, COLOR_START, COLOR_END,
    COLOR_VISITED_1, COLOR_VISITED_2, COLOR_VISITED_BIDIR_1, COLOR_VISITED_BIDIR_2,
    COLOR_PATH, COLOR_PATH_BORDER, COLOR_GRID_LINE, COST_NORMAL, COST_WEIGHT,
    COST_DIAGONAL_NORMAL, COST_DIAGONAL_WEIGHT, get_font
)

class NodeType:
    EMPTY = 0
    START = 1
    END = 2
    WALL = 3
    WEIGHT = 4

class NodeState:
    UNVISITED = 0
    VISITING = 1
    VISITED = 2
    VISITED_B = 3   # For bidirectional search from target
    PATH = 4

class Node:
    def __init__(self, row, col, size, offset_x=0, offset_y=0):
        self.row = row
        self.col = col
        self.size = size
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.x = offset_x + col * size
        self.y = offset_y + row * size
        
        self.type = NodeType.EMPTY
        self.state = NodeState.UNVISITED
        self.weight = COST_NORMAL
        self.parent = None
        
        # Pathfinding distance metrics
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.h_score = float('inf')

    def is_start(self):
        return self.type == NodeType.START

    def is_end(self):
        return self.type == NodeType.END

    def is_wall(self):
        return self.type == NodeType.WALL

    def is_weight(self):
        return self.type == NodeType.WEIGHT

    def make_empty(self):
        self.type = NodeType.EMPTY
        self.weight = COST_NORMAL

    def make_start(self):
        self.type = NodeType.START
        self.weight = COST_NORMAL

    def make_end(self):
        self.type = NodeType.END
        self.weight = COST_NORMAL

    def make_wall(self):
        self.type = NodeType.WALL
        self.weight = COST_NORMAL

    def make_weight(self):
        self.type = NodeType.WEIGHT
        self.weight = COST_WEIGHT

    def reset_pathfinding(self):
        self.state = NodeState.UNVISITED
        self.parent = None
        self.g_score = float('inf')
        self.f_score = float('inf')
        self.h_score = float('inf')

    def draw(self, surface):
        rect = (self.x, self.y, self.size, self.size)
        
        # Determine background fill color based on type and state
        if self.type == NodeType.START:
            color = COLOR_START
        elif self.type == NodeType.END:
            color = COLOR_END
        elif self.type == NodeType.WALL:
            color = COLOR_WALL
        elif self.state == NodeState.PATH:
            color = COLOR_PATH
        elif self.state == NodeState.VISITED_B:
            color = COLOR_VISITED_BIDIR_1
        elif self.state == NodeState.VISITED:
            color = COLOR_VISITED_1
        elif self.state == NodeState.VISITING:
            color = COLOR_VISITED_2
        elif self.type == NodeType.WEIGHT:
            color = COLOR_WEIGHT
        else:
            color = COLOR_EMPTY

        # Draw cell background
        pygame.draw.rect(surface, color, rect, border_radius=3)
        
        # Grid line border
        pygame.draw.rect(surface, COLOR_GRID_LINE, rect, width=1, border_radius=3)

        # Draw custom visual indicators for special nodes
        if self.type == NodeType.START:
            # Draw start arrow / circle icon
            center = (self.x + self.size // 2, self.y + self.size // 2)
            pygame.draw.circle(surface, (255, 255, 255), center, self.size // 4)
        elif self.type == NodeType.END:
            # Draw target icon
            center = (self.x + self.size // 2, self.y + self.size // 2)
            pygame.draw.circle(surface, (255, 255, 255), center, self.size // 3, width=2)
            pygame.draw.circle(surface, (255, 255, 255), center, self.size // 6)
        elif self.type == NodeType.WEIGHT:
            # Draw weight symbol '5' or weight icon
            font = get_font(size=12, bold=True)
            text_surf = font.render("5", True, (15, 23, 42))
            text_rect = text_surf.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
            surface.blit(text_surf, text_rect)


class Grid:
    def __init__(self, rows, cols, node_size, offset_x=0, offset_y=0):
        self.rows = rows
        self.cols = cols
        self.node_size = node_size
        self.offset_x = offset_x
        self.offset_y = offset_y
        
        self.grid = []
        self.start_node = None
        self.end_node = None
        
        self._build_grid()

    def _build_grid(self):
        self.grid = []
        for r in range(self.rows):
            row_nodes = []
            for c in range(self.cols):
                node = Node(r, c, self.node_size, self.offset_x, self.offset_y)
                row_nodes.append(node)
            self.grid.append(row_nodes)

        # Default start and end positions
        default_start_r, default_start_c = self.rows // 2, max(2, self.cols // 6)
        default_end_r, default_end_c = self.rows // 2, min(self.cols - 3, (5 * self.cols) // 6)
        
        self.set_start(default_start_r, default_start_c)
        self.set_end(default_end_r, default_end_c)

    def set_start(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if self.start_node:
                self.start_node.make_empty()
            self.start_node = self.grid[r][c]
            self.start_node.make_start()

    def set_end(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            if self.end_node:
                self.end_node.make_empty()
            self.end_node = self.grid[r][c]
            self.end_node.make_end()

    def get_node(self, r, c):
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c]
        return None

    def get_node_at_pixel(self, x, y):
        col = (x - self.offset_x) // self.node_size
        row = (y - self.offset_y) // self.node_size
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    def get_neighbors(self, node, allow_diagonals=False):
        neighbors = []
        r, c = node.row, node.col

        # 4 Orthogonal directions (Up, Right, Down, Left)
        directions = [
            (-1, 0, COST_NORMAL),  # Up
            (0, 1, COST_NORMAL),   # Right
            (1, 0, COST_NORMAL),   # Down
            (0, -1, COST_NORMAL)   # Left
        ]

        for dr, dc, base_cost in directions:
            nr, nc = r + dr, c + dc
            neighbor = self.get_node(nr, nc)
            if neighbor and not neighbor.is_wall():
                neighbors.append((neighbor, neighbor.weight * base_cost))

        # 8 Diagonal directions if enabled
        if allow_diagonals:
            diag_directions = [
                (-1, -1), # Up-Left
                (-1, 1),  # Up-Right
                (1, -1),  # Down-Left
                (1, 1)    # Down-Right
            ]
            for dr, dc in diag_directions:
                nr, nc = r + dr, c + dc
                neighbor = self.get_node(nr, nc)
                if neighbor and not neighbor.is_wall():
                    # Corner-cutting check: don't move diagonally if both adjacent orthogonals are walls
                    adj1 = self.get_node(r + dr, c)
                    adj2 = self.get_node(r, c + dc)
                    
                    wall1 = adj1.is_wall() if adj1 else False
                    wall2 = adj2.is_wall() if adj2 else False
                    
                    if not (wall1 and wall2):
                        move_cost = COST_DIAGONAL_WEIGHT if neighbor.is_weight() else COST_DIAGONAL_NORMAL
                        neighbors.append((neighbor, move_cost))

        return neighbors

    def clear_visualization(self):
        """Clears visited states and paths while keeping walls and weights intact."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c].reset_pathfinding()

    def reset_grid(self):
        """Clears everything including walls and weights."""
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c].make_empty()
                self.grid[r][c].reset_pathfinding()
        
        # Restore Start and End
        self.set_start(self.rows // 2, max(2, self.cols // 6))
        self.set_end(self.rows // 2, min(self.cols - 3, (5 * self.cols) // 6))

    def draw(self, surface):
        for r in range(self.rows):
            for c in range(self.cols):
                self.grid[r][c].draw(surface)
