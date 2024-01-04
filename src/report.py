"""
---
name: report.py
description: Create Model History report
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import pandas as pd


class Report():
    """ Report class """

    def __init__(self, history) -> None:
        self.__history = history.history
        self.__dataframe: pd.DataFrame
        self._parse_data()

    def _parse_data(self):
        self.__dataframe = pd.DataFrame(
            [
                self.__history['loss'],
                self.__history['accuracy'],
                self.__history['val_loss'],
                self.__history['val_accuracy']
            ],
        ).transpose()
        self.__dataframe.columns = [
            'loss', 'accuracy', 'val_loss', 'val_accuracy'
        ]

    def save(self):
        """ Save reports """
        self.csv('report.csv')
        self.png('report.png')

    def csv(self, destination: str):
        """ Save CSV format report

        Args:
            destination (str): destination path
        """
        self.__dataframe.to_csv(destination, index=False)

    def png(self, destination: str):
        """ Save PNG format report

        Args:
            destination (str): destination path
        """
        plot = self.__dataframe.plot()
        fig = plot.get_figure()
        fig.savefig(destination)
