import os
import tensorflow as tf
import tensorflow_datasets as tfds
import numpy as np
import json
from glob import glob
from ml.model import build_cnn

# --- CONFIGURATION ---
BATCH_SIZE = 64
EPOCHS = 15
CLASS_NAMES = [
    "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    "div", "eq", "lpar", "minus", "mul", "plus", "rpar"
]


def get_label_id(folder_name):
    """Maps a folder name (e.g. 'plus') to its ID (e.g. 15)."""
    try:
        return CLASS_NAMES.index(folder_name)
    except ValueError:
        return None


def load_local_images(root_dirs):
    """
    Scans multiple folders (custom_data, symbols) and collects all image paths.
    Returns: (file_paths, labels)
    """
    all_paths = []
    all_labels = []

    print(f"📂 Scanning local folders: {root_dirs}")

    for root in root_dirs:
        if not os.path.exists(root):
            print(f"⚠️ Warning: Folder not found: {root}")
            continue

        subfolders = os.listdir(root)
        for folder in subfolders:
            folder_path = os.path.join(root, folder)
            if not os.path.isdir(folder_path):
                continue

            label_id = get_label_id(folder)
            if label_id is None:
                continue

            # Find images
            extensions = ["*.png", "*.jpg", "*.jpeg"]
            files = []
            for ext in extensions:
                files.extend(glob(os.path.join(folder_path, ext)))

            print(f"   -> Found {len(files)} images for class '{folder}' in {root}")

            all_paths.extend(files)
            all_labels.extend([label_id] * len(files))

    return all_paths, all_labels


def preprocess_image(path, label):
    """Loads and processes a local image file."""
    img = tf.io.read_file(path)

    # Force TF to see this as an image (not GIF), and force Grayscale
    img = tf.image.decode_image(img, channels=1, expand_animations=False)

    # Explicitly set shape so 'resize' works
    img.set_shape([None, None, 1])

    img = tf.image.resize(img, [28, 28])
    img = tf.cast(img, tf.float32) / 255.0

    # Ensure label is int64 (redundant but safe)
    label = tf.cast(label, tf.int64)

    return img, label


def load_emnist():
    """Loads the official EMNIST digits dataset."""
    print("📥 Loading EMNIST Digits...")
    ds, info = tfds.load("emnist/digits", split="train", with_info=True, as_supervised=True)

    def prep_emnist(img, label):
        # EMNIST needs rotation and flipping to match standard images
        img = tf.cast(img, tf.float32) / 255.0
        img = tf.transpose(img, perm=[1, 0, 2])
        img = tf.image.flip_left_right(img)
        return img, label

    return ds.map(prep_emnist, num_parallel_calls=tf.data.AUTOTUNE)


def main():
    # 1. LOAD LOCAL DATA
    local_dirs = ["data/custom_data", "data/symbols"]
    paths, labels = load_local_images(local_dirs)

    if len(paths) == 0:
        print("❌ Error: No local images found! Check your folders.")
        return

    # --- CRITICAL FIX: FORCE INT64 TYPE ---
    # Convert standard Python list to NumPy int64 array.
    # This prevents the "Incompatible dataset elements" error.
    labels = np.array(labels, dtype=np.int64)
    # --------------------------------------

    # Create TensorFlow Dataset
    ds_local = tf.data.Dataset.from_tensor_slices((paths, labels))
    ds_local = ds_local.map(preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)

    # 2. LOAD EMNIST
    ds_emnist = load_emnist()

    # 3. BALANCE THE DATASETS
    num_local = len(paths)
    print(f"📊 Total Local Images: {num_local}")

    # Repeat local data heavily so the model sees it as often as EMNIST
    ds_local = ds_local.shuffle(10000).repeat(100)

    # 4. MERGE
    print("🔗 Merging datasets...")
    # Now both datasets have int64 labels, so this will work!
    ds_train = ds_emnist.concatenate(ds_local)
    ds_train = ds_train.shuffle(50000).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    # 5. BUILD & TRAIN
    print(f"🧠 Building Model for {len(CLASS_NAMES)} classes...")
    model = build_cnn(num_classes=len(CLASS_NAMES))

    # Train
    model.fit(ds_train, epochs=EPOCHS, steps_per_epoch=1000)

    # 6. SAVE EVERYTHING
    output_dir = "ml/export/checkpoints"
    os.makedirs(output_dir, exist_ok=True)

    model_path = os.path.join(output_dir, "char_cnn.keras")
    model.save(model_path)
    print(f"✅ Model saved to {model_path}")

    # Save the label map
    label_map = {i: name for i, name in enumerate(CLASS_NAMES)}
    with open("ml/label_map.json", "w") as f:
        json.dump(label_map, f, indent=2)
    print("✅ label_map.json updated.")


if __name__ == "__main__":
    main()