"""
---
name: config.py
description: Configuration Singleton package
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

from json import loads as json_load, JSONDecodeError
from yaml import load as yaml_load, Loader, YAMLError


class Config:
    """ Configuration Singleton """
    __path = ''
    __config = dict

    def __new__(cls):
        if not hasattr(cls, 'instance') or not cls.instance:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __load(self) -> None:
        # Read file content
        with open(self.__path, 'r', encoding='UTF-8') as reader:
            try:
                data = reader.read()
                reader.close()
            except IOError:
                print("Can't open configuration file")
                return

        # Parse JSON
        try:
            self.__config = json_load(data)
            return
        except JSONDecodeError:
            pass

        # Parse YAML
        try:
            self.__config = yaml_load(data, Loader=Loader)
            return
        except YAMLError:
            pass

        print("Can't parse configuration file")

    @property
    def file(self):
        """ Configuration file getter

        Returns:
            str: Configuration file absolute path
        """
        return self.__path

    @file.setter
    def file(self, path):
        self.__path = path
        self.__load()

    @property
    def get(self) -> dict:
        """ Configuration getter

        Returns:
            dict: full configuration structure
        """
        return self.__config
