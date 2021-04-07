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
This file creates the model (model.h5) and class (classes.txt) files.
"""

from pathlib import Path
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from config import DOWNLOAD_PATH, MODEL_PATH, EPOCHS, IMG_SIZE


DATA_PATH = Path.joinpath(Path(DOWNLOAD_PATH), "frames")
MODEL_PATH = Path(MODEL_PATH)
MODEL_FILE = Path.joinpath(MODEL_PATH, "model.h5")
CLASS_FILE = Path.joinpath(MODEL_PATH, "classes.txt")

IMG_HEIGHT = IMG_SIZE["height"]
IMG_WIDTH = IMG_SIZE["width"]

"""Get all classes."""
CLASS_NAMES = [category.name for category in DATA_PATH.iterdir()]
NUM_CLASSES = len(CLASS_NAMES)

"""Save classes in a txt file."""
CLASS_FILE.touch()
classes = ""
for name in CLASS_NAMES:
    classes += str(name) + '\n'
CLASS_FILE.write_text(classes)


"""
GPU support fix.
https://github.com/tensorflow/tensorflow/issues/24828#issuecomment-464910864
"""
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)


def main():
    """Creates a model."""

    """Load the data."""
    trainData, valData = loadData(str(DATA_PATH))

    """Create and compile the model."""
    model = getModel()
    model.summary()

    """Fit the model and save the history."""
    history = model.fit(trainData, validation_data=valData, epochs=EPOCHS)

    """Save the model to a file."""
    model.save(str(MODEL_FILE))
    print("Model saved.")

    """Make loss and accuracy plots on the training and validation sets."""
    makePlots(history, EPOCHS)


def loadData(data_dir):
    """Loads the data. Returns tuple (`train_ds`, `val_ds`)."""

    """Training data."""
    train_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=16
    )

    """Validation data."""
    val_ds = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=16
    )

    """Configure the dataset for performance."""
    train_ds = train_ds.shuffle(250).prefetch(buffer_size=1)
    val_ds = val_ds.prefetch(buffer_size=1)

    return train_ds, val_ds


def getModel():
    """Creates and compiles neural network."""

    model = Sequential([
        layers.experimental.preprocessing.Rescaling(1./255, input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)),
        layers.Conv2D(128, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(64, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(32, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Conv2D(16, 3, padding='same', activation='relu'),
        layers.MaxPooling2D(),
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(NUM_CLASSES),
    ])

    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy']
    )

    return model


def makePlots(history, epochs):
    """Visualizes training results."""

    acc = history.history['accuracy']
    val_acc = history.history['val_accuracy']

    loss = history.history['loss']
    val_loss = history = history.history['val_loss']
    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))

    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, acc, label="Training Accuracy")
    plt.plot(epochs_range, val_acc, label="Validation Accuracy")
    plt.legend(loc="lower right")
    plt.title("Training and Validation Accuracy")

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label="Traing Loss")
    plt.plot(epochs_range, val_loss, label="Validation Loss")
    plt.legend(loc="upper right")
    plt.title("Training and Validation Loss")
    plt.show()


if __name__ == "__main__":
    main()
