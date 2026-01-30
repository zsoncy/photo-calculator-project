import cv2
import numpy as np
import re
from sympy import sympify, Symbol, simplify, Poly, solve, Eq
from ml import segment, infer

# Mapping
MATH_MAP = {
    "plus": "+", "minus": "-", "mul": "*", "div": "/",
    "eq": "=", "lpar": "(", "rpar": ")", "x": "x", "X": "x"
}


def analyze_image(binary_image):
    """
    1. Applies 'Nuclear Glue' (Dilation) to merge broken symbols (x, =, +).
    2. Uses those merged blobs to find bounding boxes.
    3. Cuts the characters from the original sharp image.
    4. Runs Model + Math Logic.
    """

    # 1. DILATION
    if binary_image is None:
        return ["Error: No Image"]

    # Inverting
    bw_inv = 255 - binary_image

    # Expand text by ~20 pixels to merge split strokes
    kernel = np.ones((5, 5), np.uint8)
    bw_fat = cv2.dilate(bw_inv, kernel, iterations=4)

    # Invert back for segment.py
    bw_fat_inv = 255 - bw_fat

    # 2. SEGMENTATION
    boxes = segment.find_char_boxes(bw_fat_inv)

    if not boxes:
        return ["Error: Empty"]

    # 3. EXTRACTION
    # extract from the ORIGINAL sharp binary_image, given the location from the dilated one.
    batch_images = []
    for box in boxes:
        char_img = segment.extract_28x28(binary_image, box)
        batch_images.append(char_img)

    # 4. MODEL + MATH
    # PREDICTION
    predictions = infer.predict_batch(batch_images)

    # BUILD STRING
    raw_eq = ""
    for p in predictions:
        token = MATH_MAP.get(p, p)
        raw_eq += token

    print(f"Model natural Output: {raw_eq}")

    # HEALER
    clean_eq = raw_eq.replace("--", "=")
    clean_eq = re.sub(r"x(\d)", r"x^\1", clean_eq)
    clean_eq = re.sub(r"(\d)x", r"\1*x", clean_eq)

    print(f"Final processed equation: {clean_eq}")

    # 7. PARSE TO LIST
    return clean_eq, parse_equation_to_list(clean_eq)


def parse_equation_to_list(eq_str):
    try:
        eq_str = eq_str.lower().replace(" ", "")

        # Simple Expression
        if "x" not in eq_str and "=" not in eq_str:
            return [eq_str]

        # SymPy - Algebra
        x = Symbol('x')
        if "=" in eq_str:
            left_str, right_str = eq_str.split("=")
        else:
            left_str, right_str = eq_str, "0"

        left_str = sympify(left_str)
        right_str = sympify(right_str)
        expression = simplify(left_str - right_str)

        poly = Poly(expression, x)
        # LIST OF SYMPY NUMBERS: for ex:  [Integer(3), Integer(-9), Integer(1)]
        coeffs = poly.all_coeffs()

        return [str(int(c)) for c in coeffs]

    except Exception as e:
        print(f"Parsing Failed: {e}")
        return [eq_str]