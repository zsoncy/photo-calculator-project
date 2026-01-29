import cv2
import numpy as np
from sympy import sympify, Symbol, solve, Eq, simplify, Poly
from ml import segment, infer

# Map model class names to real math symbols
MATH_MAP = {
    "plus": "+",
    "minus": "-",
    "mul": "*",
    "div": "/",
    "eq": "=",
    "lpar": "(",
    "rpar": ")",
    "x": "x"
}


def get_brain_output(binary_img):
    """
    1. Cuts characters from the binary image.
    2. Predicts them using the model.
    3. Converts to a string (e.g., "3x+5=10").
    4. Parses that string into a list format for Answer_Page.
    """

    # SEGMENTATION
    boxes = segment.find_char_boxes(binary_img)
    if not boxes:
        return ["Error"]

    # CUTTING IT OUT
    batch_images = []
    for box in boxes:
        char_img = segment.extract_28x28(binary_img, box)
        batch_images.append(char_img)

    # INFERENCE
    predictions = infer.predict_batch(batch_images)

    # TO STRING
    raw_equation = ""
    for p in predictions:
        token = MATH_MAP.get(p, p)
        raw_equation += token

    print(f"Raw output: {raw_equation}")

    # CONVERSION TO LIST
    return parse_to_list(raw_equation)


def parse_to_list(eq_str):
    """
    Converts raw string like "15x+9-3x=-2" into ["12", "11"]
    """
    try:
        eq_str = eq_str.lower().replace(" ", "")

        # Case 1: Simple Expression
        if "=" not in eq_str and "x" not in eq_str:
            return [eq_str]

        # SymPy
        x = Symbol('x')

        if "=" in eq_str:
            lhs_str, rhs_str = eq_str.split("=")
        else:
            lhs_str, rhs_str = eq_str, "0"

        lhs = sympify(lhs_str)
        rhs = sympify(rhs_str)
        expr = simplify(lhs - rhs)

        # Check if it's a polynomial in X
        poly = Poly(expr, x)
        degree = poly.degree()
        coeffs = poly.all_coeffs()  # Returns [a, b, c] highest to lowest

        # Convert coeffs to integer strings
        coeffs_str = [str(int(c)) for c in coeffs]

        # Case 2: Linear (Degree 1) -> Returns [a, b]
        if degree == 1:
            return coeffs_str  # [slope, intercept]

        # Case 3: Quadratic (Degree 2) -> Returns [a, b, c]
        elif degree == 2:
            return coeffs_str  # [a, b, c]

        # Case 4: Constant or higher order?
        else:
            return [str(expr)]

    except Exception as e:
        print(f"Parsing Error: {e}")
        return [eq_str]