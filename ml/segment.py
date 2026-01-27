import cv2
import numpy as np


def find_char_boxes(bw: np.ndarray):

    inv = 255 - bw

    cleaned = inv

    # connectivity=8 checks diagonal pixels too
    n, labels, stats, _ = cv2.connectedComponentsWithStats(cleaned, connectivity=8)

    boxes = []
    H, W = bw.shape[:2]

    # Loop through found components (skip i=0 because that is the background)
    for i in range(1, n):
        x, y, w, h, area = stats[i]

        # Filtering
        if area < 30: continue  # Too small
        if w > 0.9 * W or h > 0.9 * H: continue  # Too big

        boxes.append((x, y, w, h))

    # SORTING
    # Sort boxes based on the X-coordinate (Left -> Right)
    boxes.sort(key=lambda b: b[0])

    return boxes


def extract_28x28(bw: np.ndarray, box, pad=0):
    x, y, w, h = box

    # Cut out the character
    roi = bw[y:y + h, x:x + w]

    # Resize
    scale = 20.0 / max(w, h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    resized_roi = cv2.resize(roi, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Center
    canvas = np.full((28, 28), 255, dtype=np.uint8)  # White background

    x_center = (28 - new_w) // 2
    y_center = (28 - new_h) // 2

    canvas[y_center:y_center + new_h, x_center:x_center + new_w] = resized_roi

    # Invert (White Text on Black)
    out = 255 - canvas
    _, out = cv2.threshold(out, 127, 255, cv2.THRESH_BINARY)

    return out
