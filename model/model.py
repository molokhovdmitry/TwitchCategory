from config import DATA_PATH
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

import sys


from config import DATA_PATH
import pathlib
directory = pathlib.Path(DATA_PATH)

#imageCount = len(list(directory.glob("*/*.jpg")))

#game = list(directory.glob('941530474/*'))
#image = PIL.Image.open(str(game[105]))
#image.show()

IMG_HEIGHT = 480
IMG_WIDTH = 854

train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    DATA_PATH,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=16
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    DATA_PATH,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMG_HEIGHT, IMG_WIDTH),
    batch_size=16
)


AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.cache().shuffle(50).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)


image_batch, labels_batch = next(iter(train_ds))
print(image_batch)
print(labels_batch)


normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixels values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image)) 