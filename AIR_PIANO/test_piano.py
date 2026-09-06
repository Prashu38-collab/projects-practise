import numpy as np
import pygame

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

# SCREEN
WIDTH = 1200
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Air Piano")

clock = pygame.time.Clock()

# PIANO SETTINGS
WHITE_KEY_COUNT = 36

KEY_WIDTH = WIDTH / WHITE_KEY_COUNT
KEY_HEIGHT = 150
KEY_Y = 200

BLACK_KEY_WIDTH = KEY_WIDTH * 0.6
BLACK_KEY_HEIGHT = KEY_HEIGHT * 0.6

# NOTE INFORMATION
NOTE_NAMES = [
    "C", "C#", "D", "D#", "E",
    "F", "F#", "G", "G#", "A", "A#", "B"
]

# Generate 61 notes: C2 -> C7
notes = []
for octave in range(2, 7):
    for note in NOTE_NAMES:
        notes.append(note + str(octave))
notes.append("C7")

# MIDI MAPPING
# C2 = MIDI 36
note_to_midi = {}
for i, note in enumerate(notes):
    note_to_midi[note] = 36 + i

# AUDIO ENGINE
class SoundEngine:

    def __init__(self):
        self.sample_rate = 44100
        self.duration = 1.0
        self.sounds = {}
        self.generate_all_notes()

    def get_frequency(self, midi_note):
        """Convert MIDI note number to frequency. A4 = MIDI 69 = 440 Hz"""
        return 440 * (2 ** ((midi_note - 69) / 12))

    def generate_sine_wave(self, frequency):
        t = np.linspace(
            0,
            self.duration,
            int(self.sample_rate * self.duration),
            False
        )
        wave = np.sin(frequency * t * 2 * np.pi)
        audio = np.int16(wave * 32767)

        # Convert mono -> stereo
        stereo_audio = np.column_stack((audio, audio))
        return pygame.sndarray.make_sound(stereo_audio)

    def generate_all_notes(self):
        for note, midi in note_to_midi.items():
            frequency = self.get_frequency(midi)
            self.sounds[midi] = self.generate_sine_wave(frequency)

    def play_note(self, midi_note):
        if midi_note in self.sounds:
            self.sounds[midi_note].play()

sound_engine = SoundEngine()

# KEY RECTANGLES
white_keys = []
black_keys = []

# White Keys
for i in range(WHITE_KEY_COUNT):
    x = i * KEY_WIDTH
    rect = pygame.Rect(x, KEY_Y, KEY_WIDTH, KEY_HEIGHT)
    white_keys.append({
        "rect": rect,
        "note": notes[i],
        "midi": note_to_midi[notes[i]]
    })

# Black Keys
# Black key appears after these white-key positions
BLACK_AFTER_WHITE = [0, 1, 3, 4, 5]
black_index = 0

for i in range(WHITE_KEY_COUNT - 1):
    if i % 7 in BLACK_AFTER_WHITE:
        black_x = (i + 1) * KEY_WIDTH - BLACK_KEY_WIDTH / 2
        rect = pygame.Rect(black_x, KEY_Y, BLACK_KEY_WIDTH, BLACK_KEY_HEIGHT)

        # Find the MIDI note directly
        white_midi = white_keys[i]["midi"]
        black_midi = white_midi + 1

        # Find its note name
        black_note = notes[notes.index(white_keys[i]["note"]) + 1]

        black_keys.append({
            "rect": rect,
            "note": black_note,
            "midi": black_midi
        })
        black_index += 1

pressed_note = None

# MAIN LOOP
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            key_found = False

            # Check Black Keys First
            for key in black_keys:
                if key["rect"].collidepoint(mouse_pos):
                    pressed_note = key["note"]
                    print(f"Black Key: {key['note']} | MIDI: {key['midi']}")
                    sound_engine.play_note(key["midi"])
                    key_found = True
                    break

            # Check White Keys
            if not key_found:
                for key in white_keys:
                    if key["rect"].collidepoint(mouse_pos):
                        pressed_note = key["note"]
                        print(f"White Key: {key['note']} | MIDI: {key['midi']}")
                        sound_engine.play_note(key["midi"])
                        break

    # DRAW
    screen.fill("gray")

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    # Draw White Keys
    for key in white_keys:
        rect = key["rect"]
        over_black = False

        for black_key in black_keys:
            if black_key["rect"].collidepoint(mouse_pos):
                over_black = True
                break

        if mouse_pressed and rect.collidepoint(mouse_pos) and not over_black:
            color = "lightblue"
        else:
            color = "white"

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, "black", rect, 2)

    # Draw Black Keys
    for key in black_keys:
        rect = key["rect"]

        if mouse_pressed and rect.collidepoint(mouse_pos):
            color = "darkblue"
        else:
            color = "black"

        pygame.draw.rect(screen, color, rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()