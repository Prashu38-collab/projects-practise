"""
Interactive Custom UI Components for Pygame.
Includes Button, Dropdown, Slider, ToggleSwitch, and StatsCard.
"""

import pygame
from ui.theme import (
    COLOR_PANEL_BG, COLOR_PANEL_BORDER, COLOR_PRIMARY, COLOR_PRIMARY_HOVER,
    COLOR_TEXT_BRIGHT, COLOR_TEXT_MUTED, COLOR_SUCCESS, COLOR_DANGER,
    COLOR_WARNING, get_font
)

class Button:
    def __init__(self, x, y, width, height, text, callback=None, bg_color=COLOR_PANEL_BG, hover_color=COLOR_PRIMARY, icon=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.callback = callback
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = False
        self.is_active = False
        self.icon = icon

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        return False

    def draw(self, surface):
        if self.is_active:
            color = self.hover_color
        elif self.is_hovered:
            # Interpolate towards hover color
            color = self.hover_color
        else:
            color = self.bg_color

        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, self.rect, width=1, border_radius=6)

        font = get_font(size=14, bold=True)
        text_surf = font.render(self.text, True, COLOR_TEXT_BRIGHT)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class Dropdown:
    def __init__(self, x, y, width, height, options, default_index=0, on_select=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_index = default_index
        self.on_select = on_select
        self.is_open = False
        self.hovered_option = -1

    def get_selected(self):
        return self.options[self.selected_index]

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.is_open:
                mouse_x, mouse_y = event.pos
                for i, opt in enumerate(self.options):
                    opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                    if opt_rect.collidepoint(mouse_x, mouse_y):
                        self.hovered_option = i
                        break
                else:
                    self.hovered_option = -1

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.rect.collidepoint(pos):
                self.is_open = not self.is_open
                return True
            elif self.is_open:
                for i, opt in enumerate(self.options):
                    opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                    if opt_rect.collidepoint(pos):
                        self.selected_index = i
                        self.is_open = False
                        if self.on_select:
                            self.on_select(i, self.options[i])
                        return True
                self.is_open = False
        return False

    def draw(self, surface):
        # Draw Main Box
        color = COLOR_PRIMARY if self.is_open else COLOR_PANEL_BG
        pygame.draw.rect(surface, color, self.rect, border_radius=6)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, self.rect, width=1, border_radius=6)

        font = get_font(size=13, bold=True)
        text_surf = font.render(self.options[self.selected_index], True, COLOR_TEXT_BRIGHT)
        surface.blit(text_surf, (self.rect.x + 12, self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

        # Arrow indicator
        arrow_color = COLOR_TEXT_BRIGHT
        arrow_x = self.rect.right - 15
        arrow_y = self.rect.centery
        if self.is_open:
            pygame.draw.polygon(surface, arrow_color, [(arrow_x - 4, arrow_y + 3), (arrow_x + 4, arrow_y + 3), (arrow_x, arrow_y - 3)])
        else:
            pygame.draw.polygon(surface, arrow_color, [(arrow_x - 4, arrow_y - 3), (arrow_x + 4, arrow_y - 3), (arrow_x, arrow_y + 3)])

        # Draw Open Menu Overlay
        if self.is_open:
            for i, opt in enumerate(self.options):
                opt_rect = pygame.Rect(self.rect.x, self.rect.y + (i + 1) * self.rect.height, self.rect.width, self.rect.height)
                bg_col = COLOR_PRIMARY_HOVER if i == self.hovered_option else COLOR_PANEL_BG
                pygame.draw.rect(surface, bg_col, opt_rect)
                pygame.draw.rect(surface, COLOR_PANEL_BORDER, opt_rect, width=1)

                opt_surf = font.render(opt, True, COLOR_TEXT_BRIGHT)
                surface.blit(opt_surf, (opt_rect.x + 12, opt_rect.y + (opt_rect.height - opt_surf.get_height()) // 2))


class Slider:
    def __init__(self, x, y, width, min_val, max_val, default_val, label="Speed", on_change=None):
        self.rect = pygame.Rect(x, y, width, 10)
        self.min_val = min_val
        self.max_val = max_val
        self.val = default_val
        self.label = label
        self.on_change = on_change
        self.is_dragging = False

        self.handle_radius = 8
        self._update_handle_pos()

    def _update_handle_pos(self):
        ratio = (self.val - self.min_val) / (self.max_val - self.min_val)
        self.handle_x = self.rect.x + ratio * self.rect.width

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            handle_rect = pygame.Rect(self.handle_x - self.handle_radius, self.rect.centery - self.handle_radius, self.handle_radius * 2, self.handle_radius * 2)
            if handle_rect.collidepoint(mouse_x, mouse_y) or self.rect.collidepoint(mouse_x, mouse_y):
                self.is_dragging = True
                self._update_val_from_mouse(mouse_x)
                return True

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                return True

        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self._update_val_from_mouse(event.pos[0])
            return True

        return False

    def _update_val_from_mouse(self, mouse_x):
        rel_x = max(0, min(self.rect.width, mouse_x - self.rect.x))
        ratio = rel_x / self.rect.width
        self.val = int(self.min_val + ratio * (self.max_val - self.min_val))
        self._update_handle_pos()
        if self.on_change:
            self.on_change(self.val)

    def draw(self, surface):
        font = get_font(size=12, bold=True)
        lbl_surf = font.render(f"{self.label}: {self.val} ms", True, COLOR_TEXT_MUTED)
        surface.blit(lbl_surf, (self.rect.x, self.rect.y - 18))

        # Track background
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, self.rect, border_radius=5)
        # Active track fill
        active_rect = pygame.Rect(self.rect.x, self.rect.y, self.handle_x - self.rect.x, self.rect.height)
        pygame.draw.rect(surface, COLOR_PRIMARY, active_rect, border_radius=5)
        # Handle knob
        pygame.draw.circle(surface, COLOR_TEXT_BRIGHT, (int(self.handle_x), self.rect.centery), self.handle_radius)


class ToggleSwitch:
    def __init__(self, x, y, label, default_state=False, on_toggle=None):
        self.x = x
        self.y = y
        self.width = 44
        self.height = 22
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.label = label
        self.state = default_state
        self.on_toggle = on_toggle

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.state = not self.state
                if self.on_toggle:
                    self.on_toggle(self.state)
                return True
        return False

    def draw(self, surface):
        font = get_font(size=12, bold=True)
        lbl_surf = font.render(self.label, True, COLOR_TEXT_BRIGHT)
        surface.blit(lbl_surf, (self.x + self.width + 10, self.y + 2))

        bg_color = COLOR_SUCCESS if self.state else COLOR_PANEL_BORDER
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=11)

        knob_x = self.x + self.width - 11 if self.state else self.x + 11
        pygame.draw.circle(surface, COLOR_TEXT_BRIGHT, (knob_x, self.y + 11), 8)


class StatsCard:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.status = "Ready"
        self.visited_nodes = 0
        self.path_length = 0
        self.path_cost = 0
        self.exec_time = 0.0

    def update_stats(self, status="Ready", visited=0, path_len=0, cost=0, exec_time=0.0):
        self.status = status
        self.visited_nodes = visited
        self.path_length = path_len
        self.path_cost = cost
        self.exec_time = exec_time

    def draw(self, surface):
        pygame.draw.rect(surface, COLOR_PANEL_BG, self.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_PANEL_BORDER, self.rect, width=1, border_radius=8)

        font_bold = get_font(size=13, bold=True)
        font_regular = get_font(size=12, bold=False)

        items = [
            ("Status:", self.status, COLOR_PRIMARY if self.status != "Path Found!" else COLOR_SUCCESS),
            ("Visited Nodes:", f"{self.visited_nodes}", COLOR_TEXT_BRIGHT),
            ("Path Length:", f"{self.path_length} nodes", COLOR_TEXT_BRIGHT),
            ("Path Cost:", f"{self.path_cost:.1f}", COLOR_WARNING),
            ("Exec Time:", f"{self.exec_time:.2f} ms", COLOR_TEXT_BRIGHT)
        ]

        start_x = self.rect.x + 15
        for i, (label, val, color) in enumerate(items):
            item_x = start_x + i * 230
            lbl_surf = font_regular.render(label, True, COLOR_TEXT_MUTED)
            val_surf = font_bold.render(val, True, color)
            surface.blit(lbl_surf, (item_x, self.rect.y + 8))
            surface.blit(val_surf, (item_x, self.rect.y + 24))
