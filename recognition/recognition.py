import tensorflow as tf
from tensorflow import keras
import numpy as np

"""
GPU support fix.
https://github.com/tensorflow/tensorflow/issues/24828#issuecomment-464910864
"""
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

from config import DATA_PATH
IMG_HEIGHT = 180
IMG_WIDTH = 180

"""Get all classes."""
import pathlib
CLASS_NAMES = [category.name for category in pathlib.Path(DATA_PATH).iterdir()]


def main():

    path = "valorant.jpg"
    recognize(path)

def recognize(imgPath):
    """Recognize image class."""

    img = keras.preprocessing.image.load_img(
        imgPath, target_size=(IMG_HEIGHT, IMG_WIDTH)
    )
    img.show()

    img_array = keras.preprocessing.image.img_to_array(img)
    img_array = tf.expand_dims(img_array, 0)

    model = keras.models.load_model("../model/model.h5")

    predictions = model.predict(img_array)
    category = CLASS_NAMES[predictions.argmax()]
    probability = max(predictions[0])

    score = tf.nn.softmax(predictions[0])

    print(
        "This image most likely belongs to {} with a {:.2f}% confidence."
        .format(CLASS_NAMES[np.argmax(score)], 100 * np.max(score))
    )


if __name__ == "__main__":
    main()
