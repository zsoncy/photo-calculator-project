from tensorflow import keras
from tensorflow.keras import layers

def build_cnn(num_classes: int, input_shape=(28, 28, 1)) -> keras.Model:
    inputs = keras.Input(shape=input_shape, name="image")
    x = layers.Conv2D(32, 3, activation="relu")(inputs)
    x = layers.Conv2D(32, 3, activation="relu")(x)
    x = layers.MaxPool2D()(x)
    x = layers.Dropout(0.25)(x)

    x = layers.Conv2D(64, 3, activation="relu")(x)
    x = layers.Conv2D(64, 3, activation="relu")(x)
    x = layers.MaxPool2D()(x)
    x = layers.Dropout(0.25)(x)

    x = layers.Flatten()(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="probs")(x)

    model = keras.Model(inputs, outputs, name="char_cnn")
    model.compile(
        optimizer=keras.optimizers.Adam(1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model
