"""Hand detection using the MediaPipe Tasks Hand Landmarker API.

"""
from __future__ import annotations

import os
import time
from dataclasses import dataclass

import cv2
import mediapipe as mp
import numpy as np

from hand_tracking.landmarks import (
    HAND_CONNECTIONS,
    LandmarkIndex,
    NUM_LANDMARKS,
)

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode
HandLandmarkerResult = mp.tasks.vision.HandLandmarkerResult


@dataclass(frozen=True)
class Hand:
    """All 21 hand landmarks in pixel coordinates."""
    handedness: str
    confidence: float
    landmarks: np.ndarray
def find_model_path() -> str:
    """Locate the ``hand_landmarker.task`` model file."""

    
    package_dir = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(package_dir, os.pardir, "models", "hand_landmarker.task"),
        os.path.join(os.getcwd(), "models", "hand_landmarker.task"),
        os.path.join(package_dir, "models", "hand_landmarker.task"),
    ]

    for candidate in candidates:
        path = os.path.abspath(candidate)
        if os.path.isfile(path):
            return path

    raise FileNotFoundError(
        "Could not find 'hand_landmarker.task'. Download it into the "
        "'models/' directory from: "
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/"
        "hand_landmarker/float16/latest/hand_landmarker.task "
        f"Searched: {', '.join(candidates)}"
    )


class HandDetector:
    """Wraps the MediaPipe Tasks Hand Landmarker.

    This detector runs in VIDEO mode and expects a monotonically
    increasing timestamp (in ms) supplied by the caller for each frame.

    Args:
        model_path: Path to the ``hand_landmarker.task`` model file.
            Defaults to the project ``models/`` directory.
        num_hands: Maximum number of hands to detect (default 2).
        min_hand_detection_confidence: Minimum confidence for palm
            detection in [0, 1].
        min_hand_presence_confidence: Minimum confidence for hand
            presence scoring.
        min_tracking_confidence: Minimum confidence for tracking.
        delegate: Device delegate (CPU or GPU).

    Raises:
        FileNotFoundError: If the model file does not exist.
        RuntimeError: If MediaPipe fails to initialize the landmarker.
    """

    def __init__(
        self,
        model_path: str | None = None,
        num_hands: int = 2,
        min_hand_detection_confidence: float = 0.5,
        min_hand_presence_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
        delegate: BaseOptions.Delegate = BaseOptions.Delegate.CPU,
    ) -> None:
        self._model_path = model_path or find_model_path()

        if not os.path.isfile(self._model_path):
            raise FileNotFoundError(
                f"Hand Landmarker model not found: {self._model_path}"
            )

        self._num_hands = num_hands
        self._landmarker: HandLandmarker | None = None
        self._start_time: float = time.perf_counter()

        options = HandLandmarkerOptions(
            base_options=BaseOptions(
                model_asset_path=self._model_path,
                delegate=delegate,
            ),
            running_mode=VisionRunningMode.VIDEO,
            num_hands=num_hands,
            min_hand_detection_confidence=min_hand_detection_confidence,
            min_hand_presence_confidence=min_hand_presence_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )

        try:
            self._landmarker = HandLandmarker.create_from_options(options)
        except Exception as exc:  # MediaPipe raises TaskRunner fatal errors
            raise RuntimeError(
                "Failed to initialize MediaPipe Hand Landmarker. "
                f"Model: {self._model_path}. Original error: {exc}"
            ) from exc

        print(f"Hand Landmarker initialized (model: {self._model_path})")

    @property
    def num_hands(self) -> int:
        """Return the configured maximum number of hands."""
        return self._num_hands

    def detect(self, frame_bgr: np.ndarray) -> list[Hand]:
        """Detect hands in a BGR frame.

        Args:
            frame_bgr: A BGR-format frame (as produced by OpenCV).

        Returns:
            A list of ``Hand`` objects, one per detected hand.
            The list is empty if no hands are present.

        Raises:
            RuntimeError: If called before/after the landmarker is ready.
        """
        if self._landmarker is None:
            raise RuntimeError("Hand Landmarker is not initialized.")

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        # Real elapsed milliseconds since detector creation. MediaPipe's
        # detect_for_video requires monotonically increasing timestamps; using
        # real time improves inter-frame tracking accuracy.
        timestamp_ms = int((time.perf_counter() - self._start_time) * 1000)

        try:
            result: HandLandmarkerResult = self._landmarker.detect_for_video(
                mp_image, timestamp_ms
            )
        except Exception as exc:
            raise RuntimeError(
                f"MediaPipe detect_for_video failed: {exc}"
            ) from exc

        hands: list[Hand] = []
        height, width = frame_bgr.shape[:2]

        if not result.hand_landmarks:
            return hands

        for hand_index, landmarks in enumerate(result.hand_landmarks):
            if len(landmarks) != NUM_LANDMARKS:
                continue

            pts = np.empty((NUM_LANDMARKS, 2), dtype=np.float32)
            for i, lm in enumerate(landmarks):
                pts[i, 0] = lm.x * width
                pts[i, 1] = lm.y * height

            handedness = "Right"
            confidence = 0.0
            if result.handedness and hand_index < len(result.handedness):
                top = result.handedness[hand_index][0]
                handedness = top.category_name
                confidence = float(top.score)

            hands.append(Hand(handedness=handedness, confidence=confidence, landmarks=pts))

        return hands

    def close(self) -> None:
        """Release the underlying landmarker resources."""
        if self._landmarker is not None:
            try:
                self._landmarker.close()
            except Exception:
                pass
            self._landmarker = None

    def __enter__(self) -> "HandDetector":
        """Support use as a context manager."""
        return self

    def __exit__(self, *exc_info: object) -> None:
        """Close resources on context exit."""
        self.close()


def draw_hand_skeleton(
    frame: np.ndarray,
    hand: Hand,
    *,
    point_color: tuple[int, int, int] = (0, 255, 0),
    line_color: tuple[int, int, int] = (0, 200, 255),
) -> np.ndarray:
    """Draw the hand skeleton on a BGR frame, in place.

    Args:
        frame: The BGR frame to draw on.
        hand: The detected hand.
        point_color: BGR color for landmark points.
        line_color: BGR color for connecting lines.

    Returns:
        The same frame, modified in place.
    """
    pts = hand.landmarks.astype(int)

    for a, b in HAND_CONNECTIONS:
        cv2.line(frame, tuple(pts[a]), tuple(pts[b]), line_color, 2)

    for idx in LandmarkIndex:
        cv2.circle(frame, tuple(pts[int(idx)]), 4, point_color, -1, cv2.LINE_AA)

    # Emphasize the index fingertip.
    tip = tuple(pts[int(LandmarkIndex.INDEX_TIP)])
    cv2.circle(frame, tip, 8, (0, 255, 255), 2, cv2.LINE_AA)

    return frame