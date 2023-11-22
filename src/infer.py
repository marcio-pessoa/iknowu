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

from src.config import Config
from src.log import Log

# 0 = all messages are logged (default behavior)
# 1 = INFO messages are not printed
# 2 = INFO and WARNING messages are not printed
# 3 = INFO, WARNING, and ERROR messages are not printed
os.environ['TF_CPP_MIN_LOG_LEVEL'] = str(Log().tf_verbosity)

with contextlib.redirect_stdout(None):
    import keras
    from keras_preprocessing import image


class Infer():
    """ Infer class """

    __version__ = 0.02

    def __init__(self):
        self.__directory = ''
        self.__picture_path = ''
        self.__picture = None
        self.__people = []
        self.__model: keras.models.Sequential
        self._config()

    def _config(self):
        self.__directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '../',
            Config().get['general']['directory']
        )

        if not os.path.isdir(self.__directory):
            raise ValueError(f'Directory not found: {self.__directory}')

        for person in Config().get['person']:
            self.__people.append(person['nick'])
        self.__people.sort()

    @property
    def picture(self) -> str:
        """ Picure path getter

        Returns:
            str: Picture path
        """
        return self.__picture_path

    @picture.setter
    def picture(self, picture_path: str):
        """ Picture path setter

        Args:
            picture_path (str): File path

        Raises:
            Exception: Error message when file not found
        """
        self.__picture_path = picture_path
        if not os.path.isfile(self.__picture_path):
            raise ValueError(f'File not found: {self.__picture_path}')

    def _load_model(self):
        model_file_path = os.path.join(self.__directory, 'model.h5')
        self.__model = keras.models.load_model(model_file_path)

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
        """ Run infer """
        self._load_model()
        self._load_picture()
        classes = self.__model.predict(self.__picture, batch_size=10)
        person = self._what_is_your_name(classes)
        return person
