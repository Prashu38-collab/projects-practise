import sys

import numpy as np

import pygame

SAMPLE_RATE = 44100
DURATION = 0.5
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400
FPS = 60

WHITE, BLACK, GRAY, ACTIVE = (
    255, 255, 255), (0, 0, 0), (200, 200, 200), (100, 150, 255)

NOTES = {
    'C4': 261.63, 'C#4': 277.18, 'D4': 293.66, 'D#4': 311.13, 'E4': 329.63,
    'F4': 349.23, 'F#4': 369.99, 'G4': 392.00, 'G#4': 415.30, 'A4': 440.00,
    'A#4': 466.16, 'B4': 493.88, 'C5': 523.25, 'C#5': 554.37, 'D5': 587.33,
    'D#5': 622.25, 'E5': 659.25
}

KEY_MAP = {
    pygame.K_a: 'C4', pygame.K_w: 'C#4', pygame.K_s: 'D4', pygame.K_e: 'D#4',
    pygame.K_d: 'E4', pygame.K_f: 'F4', pygame.K_t: 'F#4', pygame.K_g: 'G4',
    pygame.K_y: 'G#4', pygame.K_h: 'A4', pygame.K_u: 'A#4', pygame.K_j: 'B4',
    pygame.K_k: 'C5', pygame.K_o: 'C#5', pygame.K_l: 'D5', pygame.K_p: 'D#5',
    pygame.K_SEMICOLON: 'E5'
}

KEY_LAYOUT = [
    ('C4', 'white'), ('C#4', 'black'), ('D4',
                                        'white'), ('D#4', 'black'), ('E4', 'white'),
    ('F4', 'white'), ('F#4', 'black'), ('G4',
                                        'white'), ('G#4', 'black'), ('A4', 'white'),
    ('A#4', 'black'), ('B4', 'white'), ('C5',
                                        'white'), ('C#5', 'black'), ('D5', 'white'),
    ('D#5', 'black'), ('E5', 'white')
]


class AudioEngine:
    def __init__(self):

        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=2)
        self.sounds = {note: self._gen_sound(
            freq) for note, freq in NOTES.items()}

    def _gen_sound(self, freq):
        t = np.linspace(0, DURATION, int(SAMPLE_RATE * DURATION), False)
        # Generate mono wave first
        mono_wave = np.sin(freq * t * 2 * np.pi)

        # Convert to 16-bit integer
        mono_int = np.int16(mono_wave * 32767)

        # Stack mono channel twice to create stereo (2D array: [samples, 2])
        stereo_wave = np.column_stack((mono_int, mono_int))

        return pygame.sndarray.make_sound(stereo_wave)

    def play(self, note):
        if note in self.sounds:
            self.sounds[note].play(fade_ms=50)


class PianoUI:
    def __init__(self, screen):
        self.screen = screen
        self.rects = {}
        self._build_layout()

    def _build_layout(self):
        w_count = sum(1 for _, t in KEY_LAYOUT if t == 'white')
        w_width = SCREEN_WIDTH / w_count
        w_height = SCREEN_HEIGHT - 50
        b_width = w_width * 0.6
        b_height = w_height * 0.6
        w_idx = 0

        for note, ktype in KEY_LAYOUT:
            if ktype == 'white':
                x = w_idx * w_width
                w_idx += 1
            else:
                x = (w_idx * w_width) - (b_width / 2)

            width = b_width if ktype == 'black' else w_width
            height = b_height if ktype == 'black' else w_height
            self.rects[note] = pygame.Rect(x, 50, width, height)

    def draw(self, active_notes):
        self.screen.fill(GRAY)

        font = pygame.font.SysFont('Arial', 24)
        self.screen.blit(font.render(
            "Keyboard (A-L) or Mouse", True, BLACK), (10, 10))

        for note, ktype in KEY_LAYOUT:
            rect = self.rects[note]
            is_active = note in active_notes

            if ktype == 'white':
                pygame.draw.rect(
                    self.screen, ACTIVE if is_active else WHITE, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 2)
                if not is_active:
                    lbl = pygame.font.SysFont(
                        'Arial', 12).render(note, True, BLACK)
                    self.screen.blit(lbl, lbl.get_rect(
                        center=(rect.centerx, rect.bottom - 15)))
            else:
                pygame.draw.rect(
                    self.screen, ACTIVE if is_active else BLACK, rect)
                pygame.draw.rect(
                    self.screen, WHITE if is_active else BLACK, rect, 2)


class PianoApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Modular PyGame Piano")
        self.clock = pygame.time.Clock()

        self.audio = AudioEngine()
        self.ui = PianoUI(self.screen)
        self.active_notes = set()

    def _handle_keyboard(self, event):
        if event.type == pygame.KEYDOWN and event.key in KEY_MAP:
            note = KEY_MAP[event.key]
            if note not in self.active_notes:
                self.active_notes.add(note)
                self.audio.play(note)
        elif event.type == pygame.KEYUP and event.key in KEY_MAP:
            self.active_notes.discard(KEY_MAP[event.key])

    def _handle_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            clicked_note = None
            for note, ktype in KEY_LAYOUT:
                if self.ui.rects[note].collidepoint(pos):
                    if ktype == 'black':
                        clicked_note = note
                        break
                    elif clicked_note is None:
                        clicked_note = note

            if clicked_note and clicked_note not in self.active_notes:
                self.active_notes.add(clicked_note)
                self.audio.play(clicked_note)

        elif event.type == pygame.MOUSEBUTTONUP:
            self.active_notes.clear()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self._handle_keyboard(event)
                    self._handle_mouse(event)

            self.ui.draw(self.active_notes)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    PianoApp().run()
