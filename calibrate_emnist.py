import tensorflow as tf
import tensorflow_datasets as tfds
import cv2
import numpy as np


def main():
    print("Loading 5 random EMNIST samples...")
    ds = tfds.load("emnist/digits", split="train", as_supervised=True)
    ds = ds.take(5)  # 5 examples

    #  4 strips of images to test different fixes
    strip_1, strip_2, strip_3, strip_4 = [], [], [], []

    print("Generating variations...")

    for i, (img_tensor, label) in enumerate(ds):
        # Base conversion
        img = tf.cast(img_tensor, tf.float32) / 255.0

        # --- VARIATION 1: Transpose Only ---
        v1 = tf.transpose(img, perm=[1, 0, 2])

        # --- VARIATION 2: Transpose + Flip Left/Right ---
        v2 = tf.image.flip_left_right(v1)

        # --- VARIATION 3: Transpose + Flip Up/Down ---
        v3 = tf.image.flip_up_down(v1)

        # --- VARIATION 4: Raw (No Transpose) ---
        v4 = img

        # Convert helper
        def to_bgr(t):
            x = (t.numpy() * 255).astype(np.uint8)
            return cv2.cvtColor(x, cv2.COLOR_GRAY2BGR)

        strip_1.append(to_bgr(v1))
        strip_2.append(to_bgr(v2))
        strip_3.append(to_bgr(v3))
        strip_4.append(to_bgr(v4))

    # Stitch them into one big "Menu"
    def make_row(imgs, title):
        row = np.hstack(imgs)
        # Add a black border to write text
        canvas = np.zeros((50 + 28, row.shape[1], 3), dtype=np.uint8)
        canvas[50:, :] = row
        cv2.putText(canvas, title, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        return canvas

    final_img = np.vstack([
        make_row(strip_1, "1. Transpose Only"),
        make_row(strip_2, "2. Transpose + Flip LR"),
        make_row(strip_3, "3. Transpose + Flip UD"),
        make_row(strip_4, "4. Raw (No Fix)")
    ])

    cv2.imwrite("debug_calibration.png", final_img)
    print("Generated 'debug_calibration.png'. Open it and see which row is readable!")


if __name__ == "__main__":
    main()