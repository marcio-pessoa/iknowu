"""
---
name: train.py
description: IknowU train package
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import os
import contextlib

from src.config import Config
from src.log import Log, logging

# 0 = all messages are logged (default behavior)
# 1 = INFO messages are not printed
# 2 = INFO and WARNING messages are not printed
# 3 = INFO, WARNING, and ERROR messages are not printed
os.environ['TF_CPP_MIN_LOG_LEVEL'] = str(Log().tf_verbosity)

with contextlib.redirect_stdout(None):
    import keras
    from keras_preprocessing.image import ImageDataGenerator


class Train():
    """ Train class """

    __version__ = 0.02

    def __init__(self):
        self.__directory = ''
        self.__dir_training = ''
        self.__dir_evaluate = ''
        self.__model: keras.models.Sequential
        self.__generator_training = None
        self.__generator_evaluate = None
        self.epochs = 10

        self._config()

    def _config(self):
        self.__directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            '../',
            Config().get['general']['directory']
        )
        self.__dir_training = os.path.join(self.__directory, 'training')
        self.__dir_evaluate = os.path.join(self.__directory, 'evaluate')
        directories = (self.__dir_training, self.__dir_evaluate)
        for i in directories:
            if not os.path.isdir(i):
                raise ValueError(f'Directory not found: {i}')

    def _datagen(self):
        # Set data generator
        datagen_training = ImageDataGenerator(
            rescale=1/255,
            rotation_range=10,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            vertical_flip=True,
            fill_mode='nearest')
        datagen_evaluate = ImageDataGenerator(rescale=1/255)

        # Set image directories
        self.__generator_training = datagen_training.flow_from_directory(
            self.__dir_training,
            target_size=(150, 150),
            class_mode='categorical'
        )
        self.__generator_evaluate = datagen_evaluate.flow_from_directory(
            self.__dir_evaluate,
            target_size=(150, 150),
            class_mode='categorical'
        )

    def _model(self):
        self.__model = keras.models.Sequential([
            # Note the input shape is the desired size of the image 150x150
            # with 3 bytes color
            # This is the first convolution
            keras.layers.Conv2D(
                64, (3, 3),
                activation='relu',
                input_shape=(150, 150, 3)),
            keras.layers.MaxPooling2D(2, 2),
            # The second convolution
            keras.layers.Conv2D(
                64, (3, 3),
                activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            # The third convolution
            keras.layers.Conv2D(
                128, (3, 3),
                activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            # The fourth convolution
            keras.layers.Conv2D(
                128, (3, 3),
                activation='relu'),
            keras.layers.MaxPooling2D(2, 2),
            # Flatten the results to feed into a DNN
            keras.layers.Flatten(),
            keras.layers.Dropout(0.5),
            # 512 neuron hidden layer
            keras.layers.Dense(
                512,
                activation='relu'),
            keras.layers.Dense(
                3,
                activation='softmax')])
        self.__model.compile(
            loss='categorical_crossentropy',
            optimizer='rmsprop',
            metrics=['accuracy'])

        if Log().verbosity == logging.DEBUG:
            self.__model.summary()

    def save(self):
        """ Save model """
        model_file_path = os.path.join(self.__directory, 'model.keras')
        self.__model.save(model_file_path)

    def run(self):
        """ Run model """
        self._datagen()
        self._model()

        verbose = False
        if Log().verbosity == logging.DEBUG:
            verbose = True

        history = self.__model.fit(
            self.__generator_training,
            epochs=self.epochs,
            validation_data=self.__generator_evaluate,
            verbose=verbose)
        return history
