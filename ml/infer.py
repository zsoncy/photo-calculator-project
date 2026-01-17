import json, os
import numpy as np
import tensorflow as tf

_model = None
_label_map = None

def load_model(model_dir="ml/export/char_cnn", label_map_path="ml/label_map.json"):
    global _model, _label_map
    if _model is None:
        _model = tf.keras.models.load_model(model_dir)
        with open(label_map_path, "r", encoding="utf-8") as f:
            _label_map = {int(k): v for k, v in json.load(f).items()}

def predict_batch(images_28x28):
    load_model()  # idempotent
    arr = np.stack(images_28x28).astype("float32") / 255.0
    arr = arr[..., None]  # (N,28,28,1)
    probs = _model.predict(arr, verbose=0)
    idx = probs.argmax(axis=1)
    return [_label_map[int(i)] for i in idx]
