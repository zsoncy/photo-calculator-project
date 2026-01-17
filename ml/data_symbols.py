import tensorflow as tf
import pathlib

# data/symbols/<class_name>/*.png
def load_symbols_from_folders(root="data/symbols", img_size=(28,28), batch_size=64):
    root = pathlib.Path(root)
    ds = tf.keras.preprocessing.image_dataset_from_directory(
        root, labels="inferred", label_mode="int", color_mode="grayscale",
        image_size=img_size, batch_size=batch_size, shuffle=True
    )
    # Normalize & ensure (28,28,1)
    def prep(x, y):
        x = tf.cast(x, tf.float32) / 255.0
        return x, y
    ds = ds.map(prep, num_parallel_calls=tf.data.AUTOTUNE)
    class_names = ds.class_names  # folder order
    return ds, class_names
