import json, os
import numpy as np
import tensorflow as tf

_model = None
_label_map = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "export", "checkpoints", "char_cnn.keras")
LABEL_PATH = os.path.join(BASE_DIR, "label_map.json")

def load_model(model_dir = MODEL_PATH, label_map_path = LABEL_PATH):
    global _model, _label_map
    if _model is None:
        _model = tf.keras.models.load_model(model_dir)
        with open(label_map_path, "r", encoding="utf-8") as f:
            _label_map = {int(k): v for k, v in json.load(f).items()}

def predict_batch(images_28x28):
    load_model()
    arr = np.stack(images_28x28).astype("float32") / 255.0
    arr = arr[..., None]  # (N,28,28,1)
    probs = _model.predict(arr, verbose=0)
    idx = probs.argmax(axis=1)
    return [_label_map[int(i)] for i in idx]
