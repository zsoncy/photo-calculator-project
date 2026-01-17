import cv2
import numpy as np

def find_char_boxes(bw: np.ndarray):
    # Invert for finding connected components: text -> 255
    inv = 255 - bw
    # Remove tiny blobs
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    clean = cv2.morphologyEx(inv, cv2.MORPH_OPEN, se)

    # Connected components
    n, labels, stats, _ = cv2.connectedComponentsWithStats(clean, connectivity=8)
    boxes = []
    H, W = bw.shape[:2]
    for i in range(1, n):
        x, y, w, h, area = stats[i]
        if area < 20:        # too small
            continue
        if h < 8 or w < 5:   # too thin
            continue
        if h > 0.9*H or w > 0.9*W:
            continue
        boxes.append((x, y, w, h))

    # sort by row (y), then x
    boxes.sort(key=lambda b: (b[1]//30, b[0]))
    return boxes

def extract_28x28(bw: np.ndarray, box, pad=4):
    x, y, w, h = box
    roi = bw[y:y+h, x:x+w]
    # make square canvas (white), paste centered
    side = max(w, h) + 2*pad
    canvas = np.full((side, side), 255, dtype=np.uint8)
    x0 = (side - w)//2
    y0 = (side - h)//2
    canvas[y0:y0+h, x0:x0+w] = roi
    # resize to 28x28
    out = cv2.resize(canvas, (28,28), interpolation=cv2.INTER_AREA)
    # invert for CNN if trained on digit white on black (optional)
    # EMNIST typically uses white digit on black background; if your training used that:
    # out = 255 - out
    return out
