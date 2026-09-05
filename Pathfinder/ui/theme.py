"""
Theme definitions, color constants, dimensions, and typography settings for Pathfinding Visualizer.
"""

import pygame

# Initialize font module for Pygame
pygame.font.init()

# Color Palette (Modern Dark Theme)
COLOR_BG_DARK = (15, 23, 42)         # #0F172A Deep Slate
COLOR_PANEL_BG = (30, 41, 59)        # #1E293B Panel Background
COLOR_PANEL_BORDER = (51, 65, 85)    # #334155 Border Accent
COLOR_GRID_BG = (10, 15, 26)         # #0A0F1A Grid Background
COLOR_GRID_LINE = (30, 41, 59, 100)   # Grid line color

# Node Colors
COLOR_EMPTY = (15, 23, 42)
COLOR_WALL = (51, 65, 85)            # Slate wall
COLOR_WEIGHT = (245, 158, 11)        # Amber swamp weight
COLOR_START = (16, 185, 129)         # Emerald Green
COLOR_END = (239, 68, 68)            # Rose Red

# Animation States
COLOR_VISITED_1 = (6, 182, 212)      # Cyan
COLOR_VISITED_2 = (59, 130, 246)     # Royal Blue
COLOR_VISITED_BIDIR_1 = (236, 72, 153)# Hot Pink (for 2nd frontier)
COLOR_VISITED_BIDIR_2 = (139, 92, 246)# Violet

COLOR_PATH = (250, 204, 21)          # Glowing Amber/Gold
COLOR_PATH_BORDER = (234, 179, 8)

# Text & UI Colors
COLOR_TEXT_BRIGHT = (248, 250, 252)
COLOR_TEXT_MUTED = (148, 163, 184)
COLOR_PRIMARY = (99, 102, 241)        # Indigo Accent
COLOR_PRIMARY_HOVER = (129, 140, 248)
COLOR_SUCCESS = (16, 185, 129)
COLOR_DANGER = (239, 68, 68)
COLOR_WARNING = (245, 158, 11)

# Window Layout
WINDOW_WIDTH = 1360
WINDOW_HEIGHT = 860

TOP_BAR_HEIGHT = 70
SIDEBAR_WIDTH = 300
BOTTOM_BAR_HEIGHT = 45

# Grid Dimensions
GRID_ROWS = 32
GRID_COLS = 45
NODE_SIZE = 22

# Weight Costs
COST_NORMAL = 1
COST_WEIGHT = 5
COST_DIAGONAL_NORMAL = 1.414
COST_DIAGONAL_WEIGHT = 7.07

# Fonts
def get_font(size=14, bold=False):
    try:
        return pygame.font.SysFont("Helvetica Neue, Arial, sans-serif", size, bold=bold)
    except Exception:
        return pygame.font.Font(None, size)
