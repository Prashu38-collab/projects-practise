
import os
import sys

import cv2

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from hand_tracking.camera import Camera
from hand_tracking.detector import HandDetector, draw_hand_skeleton
from hand_tracking.landmarks import LandmarkIndex
from piano.pygame_piano import PygamePiano
from vision.calibration import PianoCalibration
from vision.coordinate_mapper import CameraToWindowMapper
from vision.press_detection import FINGERS_PER_HAND, PressDetector

WINDOW_NAME: str = "Air Piano — Camera"
QUIT_KEYS: set[int] = {ord("q"), 27}  # Q or ESC

# Press detection tuning (see vision/press_detection.py for details).
DOWNWARD_THRESHOLD: float = 12.0     # camera pixels per frame (increased for stability)
NOTE_COOLDOWN: float = 0.10         # seconds
SMOOTHING: float = 0.5              # exponential smoothing alpha in (0, 1]

# Calibration file (optional; falls back to defaults).
CALIBRATION_FILE: str = "calibration.json"

# One landmark index per finger (thumb, index, middle, ring, pinky).
FINGER_TIP_LANDMARKS: list[LandmarkIndex] = [
    LandmarkIndex.THUMB_TIP,
    LandmarkIndex.INDEX_TIP,
    LandmarkIndex.MIDDLE_TIP,
    LandmarkIndex.RING_TIP,
    LandmarkIndex.PINKY_TIP,
]


def load_calibration() -> PianoCalibration:
    """Load calibration if present, else use defaults.

    A missing file is not an error; the default bottom-anchored layout is used.
    A malformed file is an error so the user can fix it.
    """
    try:
        cal = PianoCalibration.load(CALIBRATION_FILE)
        print(f"Loaded calibration from {CALIBRATION_FILE}")
        return cal
    except FileNotFoundError:
        return PianoCalibration.from_default()
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Falling back to default calibration.", file=sys.stderr)
        return PianoCalibration.from_default()


def draw_hud(frame: cv2.Mat, fps: float, hand_count: int) -> cv2.Mat:
    """Draw the FPS counter and general status HUD."""
    cv2.putText(
        frame, f"FPS: {fps:.1f}", (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2,
    )
    cv2.putText(
        frame, f"Hands: {hand_count}", (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2,
    )
    cv2.putText(
        frame, "Press Q or ESC to quit", (10, 90),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1,
    )
    return frame


def draw_play_region(
    frame: cv2.Mat,
    mapper: CameraToWindowMapper,
) -> cv2.Mat:
    """Outline the calibrated play region in the camera frame."""
    x, y, w, h = mapper.region_rect
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(
        frame, "Play region", (x + 4, y - 8),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1,
    )
    return frame


def draw_fingertips(
    frame: cv2.Mat,
    hands: list,
    hand_labels: list[str],
) -> cv2.Mat:
    """Draw markers and labels at each tracked fingertip."""
    for hand, label in zip(hands, hand_labels):
        pts = hand.landmarks
        for idx in FINGER_TIP_LANDMARKS:
            pt = (int(pts[int(idx)][0]), int(pts[int(idx)][1]))
            cv2.circle(frame, pt, 8, (0, 255, 255), 2, cv2.LINE_AA)
        tip = (int(pts[int(LandmarkIndex.INDEX_TIP)][0]),
               int(pts[int(LandmarkIndex.INDEX_TIP)][1]))
        cv2.putText(
            frame, label, (tip[0] - 20, tip[1] - 16),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 1,
        )
    return frame


def main() -> None:
    """Run the Air Piano application."""
    try:
        camera = Camera(camera_index=0, mirror=True)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        detector = HandDetector(num_hands=2)
        piano = PygamePiano()
    except (FileNotFoundError, RuntimeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        camera.release()
        sys.exit(1)

    calibration = load_calibration()
    mapper = CameraToWindowMapper(
        calibration=calibration,
        camera_width=camera.width,
        camera_height=camera.height,
        window_width=piano._width,
        window_height=piano._height,
    )

    # Downward threshold expressed in piano-window pixels.
    threshold_window = max(2.0, DOWNWARD_THRESHOLD * mapper.scale_y)
    press_detector = PressDetector(
        piano.keyboard,
        downward_threshold=threshold_window,
        cooldown=NOTE_COOLDOWN,
        smoothing=SMOOTHING,
        trigger_indices=None,  # all fingers can trigger notes
    )

    cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_AUTOSIZE)

    print("Air Piano — Computer Vision Virtual Piano")
    print(f"Piano window: 61-key layout ({piano._width}x{piano._height}), "
          f"{len(piano.keyboard.keys)} keys total")
    print(f"Tracking up to {FINGERS_PER_HAND} fingertips per hand.")
    print("Note trigger: all fingers enabled.")
    print(f"Play region in camera: {mapper.region_rect}")
    print(f"Downward threshold: {threshold_window:.1f} window px")
    print("Press Q or ESC (camera window) or close the piano window to quit.")

    try:
        while True:
            success, frame = camera.read()

            if not success or frame is None:
                print("Warning: Failed to read frame from camera.", file=sys.stderr)
                continue

            piano.handle_events()
            if piano.quit_requested:
                break

            hands = detector.detect(frame)
            hand_labels = [h.handedness for h in hands]

            # Extract all fingertips per hand, in a fixed order, in window
            # coordinates for press detection and hover.
            windows: list[list[tuple[float, float]]] = []
            for hand in hands:
                pts = hand.landmarks
                finger_window_points: list[tuple[float, float]] = []
                for idx in FINGER_TIP_LANDMARKS:
                    wx, wy = mapper.to_window(
                        float(pts[int(idx)][0]), float(pts[int(idx)][1])
                    )
                    finger_window_points.append((wx, wy))
                windows.append(finger_window_points)

            # Downward press detection + audio (multi-finger, two-hand).
            triggered, hovered = press_detector.update(windows, hand_labels)
            for key in triggered:
                piano.play_key(key)

            # Hover highlight: every key currently under a fingertip.
            hover_names = {key.note.name for key in hovered.values()}
            piano.set_hover(hover_names)

            piano.draw()

            for hand in hands:
                draw_hand_skeleton(frame, hand)

            frame = draw_play_region(frame, mapper)
            frame = draw_hud(frame, camera.fps, len(hands))
            frame = draw_fingertips(frame, hands, hand_labels)

            cv2.imshow(WINDOW_NAME, frame)

            key_press = cv2.waitKey(1) & 0xFF
            if key_press in QUIT_KEYS:
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    finally:
        detector.close()
        piano.close()
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()