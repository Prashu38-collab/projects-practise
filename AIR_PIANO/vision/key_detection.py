"""Mapping fingertip positions to piano keys.

Separates the geometry question ("which key is at this pixel?") from the
motion question ("should this key be triggered?").
"""

from __future__ import annotations

from typing import TypeAlias

import numpy as np

from piano.keyboard import Key, PianoKeyboard

# A 2D position in pixel coordinates.
Point: TypeAlias = tuple[float, float] | np.ndarray


def map_fingertip_to_key(
    keyboard: PianoKeyboard,
    fingertip: Point,
) -> Key | None:
    """Return the key under a fingertip position, or None.

    Args:
        keyboard: The keyboard to query.
        fingertip: (x, y) fingertip position in pixels.

    Returns:
        The Key under the fingertip, or None if the fingertip is outside
        the keyboard.
    """
    if isinstance(fingertip, np.ndarray):
        fingertip = (float(fingertip[0]), float(fingertip[1]))
    x, y = fingertip
    return keyboard.hit_test(float(x), float(y))


def is_inside_keyboard(key: Key | None) -> bool:
    """Return True if a key was resolved for the fingertip."""
    return key is not None