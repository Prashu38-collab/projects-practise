"""Mapping camera-frame fingertip positions into piano-window coordinates."""


from __future__ import annotations

from vision.calibration import PianoCalibration


class CameraToWindowMapper:
    """Linearly map points from a camera region onto a piano window."""
    def __init__(
        self,
        calibration: PianoCalibration,
        camera_width: int,
        camera_height: int,
        window_width: int,
        window_height: int,
    ) -> None:
        self._calibration = calibration
        self._window_width = window_width
        self._window_height = window_height
        self._region_x, self._region_y, self._region_w, self._region_h = (
            calibration.to_pixels(camera_width, camera_height)
        )

    @property
    def region_rect(self) -> tuple[int, int, int, int]:
        """Return the camera-frame region x, y, width, height in pixels."""
        return self._region_x, self._region_y, self._region_w, self._region_h

    @property
    def scale_x(self) -> float:
        """Camera-pixels-to-window-pixels scale factor along X."""
        return self._window_width / max(1, self._region_w)

    @property
    def scale_y(self) -> float:
        """Camera-pixels-to-window-pixels scale factor along Y."""
        return self._window_height / max(1, self._region_h)

    def to_window(self, x: float, y: float) -> tuple[float, float]:
        """Map a camera-frame point onto the piano window."""
        wx = (float(x) - self._region_x) * self.scale_x
        wy = (float(y) - self._region_y) * self.scale_y
        return wx, wy