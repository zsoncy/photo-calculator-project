import cv2
import numpy as np
import os
import sys
import re
from sympy import sympify, Symbol, simplify, Poly, solve, Eq
from ml import segment, infer

# Mapping
MATH_MAP = {
    "plus": "+", "minus": "-", "mul": "*", "div": "/",
    "eq": "=", "lpar": "(", "rpar": ")", "x": "x", "X": "x"
}


def solve_image(image_path):
    print(f"\nOpening image: {image_path}")

    if not os.path.exists(image_path):
        print("Error: File not found.")
        return

    # 1. PREPROCESSING
    img = cv2.imread(image_path)
    h, w = img.shape[:2]

    target_h = 1000
    scale = target_h / h
    img = cv2.resize(img, (int(w * scale), target_h))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    bw = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 41, 15
    )

    # Invert
    bw_inv = 255 - bw

    # Adds pixels to connect everything.
    kernel = np.ones((5, 5), np.uint8)
    bw_fat = cv2.dilate(bw_inv, kernel, iterations=4)

    # Invert back to Black-Text-on-White
    bw_fat_inv = 255 - bw_fat

    # 3. SEGMENTATION
    boxes = segment.find_char_boxes(bw_fat_inv)

    print(f"Found {len(boxes)} symbol(s).")

    if len(boxes) == 0:
        print("No characters found.")
        return

    # DEBUG
    debug_img = img.copy()
    for box in boxes:
        x, y, w, h = box
        cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 0, 255), 3)

    cv2.imwrite("debug_red_boxes.png", debug_img)
    print("Saved 'debug_red_boxes.png'")

    # 4. EXTRACTION & INFERENCE
    batch_images = []

    # Original Clean BW image for extraction
    bw_clean_for_ai = bw

    for box in boxes:
        char_img = segment.extract_28x28(bw_clean_for_ai, box)
        batch_images.append(char_img)

    predictions = infer.predict_batch(batch_images)
    print(f"Raw Classes: {predictions}")

    # 5. BUILD STRING
    raw_eq = ""
    for p in predictions:
        token = MATH_MAP.get(p, p)
        raw_eq += token

    print(f"Raw Equation: {raw_eq}")

    # 6. HEALER
    clean_eq = raw_eq.replace("---", "=").replace("--", "=")
    clean_eq = re.sub(r"x(\d)", r"x^\1", clean_eq)

    print(f"Healed Equation: {clean_eq}")

    # 7. SOLVER
    try:
        eq_str = clean_eq.lower().replace(" ", "")
        if "x" not in eq_str and "=" not in eq_str:
            print(f"Result: {eval(eq_str)}")
            return

        x = Symbol('x')
        if "=" in eq_str:
            lhs_str, rhs_str = eq_str.split("=")
        else:
            lhs_str, rhs_str = eq_str, "0"

        lhs = sympify(lhs_str)
        rhs = sympify(rhs_str)
        expression = simplify(lhs - rhs)

        poly = Poly(expression, x)
        coeffs = poly.all_coeffs()
        print(f"Coefficients: {[str(int(c)) for c in coeffs]}")

        solution = solve(expression, x)
        print(f"Solution: x = {solution}")

    except Exception as e:
        print(f"Math Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        target_file = "test_image_7.png"

    solve_image(target_file)