import cv2
import numpy as np
import os
import sys
import uuid


def scrape_sheet(image_path, label, output_root="data/custom_data"):
    print(f"Scraping {label} from {image_path}...")

    img = cv2.imread(image_path)
    if img is None:
        print("Error: Could not read image.")
        return

    # STANDARDIZE SIZE
    h, w = img.shape[:2]
    target_h = 1000
    scale = target_h / h
    target_w = int(w * scale)
    img = cv2.resize(img, (target_w, target_h))

    # PREPROCESSING
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Slight blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Create the CLEAN Black & White image
    bw_clean = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 41, 15
    )

    # Remove tiny noise
    kernel_clean = np.ones((3, 3), np.uint8)
    bw_clean = cv2.morphologyEx(bw_clean, cv2.MORPH_OPEN, kernel_clean)

    # CREATE THE "GLUED" VERSION (Only for finding boxes)

    kernel_glue = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 15))
    bw_glued = cv2.morphologyEx(bw_clean, cv2.MORPH_CLOSE, kernel_glue)

    # FIND CONTOURS ON THE GLUED IMAGE
    contours, _ = cv2.findContours(bw_glued, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # FILTER & EXTRACT
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    bounding_boxes.sort(key=lambda x: x[0] + x[1] * target_w)

    valid_samples = []

    for box in bounding_boxes:
        x, y, w, h = box

        # Filter noise
        if w < 20: continue
        if h < 8: continue  # Allow short symbols
        if w > 400 or h > 400: continue

        # CUT FROM THE CLEAN IMAGE, not glued
        roi = bw_clean[y:y + h, x:x + w]

        # MAKE IT EMNIST STYLE
        h_roi, w_roi = roi.shape
        scale_factor = 20.0 / max(h_roi, w_roi)

        new_w = int(w_roi * scale_factor)
        new_h = int(h_roi * scale_factor)

        resized = cv2.resize(roi, (new_w, new_h), interpolation=cv2.INTER_AREA)

        canvas = np.zeros((28, 28), dtype=np.uint8)
        x_c = (28 - new_w) // 2
        y_c = (28 - new_h) // 2
        canvas[y_c:y_c + new_h, x_c:x_c + new_w] = resized

        valid_samples.append(canvas)

    print(f"Found {len(valid_samples)} samples.")

    # SAVE
    save_dir = os.path.join(output_root, str(label))
    os.makedirs(save_dir, exist_ok=True)

    count = 0
    for sample in valid_samples:
        filename = f"{uuid.uuid4().hex[:8]}.png"
        cv2.imwrite(os.path.join(save_dir, filename), sample)
        count += 1

    print(f"Saved {count} clean examples to {save_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python scrape.py <image_path> <label>")
    else:
        scrape_sheet(sys.argv[1], sys.argv[2])