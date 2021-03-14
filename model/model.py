from config import DATA_PATH
import numpy as np
import os
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential




from config import DATA_PATH
#import pathlib
#directory = pathlib.Path(DATA_PATH)

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

train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)










"""

data = tf.keras.preprocessing.image_dataset_from_directory(
    DATA_PATH,
    image_size=(480, 854)
)
"""
