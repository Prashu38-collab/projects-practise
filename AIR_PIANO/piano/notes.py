"""Note definitions for the Air Piano.

A note name c4 maps to a MIDI note number and frequency.

    f(n) = 440 * 2 ** ((n - 69) / 12)

where n is the MIDI note number and A4 = MIDI 69 = 440 Hz.
"""

from __future__ import annotations

from dataclasses import dataclass
NOTE_NAMES: tuple[str, ...] = (
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B",
)

# MIDI number for C2, the lowest note of the standard 61-key piano (C2-C7).
C2_MIDI: int = 36

# A4 = MIDI 69 = 440 Hz.
A4_MIDI: int = 69
A4_FREQUENCY: float = 440.0

# MIDI note numbers for the middle-C-to-B octave 
MIDI_NOTE_NUMBERS: dict[str, int] = {
    "C4": 60, "D4": 62, "E4": 64, "F4": 65, "G4": 67, "A4": 69, "B4": 71,
}

# White keys rendered in Phase 3 (one octave, natural notes only).
DEFAULT_WHITE_KEYS: tuple[str, ...] = ("C4", "D4", "E4", "F4", "G4", "A4", "B4")


def midi_to_name(midi_number: int) -> str:
    """Return the note name for a MIDI number """

    octave = midi_number // 12 - 1
    name = NOTE_NAMES[midi_number % 12]
    return f"{name}{octave}"


def is_black_name(name: str) -> bool:
    
    return "#" in name


def midi_to_frequency(midi_number: int) -> float:
    """Return the frequency in Hz for a MIDI number."""

   
    return A4_FREQUENCY * (2.0 ** ((midi_number - A4_MIDI) / 12.0))


@dataclass(frozen=True)
class Note:
    """A musical note."""
    name: str
    midi_number: int
    frequency: float

    @property
    def wav_filename(self) -> str:
        """Return the expected audio filename c4.wav eg."""
        return f"{self.name}.wav"


def get_note(name: str) -> Note:
   
    if name not in MIDI_NOTE_NUMBERS:
        raise ValueError(
            f"Unknown note '{name}'. Supported notes: "
            f"{sorted(MIDI_NOTE_NUMBERS)}"
        )
    midi = MIDI_NOTE_NUMBERS[name]
    return Note(name=name, midi_number=midi, frequency=midi_to_frequency(midi))


def get_notes(names: tuple[str, ...]) -> list[Note]:
    return [get_note(name) for name in names]


def get_notes_by_midi(
    start_midi: int = C2_MIDI,
    count: int = 61,
) -> list[Note]:
  
    return [
        Note(
            name=midi_to_name(midi),
            midi_number=midi,
            frequency=midi_to_frequency(midi),
        )
        for midi in range(start_midi, start_midi + count)
    ]


def split_black_and_white(notes: list[Note]) -> tuple[list[Note], list[Note]]:
    white: list[Note] = [n for n in notes if not is_black_name(n.name)]
    black: list[Note] = [n for n in notes if is_black_name(n.name)]
    return white, black


def note_from_midi(midi_number: int) -> Note:
    return Note(
        name=midi_to_name(midi_number),
        midi_number=midi_number,
        frequency=midi_to_frequency(midi_number),
    )