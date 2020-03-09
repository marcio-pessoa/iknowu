"""
---
name: inter.py
description: IknowU inter package
copyright: 2020 Marcio Pessoa
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@telefonica.com
change-log: Check CHANGELOG.md file.
"""

import os
import numpy as np
import tensorflow as tf  # pylint: disable=import-error
# import keras_preprocessing  # pylint: disable=import-error
from keras_preprocessing import image  # pylint: disable=import-error
# from keras_preprocessing.image import ImageDataGenerator  # pylint: disable=import-error


class Infer():
    """
    description:
    """

    __version__ = 0.01

    def __init__(self):
        self.__directory = None
        self.__picture_path = None
        self.__picture = None
        self.__model = None

    def config(self, directory=None, picture=None):
        """
        description:
        """
        if directory:
            self.__directory = directory
            if not os.path.isdir(self.__directory):
                return \
                    {
                        'error': {
                            'message': 'Directory not found: ' + self.__directory
                        }
                    }
        if picture:
            self.__picture_path = picture
            if not os.path.isfile(self.__picture_path):
                return \
                    {
                        'error': {
                            'message': 'File not found: ' + self.__picture_path
                        }
                    }
        return {}

    def _load_model(self):
        model_file_path = os.path.join(self.__directory, 'model.h5')
        self.__model = tf.keras.models.load_model(model_file_path)

    def _load_picture(self):
        # for fn in uploaded.keys():

        # predicting images
        # path = fn
        img = image.load_img(self.__picture_path, target_size=(150, 150))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        self.__picture = np.vstack([x])


    def run(self):
        """
        description:
        """
        self._load_model()
        self._load_picture()
        classes = self.__model.predict(self.__picture, batch_size=10)
        print(classes)
