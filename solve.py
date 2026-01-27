import cv2
import numpy as np
import os
import sys
from ml import segment, infer

# Mapping
MATH_MAP = {
    "plus": "+",
    "minus": "-",
    "mul": "*",
    "div": "/",
    "eq": "=",
    "lpar": "(",
    "rpar": ")"
}


def solve_image(image_path):
    print(f"\nOpening image: {image_path}")

    if not os.path.exists(image_path):
        print("Error: File not found.")
        return

    img = cv2.imread(image_path)

    # PREPROCESSING
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    bw = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # SEGMENTATION
    boxes = segment.find_char_boxes(bw)
    print(f"Found {len(boxes)} symbol(s).")

    if len(boxes) == 0:
        print("No characters found.")
        return

    # PREPARE BATCH for debug
    batch_images = []
    print(f"SAVING DEBUG IMAGES")

    for i, box in enumerate(boxes):
        char_img = segment.extract_28x28(bw, box)
        batch_images.append(char_img)

        # DEBUG
        debug_filename = f"debug_char_{i}.png"
        cv2.imwrite(debug_filename, char_img)
        print(f"   -> Saved {debug_filename}")




    # INFERENCE
    predictions = infer.predict_batch(batch_images)
    print(f"ML Raw Output: {predictions}")

    # CALCULATION
    # Convert words to symbols
    equation_str = ""
    for p in predictions:
        # If it's a digit (0-9), keep it. If it's a symbol, map it.
        token = MATH_MAP.get(p, p)
        equation_str += token

    print(f"Interpreted Equation: {equation_str}")

    # Try to calculate result
    try:
        # Clean up: remove '=' if present, as python eval() doesn't like it
        clean_eq = equation_str.replace("=", "")
        result = eval(clean_eq)
        print(f"RESULT: {result}")
        print("-" * 30)
        return result
    except Exception as e:
        print(f"Could not calculate: {e}")
        return None


if __name__ == "__main__":
    # run `python solve.py my_photo.png1`
    # if there is no first argument, it uses 'test_image.png' by default.
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        target_file = "test_image.png"

    solve_image(target_file)