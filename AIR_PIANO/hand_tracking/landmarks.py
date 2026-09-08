"""MediaPipe hand landmark index constants.

These indices follow the standard MediaPipe hand landmark convention
(21 landmarks). Refer to:
https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker
"""

from enum import IntEnum


class LandmarkIndex(IntEnum):
    """Indices of the 21 hand landmarks returned by Hand Landmarker."""

    WRIST = 0

    THUMB_CMC = 1
    THUMB_MCP = 2
    THUMB_IP = 3
    THUMB_TIP = 4

    INDEX_MCP = 5
    INDEX_PIP = 6
    INDEX_DIP = 7
    INDEX_TIP = 8

    MIDDLE_MCP = 9
    MIDDLE_PIP = 10
    MIDDLE_DIP = 11
    MIDDLE_TIP = 12

    RING_MCP = 13
    RING_PIP = 14
    RING_DIP = 15
    RING_TIP = 16

    PINKY_MCP = 17
    PINKY_PIP = 18
    PINKY_DIP = 19
    PINKY_TIP = 20


NUM_LANDMARKS: int = 21

# Connections between landmarks for skeletal rendering.
# Each tuple connects two landmark indices.
HAND_CONNECTIONS: tuple[tuple[int, int], ...] = (
    # Thumb
    (LandmarkIndex.WRIST, LandmarkIndex.THUMB_CMC),
    (LandmarkIndex.THUMB_CMC, LandmarkIndex.THUMB_MCP),
    (LandmarkIndex.THUMB_MCP, LandmarkIndex.THUMB_IP),
    (LandmarkIndex.THUMB_IP, LandmarkIndex.THUMB_TIP),
    # Index finger
    (LandmarkIndex.WRIST, LandmarkIndex.INDEX_MCP),
    (LandmarkIndex.INDEX_MCP, LandmarkIndex.INDEX_PIP),
    (LandmarkIndex.INDEX_PIP, LandmarkIndex.INDEX_DIP),
    (LandmarkIndex.INDEX_DIP, LandmarkIndex.INDEX_TIP),
    # Middle finger
    (LandmarkIndex.INDEX_MCP, LandmarkIndex.MIDDLE_MCP),
    (LandmarkIndex.MIDDLE_MCP, LandmarkIndex.MIDDLE_PIP),
    (LandmarkIndex.MIDDLE_PIP, LandmarkIndex.MIDDLE_DIP),
    (LandmarkIndex.MIDDLE_DIP, LandmarkIndex.MIDDLE_TIP),
    # Ring finger
    (LandmarkIndex.MIDDLE_MCP, LandmarkIndex.RING_MCP),
    (LandmarkIndex.RING_MCP, LandmarkIndex.RING_PIP),
    (LandmarkIndex.RING_PIP, LandmarkIndex.RING_DIP),
    (LandmarkIndex.RING_DIP, LandmarkIndex.RING_TIP),
    # Pinky
    (LandmarkIndex.RING_MCP, LandmarkIndex.PINKY_MCP),
    (LandmarkIndex.PINKY_MCP, LandmarkIndex.PINKY_PIP),
    (LandmarkIndex.PINKY_PIP, LandmarkIndex.PINKY_DIP),
    (LandmarkIndex.PINKY_DIP, LandmarkIndex.PINKY_TIP),
)

# Landmark names (for logging and debugging).
LANDMARK_NAMES: dict[int, str] = {
    LandmarkIndex.WRIST: "wrist",
    LandmarkIndex.THUMB_CMC: "thumb_cmc",
    LandmarkIndex.THUMB_MCP: "thumb_mcp",
    LandmarkIndex.THUMB_IP: "thumb_ip",
    LandmarkIndex.THUMB_TIP: "thumb_tip",
    LandmarkIndex.INDEX_MCP: "index_mcp",
    LandmarkIndex.INDEX_PIP: "index_pip",
    LandmarkIndex.INDEX_DIP: "index_dip",
    LandmarkIndex.INDEX_TIP: "index_tip",
    LandmarkIndex.MIDDLE_MCP: "middle_mcp",
    LandmarkIndex.MIDDLE_PIP: "middle_pip",
    LandmarkIndex.MIDDLE_DIP: "middle_dip",
    LandmarkIndex.MIDDLE_TIP: "middle_tip",
    LandmarkIndex.RING_MCP: "ring_mcp",
    LandmarkIndex.RING_PIP: "ring_pip",
    LandmarkIndex.RING_DIP: "ring_dip",
    LandmarkIndex.RING_TIP: "ring_tip",
    LandmarkIndex.PINKY_MCP: "pinky_mcp",
    LandmarkIndex.PINKY_PIP: "pinky_pip",
    LandmarkIndex.PINKY_DIP: "pinky_dip",
    LandmarkIndex.PINKY_TIP: "pinky_tip",
}