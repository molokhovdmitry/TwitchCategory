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

IMG_HEIGHT = 180
IMG_WIDTH = 180

class_names = ['138585', '1614555304', '18122', '21779', '2692', '27471', '2748', '278888515', '29307', '29595', '30921', '32399', '32982', '33214', '369418', '460316', '460630', '488552', '489635', '490100', '490292', '491487', '491931', '493057', '508292', '508455', '509663', '510218', '511224', '512709', '512710', '513143', '516575', '518204', '941530474']

path = "test/fort3.jpg"

img = keras.preprocessing.image.load_img(
    path, target_size=(IMG_HEIGHT, IMG_WIDTH)
)

img_array = keras.preprocessing.image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)

model = keras.models.load_model("model.h5")

predictions = model.predict(img_array)
category = class_names[predictions.argmax()]
probability = max(predictions[0])

score = tf.nn.softmax(predictions[0])

print(
    "This image most likely belongs to {} with a {:.2f} percent confidence."
    .format(class_names[np.argmax(score)], 100 * np.max(score))
)
