"""
MIT License

Copyright (c) 2021 molokhovdmitry

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
This file downloads specified stream frames, loads them into a model
and predicts the game.
"""

import sys
import numpy as np
from pathlib import Path

import tensorflow as tf
from tensorflow import keras
from streamlink import Streamlink
import requests

from data.downloadFuncs import downloadFrames, delTempFiles
from data.api import gameIDtoName
from data.dbFuncs import gameIDtoName as dbGameIDtoName, sessionScope

from config import MODEL_PATH, IMG_SIZE


MODEL_PATH = Path(MODEL_PATH)
MODEL_FILE = Path.joinpath(MODEL_PATH, "model.h5")
CLASS_FILE = Path.joinpath(MODEL_PATH, "classes.txt")

IMG_HEIGHT = IMG_SIZE["height"]
IMG_WIDTH = IMG_SIZE["width"]

"""Get all classes."""
CLASS_NAMES = []
with CLASS_FILE.open() as f:
    for line in f.readlines():
        CLASS_NAMES.append(int(line))


"""
GPU support fix.
https://github.com/tensorflow/tensorflow/issues/24828#issuecomment-464910864
"""
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)


def recognize(login):
    """Recognize stream game by frames."""

    """Create streamlink and api sessions."""
    streamlinkSession = Streamlink()
    apiSession = requests.session()
    
    """Load the model."""
    model = keras.models.load_model(str(MODEL_FILE))

    """Recognize frames."""
    frames = list(downloadFrames(streamlinkSession, login))
    if not frames:
        print("Couldn't download stream frames.")
        return None
    scores = [recognizeFrame(apiSession, model, frame) for frame in frames]

    """Delete downloaded frames."""
    delTempFiles()

    """Add tensors."""
    scores = np.add.reduce(scores)[0]

    """Calculate score for a stream."""
    score = np.max(scores) / len(frames)

    """Get game ID."""
    index = np.argmax(scores)
    gameID = CLASS_NAMES[index]

    """Get game name from game ID."""
    game = gameIDtoName(apiSession, gameID)

    print("{} with a score of {:.1f}".format(game, score))

    return game, score


def recognizeFrame(apiSession, model, imgPath):
    """Recognize image class."""

    """Load and resize the image."""
    img = keras.preprocessing.image.load_img(
        imgPath, target_size=(IMG_HEIGHT, IMG_WIDTH)
    )

    """Convert the image to an array."""
    imgArray = keras.preprocessing.image.img_to_array(img)
    imgArray = tf.expand_dims(imgArray, 0)

    """Predict the game."""
    predictions = model(imgArray)

    """Calculate game score for an image."""
    score = tf.nn.softmax(predictions[0])

    """Print a prediction for an image."""
    print(
        "{} with a {:.2f}% confidence."
        .format(gameIDtoName(apiSession, CLASS_NAMES[np.argmax(score)]),
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