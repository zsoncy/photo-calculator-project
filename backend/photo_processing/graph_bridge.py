import cv2
import numpy as np
import re
from sympy import sympify, Symbol, Poly
from ml import segment, infer

# Mapping
MATH_MAP = {
    "plus": "+", "minus": "-", "mul": "*", "div": "/",
    "eq": "=", "lpar": "(", "rpar": ")", "x": "x", "X": "x"
}


def analyze_for_graph(binary_image):

    if binary_image is None:
        return "Error", []

    # 1. DILATION
    bw_inv = 255 - binary_image
    kernel = np.ones((5, 5), np.uint8)
    bw_fat = cv2.dilate(bw_inv, kernel, iterations=4)
    bw_fat_inv = 255 - bw_fat

    # 2. SEGMENTATION
    boxes = segment.find_char_boxes(bw_fat_inv)
    if not boxes:
        return "Error", []

    batch_images = []
    for box in boxes:
        char_img = segment.extract_28x28(binary_image, box)
        batch_images.append(char_img)

    predictions = infer.predict_batch(batch_images)

    # BUILD STRING
    raw_eq = ""
    for p in predictions:
        token = MATH_MAP.get(p, p)
        raw_eq += token

    # HEALER
    clean_eq = raw_eq.replace("---", "=").replace("--", "=")
    clean_eq = re.sub(r"x(\d)", r"x^\1", clean_eq)  # x2 -> x^2
    clean_eq = re.sub(r"(\d)x", r"\1*x", clean_eq)  # 3x -> 3*x

    # EXTRACT COEFFICIENTS
    try:
        # Convert to lower case
        eq_str = clean_eq.lower().replace(" ", "")

        if "=" in eq_str:
            parts = eq_str.split("=")
            eq_str = max(parts, key=len)

        x = Symbol('x')
        expr = sympify(eq_str)

        # Get polynomial coefficients (highest power first)
        # 3*x^2 + 1 -> [3, 0, 1]
        poly = Poly(expr, x)
        coeffs = poly.all_coeffs()

        # Convert to strings
        coeffs_str = [str(int(c)) for c in coeffs]

        return clean_eq, coeffs_str

    except Exception as e:
        print(f"Graph Parse Error: {e}")
        return clean_eq, []