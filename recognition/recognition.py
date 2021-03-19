"""
This file downloads specified stream and predicts the game.
"""

import sys
import numpy as np

import tensorflow as tf
from tensorflow import keras

from data.download import downloadFrames, delTempFiles
from data.dbFuncs import gameIDtoName as dbGameIDtoName, sessionScope
from data.api import gameIDtoName as apiGameIDtoName

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


def recognize(login):

    """Recognize frames."""
    frames = list(downloadFrames(login))
    if not frames:
        sys.exit()
    scores = [recognizeFrame(frame) for frame in frames]

    """Delete frames."""
    delTempFiles()

    """Add tensors."""
    scores = np.add.reduce(scores)[0]

    """Calculate score."""
    score = np.max(scores)

    """Get game ID."""
    index = np.argmax(scores)
    gameID = CLASS_NAMES[index]

    """Get game name from game ID."""
    game = apiGameIDtoName(gameID)
    print(game)
    print(score)


def recognizeFrame(imgPath):
    """Recognize image class."""

    img = keras.preprocessing.image.load_img(
        imgPath, target_size=(IMG_HEIGHT, IMG_WIDTH)
    )

    imgArray = keras.preprocessing.image.img_to_array(img)
    imgArray = tf.expand_dims(imgArray, 0)

    model = keras.models.load_model("model/model.h5")

    predictions = model(imgArray)
    score = tf.nn.softmax(predictions[0])

    print(
        "This image most likely belongs to {} with a {:.2f}% confidence."
        .format(CLASS_NAMES[np.argmax(score)], 100 * np.max(score))
    )

    return predictions

if __name__ == "__main__":

    """Check command arguments."""
    if len(sys.argv) != 2:
        print("Usage: python -m recognition.recognition login")
        sys.exit()

    login = sys.argv[1]
    recognize(login)
