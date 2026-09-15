"""Piano calibration: position the virtual piano within the camera frame."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass

# Default calibration: keyboard occupies the bottom third of the frame.
DEFAULT_X_FRACTION: float = 0.05
DEFAULT_Y_FRACTION: float = 0.62
DEFAULT_WIDTH_FRACTION: float = 0.90
DEFAULT_HEIGHT_FRACTION: float = 0.33

CALIBRATION_FILENAME: str = "calibration.json"


def clamp01(value: float) -> float:
    """Clamp a value to the inclusive [0, 1] range."""
    return max(0.0, min(1.0, float(value)))


@dataclass(frozen=True)
class PianoCalibration:
    """Normalized placement of the piano within the camera frame.

    All fractions are relative to the frame dimensions:
        x_fraction      — left edge of the keyboard 
        y_fraction      — top edge of the keyboard 
        width_fraction  — total keyboard width 
        height_fraction — total keyboard height
    """

    x_fraction: float = DEFAULT_X_FRACTION
    y_fraction: float = DEFAULT_Y_FRACTION
    width_fraction: float = DEFAULT_WIDTH_FRACTION
    height_fraction: float = DEFAULT_HEIGHT_FRACTION

    def __post_init__(self) -> None:
        # Validate ranges.
        for field_name, value in (
            ("x_fraction", self.x_fraction),
            ("y_fraction", self.y_fraction),
            ("width_fraction", self.width_fraction),
            ("height_fraction", self.height_fraction),
        ):
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"{field_name} must be in [0, 1], got {value}"
                )

    @classmethod
    def from_default(cls) -> "PianoCalibration":
        """Return a calibration anchored to the bottom of the frame."""
        return cls()

    def to_pixels(
        self,
        frame_width: int,
        frame_height: int,
    ) -> tuple[int, int, int, int]:
        """Convert the normalized calibration to pixel geometry."""

        

        x = int(self.x_fraction * frame_width)
        y = int(self.y_fraction * frame_height)
        width = int(self.width_fraction * frame_width)
        height = int(self.height_fraction * frame_height)
        return x, y, width, height

    def to_dict(self) -> dict[str, float]:
        """Return a JSON-serializable dict of the calibration."""
        return {
            "x_fraction": self.x_fraction,
            "y_fraction": self.y_fraction,
            "width_fraction": self.width_fraction,
            "height_fraction": self.height_fraction,
        }

    @classmethod
    def from_dict(cls, data: dict[str, float]) -> "PianoCalibration":
        """Create a calibration from a dict, filling in defaults for missing values."""
        defaults = cls().to_dict()
        merged = {**defaults, **data}
        return cls(
            x_fraction=clamp01(merged["x_fraction"]),
            y_fraction=clamp01(merged["y_fraction"]),
            width_fraction=clamp01(merged["width_fraction"]),
            height_fraction=clamp01(merged["height_fraction"]),
        )

    def save(self, path: str = CALIBRATION_FILENAME) -> None:
        """Persist the calibration to a JSON file.

        Args:
            path: Output file path (default ``calibration.json``).
        """
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.to_dict(), fh, indent=2)
        print(f"Calibration saved to {os.path.abspath(path)}")

    @classmethod
    def load(cls, path: str = CALIBRATION_FILENAME) -> "PianoCalibration":
        """Load a calibration from a JSON file."""

        
        if not os.path.isfile(path):
            raise FileNotFoundError(
                f"Calibration file not found: {path}"
            )
        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"Calibration file {path} is not valid JSON: {exc}"
            ) from exc

        if not isinstance(data, dict):
            raise ValueError(
                f"Calibration file {path} must contain a JSON object."
            )
        return cls.from_dict(data)