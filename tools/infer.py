"""
---
name: inter.py
description: IknowU inter package
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import os
import contextlib
import numpy as np

# 0 = all messages are logged (default behavior)
# 1 = INFO messages are not printed
# 2 = INFO and WARNING messages are not printed
# 3 = INFO, WARNING, and ERROR messages are not printed
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

with contextlib.redirect_stdout(None):
    import tensorflow as tf  # pylint: disable=import-error
    from keras_preprocessing import image  # pylint: disable=import-error


class Infer():
    """
    description:
    """

    __version__ = 0.02

    def __init__(self):
        self.__directory = None
        self.__picture_path = None
        self.__picture = None
        self.__people = []
        self.__model = None

    def config(self, directory=None, picture=None, people=None):
        """
        description:
        """
        if directory:
            self.__directory = directory
            if not os.path.isdir(self.__directory):
                return \
                    {
                        'error': {
                            'message': 'Directory not found: ' +
                            self.__directory
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
        if people:
            for person in people:
                self.__people.append(person['nick'])
            self.__people.sort()
        return False

    def _load_model(self):
        model_file_path = os.path.join(self.__directory, 'model.h5')
        self.__model = tf.keras.models.load_model(model_file_path)

    def _load_picture(self):
        picture_raw = image.load_img(
            self.__picture_path, target_size=(150, 150)
        )
        picture_array = image.img_to_array(picture_raw)
        picture_array = np.expand_dims(picture_array, axis=0)
        self.__picture = np.vstack([picture_array])

    def _what_is_your_name(self, infer_list):
        infer_list_sorted = infer_list.tolist()[0]
        infer_list_sorted.sort()
        higher = infer_list_sorted[-1]
        position = np.where(infer_list == higher)
        position = position[1].tolist()[0]
        return self.__people[position]

    def run(self):
        """
        description:
        """
        self._load_model()
        self._load_picture()
        classes = self.__model.predict(self.__picture, batch_size=10)
        person = self._what_is_your_name(classes)
        return \
            {
                'results': {
                    'person': person,
                    'classes': classes
                }
            }
