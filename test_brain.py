import json
import os
import numpy as np
import tensorflow as tf
import cv2


def create_missing_label_map():
    print("reconstructing label_map.json for DIGITS + SYMBOLS...")
    label_map = {}

    # EMNIST Digits (0-9)
    for i in range(10):
        label_map[i] = str(i)

    # Own Symbols (10+)
    symbol_dir = "data/symbols"
    if os.path.exists(symbol_dir):
        # Get folder names, sorted alphabetically
        symbol_names = sorted([d for d in os.listdir(symbol_dir) if os.path.isdir(os.path.join(symbol_dir, d))])

        offset = 10
        for i, name in enumerate(symbol_names):
            label_map[offset + i] = name
            print(f"Mapped Class {offset + i} -> {name}")

    # Save it
    with open("ml/label_map.json", "w", encoding="utf-8") as f:
        json.dump(label_map, f, indent=2)
    print("label_map.json created successfully!")
    return label_map

def draw_symbol(name):
    # Create a blank 28x28 black canvas
    img = np.zeros((28, 28), dtype=np.uint8)

    # Draw White symbols (EMNIST Style)
    if name == "minus":
        cv2.line(img, (6, 14), (22, 14), 255, 2)
    elif name == "plus":
        cv2.line(img, (14, 6), (14, 22), 255, 2)
        cv2.line(img, (6, 14), (22, 14), 255, 2)
    elif name == "mul":  # X shape
        cv2.line(img, (8, 8), (20, 20), 255, 2)
        cv2.line(img, (20, 8), (8, 20), 255, 2)
    elif name == "div":  # / shape (simple slash for now)
        cv2.line(img, (20, 6), (8, 22), 255, 2)
    elif name == "eq":
        cv2.line(img, (6, 10), (22, 10), 255, 2)
        cv2.line(img, (6, 18), (22, 18), 255, 2)

    return img


def test_all_symbols():
    model_path = "ml/export/checkpoints/char_cnn.keras"
    if not os.path.exists(model_path):
        model_path = "ml/export/char_cnn.keras"

    print(f"\nLoading Brain from: {model_path}")
    model = tf.keras.models.load_model(model_path)

    # Load dictionary
    with open("ml/label_map.json", "r") as f:
        labels = json.load(f)

    print("\nSYMBOL SCORECARD:")
    print("-" * 50)
    print(f"{'TEST SHAPE':<10} | {'PREDICTION':<15} | {'CONFIDENCE':<10} | {'STATUS'}")
    print("-" * 50)

    test_cases = ["plus", "minus", "mul", "div", "eq"]

    score = 0
    for shape in test_cases:
        # Generate Image
        img = draw_symbol(shape)

        # Prepare for the brain
        input_data = img.astype("float32") / 255.0
        input_data = np.expand_dims(input_data, axis=-1)
        input_data = np.expand_dims(input_data, axis=0)

        # Predict
        probs = model.predict(input_data, verbose=0)
        idx = np.argmax(probs)
        result_name = labels.get(str(idx), "Unknown")
        conf = probs[0][idx] * 100

        # Grade it
        status = "PASS" if result_name == shape else "FAIL"
        if status == "PASS": score += 1

        print(f"{shape:<10} | {result_name:<15} | {conf:.1f}%     | {status}")

    print("-" * 50)
    print(f"FINAL SCORE: {score}/{len(test_cases)}")


if __name__ == "__main__":
    create_missing_label_map()
    test_all_symbols()