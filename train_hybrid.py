import os
import shutil
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
    "div", "eq", "lpar", "minus", "mul", "plus", "rpar", "x"
]

def get_label_id(folder_name):
    try:
        return CLASS_NAMES.index(folder_name)
    except ValueError:
        return None

def load_local_images(root_dirs):
    all_paths = []
    all_labels = []

    print(f"Scanning local folders: {root_dirs}")

    for root in root_dirs:
        if not os.path.exists(root): continue

        subfolders = os.listdir(root)
        for folder in subfolders:
            folder_path = os.path.join(root, folder)
            if not os.path.isdir(folder_path): continue

            label_id = get_label_id(folder)
            if label_id is None: continue

            extensions = ["*.png", "*.jpg", "*.jpeg"]
            files = []
            for ext in extensions:
                files.extend(glob(os.path.join(folder_path, ext)))

            print(f"   -> Found {len(files)} images for class '{folder}'")
            all_paths.extend(files)
            all_labels.extend([label_id] * len(files))

    return all_paths, all_labels


def preprocess_image(path, label):
    img = tf.io.read_file(path)
    img = tf.image.decode_image(img, channels=1, expand_animations=False)
    img.set_shape([None, None, 1])
    img = tf.image.resize(img, [28, 28])
    img = tf.cast(img, tf.float32) / 255.0
    label = tf.cast(label, tf.int64)
    return img, label


def load_emnist():
    print("Loading EMNIST Digits...")
    ds = tfds.load("emnist/digits", split="train", as_supervised=True)

    def prep_emnist(img, label):
        img = tf.cast(img, tf.float32) / 255.0
        # Transpose ONLY
        img = tf.transpose(img, perm=[1, 0, 2])
        return img, label

    return ds.map(prep_emnist, num_parallel_calls=tf.data.AUTOTUNE)

def main():

    checkpoints_dir = "ml/export/checkpoints"
    if os.path.exists(checkpoints_dir):
        print("Deleting old corrupted brain...")
        shutil.rmtree(checkpoints_dir)

    # LOAD LOCAL DATA
    local_dirs = ["data/custom_data", "data/symbols"]
    paths, labels = load_local_images(local_dirs)

    if len(paths) == 0:
        print("Error: No local images found!")
        return

    labels = np.array(labels, dtype=np.int64)
    ds_local = tf.data.Dataset.from_tensor_slices((paths, labels))
    ds_local = ds_local.map(preprocess_image, num_parallel_calls=tf.data.AUTOTUNE)

    # LOAD EMNIST
    ds_emnist = load_emnist()

    # OVER-WEIGHT OWN DATA
    ds_local = ds_local.shuffle(5000).repeat(100)

    # MERGE
    print("🔗 Merging datasets...")
    ds_train = ds_emnist.concatenate(ds_local)
    ds_train = ds_train.shuffle(50000).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

    # BUILD & TRAIN
    print(f"Building Model for {len(CLASS_NAMES)} classes...")
    model = build_cnn(num_classes=len(CLASS_NAMES))
    model.fit(ds_train, epochs=EPOCHS, steps_per_epoch=1000)

    # SAVE
    os.makedirs(checkpoints_dir, exist_ok=True)
    model.save(os.path.join(checkpoints_dir, "char_cnn.keras"))
    print(f"Model saved to {checkpoints_dir}")

    label_map = {i: name for i, name in enumerate(CLASS_NAMES)}
    with open("ml/label_map.json", "w") as f:
        json.dump(label_map, f, indent=2)

if __name__ == "__main__":
    main()