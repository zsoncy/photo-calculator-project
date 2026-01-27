import tensorflow_datasets as tfds
import tensorflow as tf


def load_emnist_byclass(batch_size=128):
    ds_train, ds_test = tfds.load("emnist/digits", split=["train", "test"], as_supervised=True)
    def prep(x, y):
        x = tf.cast(x, tf.float32) / 255.0
        x = tf.transpose(x, perm=[1, 0, 2])
        x = tf.image.flip_left_right(x)
        return x, y
    ds_train = ds_train.map(prep, num_parallel_calls=tf.data.AUTOTUNE).shuffle(10000).batch(batch_size).prefetch(
        tf.data.AUTOTUNE)
    ds_test = ds_test.map(prep, num_parallel_calls=tf.data.AUTOTUNE).batch(batch_size).prefetch(tf.data.AUTOTUNE)
    return ds_train, ds_test