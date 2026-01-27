import json, os
import tensorflow as tf
from ml.model import build_cnn
from ml.data_emnist import load_emnist_byclass
from ml.data_symbols import load_symbols_from_folders

# ---- Configure your label space ----
# Example: digits + operators
USE_EMNIST = True
USE_SYMBOLS = True


DIGITS = [str(d) for d in range(10)]
# extend with operators and parentheses as class names
SYMBOLS = ["plus", "minus", "mul", "div", "eq", "lpar", "rpar"]
# Optional letters
LETTERS = []

def main():
    batch_size = 128
    epochs = 10

    # 1) Load datasets
    if USE_EMNIST:
        ds_train_emnist, ds_test_emnist = load_emnist_byclass(batch_size=batch_size)
        # These are 62 classes; we’ll remap later if needed.
    else:
        ds_train_emnist = ds_test_emnist = None

    if USE_SYMBOLS:
        ds_symbols, symbol_class_names = load_symbols_from_folders("data/symbols", (28,28), batch_size=64)
    else:
        ds_symbols = None
        symbol_class_names = []

    # Build unified label list
    label_map = {}

    # EMNIST digits only has 10 classes (0-9)
    # Map index 0 -> "0", index 1 -> "1", etc.
    for i in range(10):
        label_map[i] = str(i)

    # Append own symbols next.
    offset = 10
    for i, name in enumerate(symbol_class_names):
        label_map[offset + i] = name

    num_classes = len(label_map)

    # 3) Combine datasets
    # Simple way: if using EMNIST + symbols, concatenate after mapping labels into unified indices.
    # For brevity, we’ll train on EMNIST only if symbols are empty; otherwise, we interleave.
    def rename_symbols(ds, start_index):
        return ds.map(lambda x, y: (x, y + start_index), num_parallel_calls=tf.data.AUTOTUNE)

    if ds_symbols is not None:
        ds_symbols = rename_symbols(ds_symbols, start_index=offset).repeat()

    if ds_train_emnist is not None and ds_symbols is not None:
        ds_train = tf.data.Dataset.sample_from_datasets(
            [ds_train_emnist, ds_symbols],
            weights=[0.8, 0.2]
        ).prefetch(tf.data.AUTOTUNE)
        ds_val = ds_test_emnist
    elif ds_train_emnist is not None:
        ds_train = ds_train_emnist
        ds_val = ds_test_emnist
    else:
        ds_train = ds_symbols
        ds_val = ds_symbols.take(50)  # crude split if only symbols
        ds_train = ds_train.skip(50)

    # 4) Build & train model
    model = build_cnn(num_classes=num_classes, input_shape=(28,28,1))
    ckpt = tf.keras.callbacks.ModelCheckpoint(
        "ml/export/checkpoints/char_cnn.keras", save_best_only=True, monitor="val_accuracy", mode="max"
    )
    es = tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True, monitor="val_accuracy")

    model.fit(
        ds_train,
        validation_data=ds_val,
        epochs=10,
        steps_per_epoch=500,
        validation_steps=50,
        callbacks=[ckpt, es]
    )
    # 5) Export model & label map
    os.makedirs("ml/export/char_cnn", exist_ok=True)
    model.save("ml/export/char_cnn")
    with open("ml/label_map.json", "w", encoding="utf-8") as f:
        json.dump(label_map, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
