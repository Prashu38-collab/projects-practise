import os
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# MODEL PATH
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(
    SCRIPT_DIR,
    "hand_landmarker.task"
)

print("MediaPipe version:", mp.__version__)
print("Model:", MODEL_PATH)
print("Model exists:", os.path.exists(MODEL_PATH))

# CREATE HAND LANDMARKER

options = HandLandmarkerOptions(
    base_options=BaseOptions(
        model_asset_path=MODEL_PATH
    ),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=2
)

with HandLandmarker.create_from_options(options) as landmarker:

    print(" Hand Landmarker created successfully!")
