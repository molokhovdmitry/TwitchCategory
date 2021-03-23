"""
This file downloads specified stream frames, loads them into a model
and predicts the game.
"""

import sys
import numpy as np
import os

import tensorflow as tf
from tensorflow import keras

from data.download import downloadFrames, delTempFiles
from data.api import gameIDtoName
from data.dbFuncs import gameIDtoName as dbGameIDtoName, sessionScope

"""
GPU support fix.
https://github.com/tensorflow/tensorflow/issues/24828#issuecomment-464910864
"""
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)


from config import DOWNLOAD_PATH
DATA_PATH = DOWNLOAD_PATH + "frames"
IMG_HEIGHT = 180
IMG_WIDTH = 180

"""Get all classes."""
import pathlib
CLASS_NAMES = [category.name for category in pathlib.Path(DATA_PATH).iterdir()]


def recognize(login):
    """Recognize stream game by frames."""

    """Recognize frames."""
    frames = list(downloadFrames(login))
    if not frames:
        sys.exit()
    scores = [recognizeFrame(frame) for frame in frames]

    """Delete frames."""
    delTempFiles()

    """Add tensors."""
    scores = np.add.reduce(scores)[0]

    """Calculate score for a stream."""
    score = np.max(scores)

    """Get game ID."""
    index = np.argmax(scores)
    gameID = CLASS_NAMES[index]

    """Get game name from game ID."""
    game = gameIDtoName(gameID)

    print(f"{game} with a score of {score}")
    return game


def recognizeFrame(imgPath):
    """Recognize image class."""

    """Load and resize the image."""
    img = keras.preprocessing.image.load_img(
        imgPath, target_size=(IMG_HEIGHT, IMG_WIDTH)
    )

    """Convert the image to an array."""
    imgArray = keras.preprocessing.image.img_to_array(img)
    imgArray = tf.expand_dims(imgArray, 0)

    """Load the model."""
    model = keras.models.load_model(f"model{os.sep}model.h5")

    """Predict the game."""
    predictions = model(imgArray)

    """Calculate game score for an image."""
    score = tf.nn.softmax(predictions[0])

    """Print a prediction for an image."""
    print(
        "{} most likely belongs to {} with a {:.2f}% confidence."
        .format(imgPath,
                gameIDtoName(CLASS_NAMES[np.argmax(score)]),
                100 * np.max(score))
    )

    return predictions

if __name__ == "__main__":

    """Check command arguments."""
    if len(sys.argv) != 2:
        print("Usage: python -m recognition.recognition login")
        sys.exit()

    login = sys.argv[1]
    recognize(login)
