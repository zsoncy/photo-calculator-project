import tensorflow as tf
import tensorflow_datasets as tfds
import cv2
import numpy as np


def main():
    print("📥 Downloading/Loading EMNIST sample...")
    ds = tfds.load("emnist/digits", split="train", as_supervised=True)

    # Take 20 images
    ds = ds.take(20)

    print("📸 Processing images with CURRENT logic...")

    images = []
    for i, (img, label) in enumerate(ds):
        # --- THIS IS THE LOGIC FROM YOUR TRAIN SCRIPT ---
        img = tf.cast(img, tf.float32) / 255.0
        img = tf.transpose(img, perm=[1, 0, 2])
        # -----------------------------------------------

        # Convert back to regular image for us to see
        img_np = (img.numpy() * 255).astype(np.uint8)
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_GRAY2BGR)

        # Add Label text
        lbl_text = str(label.numpy())
        cv2.putText(img_bgr, lbl_text, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        images.append(img_bgr)

    # Stitch them together
    row1 = np.hstack(images[:10])
    row2 = np.hstack(images[10:])
    grid = np.vstack([row1, row2])

    cv2.imwrite("debug_emnist_check.png", grid)
    print("✅ Saved 'debug_emnist_check.png'. OPEN IT NOW!")
    print("If the numbers look BACKWARDS (mirrored), delete the 'flip_left_right' line in train_hybrid.py")


if __name__ == "__main__":
    main()