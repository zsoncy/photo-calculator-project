import tensorflow_datasets as tfds
import tensorflow as tf

# pick a split: 'byclass' or 'balanced'
def load_emnist_byclass(batch_size=128):
    ds_train, ds_test = tfds.load("emnist/byclass", split=["train", "test"], as_supervised=True)
    # EMNIST images are 28x28 grayscale; normalize to [0,1], ensure shape (28,28,1)
    def prep(x, y):
        x = tf.cast(x, tf.float32) / 255.0
        x = tf.expand_dims(x, -1)  # (H,W,1)
        # EMNIST is rotated/transposed; fix orientation (official quirk)
        x = tf.transpose(x, perm=[1, 0, 2])     # swap axes
        x = tf.image.flip_left_right(x)         # horizontal flip
        return x, y
    ds_train = ds_train.map(prep, num_parallel_calls=tf.data.AUTOTUNE).shuffle(10000).batch(batch_size).prefetch(tf.data.AUTOTUNE)
    ds_test = ds_test.map(prep, num_parallel_calls=tf.data.AUTOTUNE).batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return ds_train, ds_test
