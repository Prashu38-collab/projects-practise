import os
import cv2
import turtle
import numpy as np

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_image_path():
    valid_exts = ('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.JPG', '.JPEG', '.PNG')
    for file in os.listdir(SCRIPT_DIR):
        if file.endswith(valid_exts):
            return os.path.join(SCRIPT_DIR, file)
    return None

def draw_detailed_sketch(image_path):
    if not image_path:
        print(f"Error: No image file found in {SCRIPT_DIR}")
        return

    print(f"Processing image: {image_path}")
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Could not read image.")
        return

    # 1. Scale image to fit canvas comfortably
    h, w = img.shape
    max_dim = 700
    if max(h, w) > max_dim:
        scale = max_dim / float(max(h, w))
        w, h = int(w * scale), int(h * scale)
        img = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)

    # 2. CLAHE Contrast Enhancement: Sharpens faint facial details (eyes, lips, nose)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(img)

    # 3. Bilateral Filter: Smooths out skin/background textures while keeping edges sharp
    smoothed = cv2.bilateralFilter(enhanced, d=7, sigmaColor=50, sigmaSpace=50)

    # 4. Tuned Canny Edge Detection
    edges = cv2.Canny(smoothed, threshold1=30, threshold2=110)

    # 5. Connect broken outline gaps
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    connected_edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(connected_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # 6. Turtle Window Setup
    screen = turtle.Screen()
    screen.setup(width=w + 60, height=h + 60)
    screen.bgcolor("black")
    screen.title("Radha Krishna & Cow — Detailed Face & Body Sketch")
    screen.tracer(0)

    t = turtle.Turtle()
    t.hideturtle()
    t.pencolor("white")
    t.pensize(1.2)

    half_w, half_h = w / 2, h / 2

    try:
        for contour in contours:
            length = cv2.arcLength(contour, False)
            
            # Calculate position center of this contour
            pts = contour.reshape(-1, 2)
            mean_x = np.mean(pts[:, 0]) / w
            mean_y = np.mean(pts[:, 1]) / h

            # Zone Definition:
            is_background_border = (mean_y < 0.12) or (mean_x < 0.05) or (mean_x > 0.95) or (mean_y > 0.90)
            is_face_region = (0.25 <= mean_x <= 0.80) and (0.10 <= mean_y <= 0.45)

            # Filtering Rules:
            if is_background_border:
                # Discard background leaf & sky specks, keep only long frame lines
                if length < 80:
                    continue
            elif is_face_region:
                # Allow fine detail lines (eyes, eyebrows, nostrils, lips)
                if length < 8:
                    continue
            else:
                # Body, jewelry, and cow main contours
                if length < 30:
                    continue

            # Draw Contour
            start_x, start_y = contour[0][0]
            t.penup()
            t.goto(start_x - half_w, half_h - start_y)
            t.pendown()

            for pt in contour[1:]:
                x, y = pt[0]
                t.goto(x - half_w, half_h - y)

            screen.update()

    except turtle.Terminator:
        print("Window closed gracefully.")

    screen.update()
    turtle.done()

if __name__ == "__main__":
    image_path = get_image_path()
    draw_detailed_sketch(image_path)


