import cv2
import numpy as np
import os
import random
import shutil

# Configuration
OUTPUT_DIR = "data/symbols"
CLASSES = ["plus", "minus", "mul", "div", "eq", "lpar", "rpar"]
NUM_SAMPLES = 100  # How many images per symbol
IMG_SIZE = 28


def create_canvas():
    # solid black background
    return np.zeros((IMG_SIZE, IMG_SIZE), dtype=np.uint8)


def draw_plus(img, thickness):
    center = IMG_SIZE // 2
    length = random.randint(8, 10)
    # Horizontal
    cv2.line(img, (center - length, center), (center + length, center), 255, thickness)
    # Vertical
    cv2.line(img, (center, center - length), (center, center + length), 255, thickness)


def draw_minus(img, thickness):
    center = IMG_SIZE // 2
    length = random.randint(8, 10)
    cv2.line(img, (center - length, center), (center + length, center), 255, thickness)


def draw_mul(img, thickness):
    center = IMG_SIZE // 2
    length = random.randint(7, 9)
    # Diagonal 1
    cv2.line(img, (center - length, center - length), (center + length, center + length), 255, thickness)
    # Diagonal 2
    cv2.line(img, (center + length, center - length), (center - length, center + length), 255, thickness)


def draw_div(img, thickness):
    center = IMG_SIZE // 2
    length = random.randint(7, 9)
    # Slash
    cv2.line(img, (center + length, center - length), (center - length, center + length), 255, thickness)


def draw_eq(img, thickness):
    center = IMG_SIZE // 2
    length = random.randint(8, 10)
    gap = 4
    cv2.line(img, (center - length, center - gap), (center + length, center - gap), 255, thickness)
    cv2.line(img, (center - length, center + gap), (center + length, center + gap), 255, thickness)


def draw_lpar(img, thickness):
    # Curve approximation
    center = IMG_SIZE // 2
    cv2.ellipse(img, (center + 5, center), (4, 10), 0, 90, 270, 255, thickness)


def draw_rpar(img, thickness):
    center = IMG_SIZE // 2
    cv2.ellipse(img, (center - 5, center), (4, 10), 0, -90, 90, 255, thickness)


def main():
    # 1. Clean old folder
    if os.path.exists(OUTPUT_DIR):
        print(f"Cleaning old data in {OUTPUT_DIR}...")
        shutil.rmtree(OUTPUT_DIR)

    # 2. Generate new data
    for category in CLASSES:
        folder_path = os.path.join(OUTPUT_DIR, category)
        os.makedirs(folder_path, exist_ok=True)
        print(f"Generating {category}...")

        for i in range(NUM_SAMPLES):
            img = create_canvas()

            # Randomize thickness slightly (2 or 3 pixels)
            thick = random.choice([2, 3])

            # Draw based on category
            if category == "plus":
                draw_plus(img, thick)
            elif category == "minus":
                draw_minus(img, thick)
            elif category == "mul":
                draw_mul(img, thick)
            elif category == "div":
                draw_div(img, thick)
            elif category == "eq":
                draw_eq(img, thick)
            elif category == "lpar":
                draw_lpar(img, thick)
            elif category == "rpar":
                draw_rpar(img, thick)

            # Save
            filename = f"{folder_path}/{category}_{i:04d}.png"
            cv2.imwrite(filename, img)

    print("\nDONE! Perfect synthetic symbols generated.")
    print("Now your symbols are exactly 28x28, White-on-Black, and THICK.")


if __name__ == "__main__":
    main()