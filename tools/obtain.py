"""
---
name: obtain.py
description: IknowU obtain package
copyright: 2020 Marcio Pessoa
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@telefonica.com
change-log: Check CHANGELOG.md file.
"""

import os
import shutil


class Obtain():
    """
    description:
    """

    __version__ = 0.02

    def __init__(self):
        self.__name = None
        self.__purpose = None
        self.__src_dir = None
        self.__dst_dir = None

    def config(self,
               source_directory=None,
               destination_directory=None,
               purpose=None,
               name=None):
        """
        description:
        """
        retval = {}
        if source_directory:
            retval = \
                {
                    **retval,
                    **self._source_directory(source_directory)
                }
        if destination_directory:
            retval = \
                {
                    **retval,
                    **self._destination_directory(destination_directory)
                }
        if purpose:
            retval = \
                {
                    **retval,
                    **self._purpose(purpose)
                }
        if name:
            retval = \
                {
                    **retval,
                    **self._name(name)
                }
        return retval

    def _source_directory(self, directory):
        self.__src_dir = directory
        if not os.path.isdir(self.__src_dir):
            return \
                {
                    'error': {
                        'message': 'Directory not found'
                    }
                }
        return {}

    def _destination_directory(self, directory):
        self.__dst_dir = directory
        if not os.path.isdir(self.__dst_dir):
            return create_directory(self.__dst_dir)
        return {}

    def _purpose(self, purpose):
        self.__purpose = purpose
        self.__dst_dir = os.path.join(self.__dst_dir, self.__purpose)
        if not os.path.isdir(self.__dst_dir):
            return create_directory(self.__dst_dir)
        return {}

    def _name(self, name):
        self.__name = name
        self.__name = self.__name.lower()
        self.__name = self.__name.replace(' ', '_')
        self.__dst_dir = os.path.join(self.__dst_dir, self.__name)
        if not os.path.isdir(self.__dst_dir):
            return create_directory(self.__dst_dir)
        return {}

    def info(self):
        """
        description:
        """
        return \
            {
                'source': {
                    'path': self.__src_dir,
                    'files': len(os.listdir(self.__src_dir))
                },
                'destination': {
                    'path': self.__dst_dir,
                    'files': len(os.listdir(self.__dst_dir))
                }
            }

    def run(self):
        """
        description:
        """
        src_files = os.listdir(self.__src_dir)
        for i in src_files:
            path = os.path.join(self.__src_dir, i)
            if os.path.isfile(path):
                shutil.copy(path, self.__dst_dir)
        return {}

def create_directory(directory):
    """
    description:
    """
    try:
        os.makedirs(directory)
    except OSError as err:
        return \
            {
                'error': {
                    'message': 'Failed to create directory: ' + directory,
                    'exception': str(err)
                }
            }
    return {}
