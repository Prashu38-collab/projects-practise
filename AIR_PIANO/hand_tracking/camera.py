"""Webcam capture module for Air Piano.
Provides a Camera class that handles webcam initialization,
frame capture, FPS calculation, and graceful shutdown.
"""
import time
import cv2
import numpy as np


class Camera:
    """Manages webcam capture with FPS tracking and mirror support."""

    DEFAULT_WIDTH: int = 640
    DEFAULT_HEIGHT: int = 480
    DEFAULT_FPS: int = 30

    def __init__(
        self,
        camera_index: int = 0,
        mirror: bool = True,
    ) -> None:
        """Initialize webcam capture.

        Args:
            camera_index: Index of the webcam device (default 0).
            mirror: If True, mirror the frame horizontally.

        Raises:
            RuntimeError: If the webcam cannot be opened.
        """
        self._mirror = mirror
        self._cap: cv2.VideoCapture | None = None
        self._camera_index = camera_index

        # FPS tracking
        self._frame_count: int = 0
        self._fps: float = 0.0
        self._fps_timer: float = time.perf_counter()
        self._fps_update_interval: float = 0.5  # update FPS display every 0.5s

        # Resolution
        self._width: int = self.DEFAULT_WIDTH
        self._height: int = self.DEFAULT_HEIGHT

        self._open()

    def _open(self) -> None:
        """Open the webcam device and apply resolution settings."""
        self._cap = cv2.VideoCapture(self._camera_index)

        if not self._cap.isOpened():
            hint = self._permission_hint()
            raise RuntimeError(
                f"Cannot open webcam (index={self._camera_index}). "
                "Check that a camera is connected and not in use "
                "by another application." + hint
            )

        # Set resolution and FPS
        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.DEFAULT_WIDTH)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.DEFAULT_HEIGHT)
        self._cap.set(cv2.CAP_PROP_FPS, self.DEFAULT_FPS)

        # Read actual resolution (camera may round to supported values)
        self._width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self._height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(f"Camera opened: {self._width}x{self._height} "
              f"(device index={self._camera_index})")

    @staticmethod
    def _permission_hint() -> str:
        """Return a platform-specific hint if camera permission is denied.

        On macOS, a missing Camera permission in System Settings is a common
        reason OpenCV cannot open the capture device.
        """
        import platform

        if platform.system() == "Darwin":
            return (
                " On macOS, ensure the terminal/app is granted Camera access: "
                "System Settings > Privacy & Security > Camera."
            )
        return ""

    @property
    def width(self) -> int:
        """Return the frame width in pixels."""
        return self._width

    @property
    def height(self) -> int:
        """Return the frame height in pixels."""
        return self._height

    @property
    def fps(self) -> float:
        """Return the current measured FPS."""
        return self._fps

    def read(self) -> tuple[bool, np.ndarray | None]:
        """Read a frame from the webcam.

        Returns:
            A tuple of (success, frame). If success is False,
            frame is None.
        """
        if self._cap is None or not self._cap.isOpened():
            return False, None

        success, frame = self._cap.read()

        if not success or frame is None:
            return False, None

        if self._mirror:
            frame = cv2.flip(frame, 1)

        self._update_fps()

        return True, frame

    def _update_fps(self) -> None:
        """Calculate FPS over a rolling window."""
        self._frame_count += 1
        now = time.perf_counter()
        elapsed = now - self._fps_timer

        if elapsed >= self._fps_update_interval:
            self._fps = self._frame_count / elapsed
            self._frame_count = 0
            self._fps_timer = now

    def release(self) -> None:
        """Release the webcam resource."""
        cap = getattr(self, "_cap", None)
        if cap is not None and cap.isOpened():
            cap.release()
            print("Camera released.")
        self._cap = None

    def __del__(self) -> None:
        """Ensure the camera is released on garbage collection."""
        self.release()
