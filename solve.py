import cv2
import numpy as np
import os
import sys
from sympy import sympify, Symbol, solve, simplify, Eq
from ml import segment, infer

# Mapping (Ensure your 'x' folder name matches the key here)
MATH_MAP = {
    "plus": "+",
    "minus": "-",
    "mul": "*",
    "div": "/",
    "eq": "=",
    "lpar": "(",
    "rpar": ")",
    "x": "x",
    "X": "x"
}


def solve_image(image_path):
    print(f"\nOpening image: {image_path}")

    if not os.path.exists(image_path):
        print("Error: File not found.")
        return

    # 1. READ & PREPROCESS
    img = cv2.imread(image_path)

    # Resize to standard height (matches your App logic)
    h, w = img.shape[:2]
    target_h = 1000
    scale = target_h / h
    img = cv2.resize(img, (int(w * scale), target_h))

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    bw = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 41, 15
    )

    # Clean noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    bw = cv2.morphologyEx(bw, cv2.MORPH_OPEN, kernel)

    # 2. SEGMENTATION
    boxes = segment.find_char_boxes(bw)
    print(f"Found {len(boxes)} symbol(s).")

    if len(boxes) == 0:
        print("No characters found.")
        return

    # 3. EXTRACTION
    batch_images = []
    for i, box in enumerate(boxes):
        char_img = segment.extract_28x28(bw, box)
        batch_images.append(char_img)
        # Optional: Save debug images
        # cv2.imwrite(f"debug_char_{i}.png", char_img)

    # 4. INFERENCE
    predictions = infer.predict_batch(batch_images)
    print(f"Raw Classes: {predictions}")

    # 5. STRING CONSTRUCTION
    equation_str = ""
    for p in predictions:
        token = MATH_MAP.get(p, p)
        equation_str += token

    print(f"Equation: {equation_str}")
    print("-" * 30)

    # 6. SOLVER (Algebra Support)
    try:
        # Case A: Simple Math (2+2)
        if "x" not in equation_str and "=" not in equation_str:
            result = eval(equation_str)
            print(f"RESULT: {result}")
            return

        # Case B: Algebra (3x + 5 = 10)
        x = Symbol('x')

        # Split into Left and Right sides
        if "=" in equation_str:
            lhs_str, rhs_str = equation_str.split("=")
        else:
            lhs_str, rhs_str = equation_str, "0"

        # Sympy Solve
        lhs = sympify(lhs_str)
        rhs = sympify(rhs_str)
        equation = Eq(lhs, rhs)

        solution = solve(equation, x)

        print(f"ALGEBRA SOLUTION: x = {solution}")

    except Exception as e:
        print(f"Could not solve: {e}")
        print("(Did you detect a symbol incorrectly?)")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        target_file = "test_image.png"

    solve_image(target_file)