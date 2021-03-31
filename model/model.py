"""
This file creates the model.
"""

import pathlib
import matplotlib.pyplot as plt

import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

"""
GPU support fix.
https://github.com/tensorflow/tensorflow/issues/24828#issuecomment-464910864
"""
config = tf.compat.v1.ConfigProto()
config.gpu_options.allow_growth = True
session = tf.compat.v1.Session(config=config)

from config import DOWNLOAD_PATH
DATA_PATH = DOWNLOAD_PATH + "frames"
EPOCHS = 10
IMG_HEIGHT = 240
IMG_WIDTH = 240

"""Get all classes."""
CLASS_NAMES = [category.name for category in pathlib.Path(DATA_PATH).iterdir()]
NUM_CLASSES = len(CLASS_NAMES)


def main():
    """Create a model."""

    """Load the data."""
    trainData, valData = loadData(DATA_PATH)

    """Create and compile the model."""
    model = getModel()
    #model.summary()

    """Fit the model and save the history."""
    history = model.fit(trainData, validation_data=valData, epochs=EPOCHS)

    """Save the model to a file."""
    model.save("model/model3.h5")
    print("Model saved.")

    """Make loss and accuracy plots on the training and validation sets."""
    makePlots(history, EPOCHS)


def loadData(data_dir):
    """Load the data. Return tuple (`train_ds`, `val_ds`)."""

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
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.shuffle(250).prefetch(buffer_size=1)
    val_ds = val_ds.prefetch(buffer_size=1)

    return train_ds, val_ds


def getModel():
    """Create and compile neural network."""

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
    """Visualize training results."""

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
