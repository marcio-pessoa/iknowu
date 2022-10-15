#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
---
name: iknowu.py
description: Main program file
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
"""

import sys
import os
import argparse
import numpy as np

from tools.log import Log, log
from tools.config import Config

if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
    print("This program requires Python 3.6 or higher!")
    print(
        'You are using Python '
        f'{sys.version_info.major}.{sys.version_info.minor}.'
    )
    sys.exit(True)


class IknowU():
    """ IknowU main class """

    __version__ = 0.02
    __date__ = "2020-10-15"

    def __init__(self):
        self.__name = "iknowu.py"
        self.__work_dir = os.path.dirname(os.path.realpath(__file__))

        Log().name = 'IknowU'
        Log().verbosity = 'WARNING'
        Log().start()
        log.info('Starting %s [%s]', self.__name, self.__version__)

        Config().file = os.path.join(self.__work_dir, 'config.yaml')

        parser = argparse.ArgumentParser(
            prog=self.__name,
            description='Machine Learning image categorisation',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=(
                'examples:\n'
                f'  {self.__name} --help\n'
                f'  {self.__name} -v\n'
                '\n'
                'Copyright (c) 2020 Marcio Pessoa\n'
                'License: GPLv2. There is NO WARRANTY.\n'
                'Website: https://github.com/marcio-pessoa/iknowu\n'
                'Contact: Marcio Pessoa <marcio.pessoa@gmail.com>\n'
            ),
            add_help=True,
            usage=(
                f'{self.__name} <command> [<args>]\n\n'
                'commands:\n'
                '  obtain         Obtain data (import pictures)\n'
                '  train          Train model\n'
                '  infer          Do an infer\n\n'
            )
        )
        parser.add_argument('command', help='command to run')
        parser.add_argument(
            '-V', '--version',
            action='version',
            help='show version information and exit',
            version=f'{self.__name} {self.__version__} {self.__date__}',
        )

        if len(sys.argv) < 2:
            parser.print_usage()
            sys.exit(True)

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            sys.exit(True)

        getattr(self, args.command)()

    def train(self):
        """
        description:
        """
        parser = argparse.ArgumentParser(
            prog=f'{self.__name} train',
            description='Train model')
        parser.add_argument(
            '-e', '--epochs',
            required=False,
            default=25,
            type=int,
            help='Epochs')
        parser.add_argument(
            '-v', '--verbosity',
            required=False,
            help='DEBUG, INFO, WARNING, ERROR (default) or CRITICAL')
        args = parser.parse_args(sys.argv[2:])
        Log().verbosity = args.verbosity
        log.info('Running train...')
        from tools.train \
            import Train  # pylint: disable=import-outside-toplevel
        step = Train()
        step.epochs = args.epochs
        status = step.config(
            directory=os.path.join(
                self.__work_dir,
                Config().get['general']['directory']))
        self._check_error(status)
        # log.info(step.info())
        history = step.run()
        step.save()

        header = ['loss', 'accuracy', 'val_loss', 'val_accuracy']
        result = [
            history['loss'],
            history['accuracy'],
            history['val_loss'],
            history['val_accuracy']
        ]
        log.debug(header)
        log.debug(np.transpose(result).tolist())
        log.info('Done')

    def infer(self):
        """
        description:
        """
        parser = argparse.ArgumentParser(
            prog=f'{self.__name} infer',
            description='Do an infer')
        parser.add_argument(
            '-f', '--file',
            required=True,
            help='Image file')
        parser.add_argument(
            '-v', '--verbosity',
            required=False,
            help='DEBUG, INFO, WARNING, ERROR (default) or CRITICAL')
        args = parser.parse_args(sys.argv[2:])
        Log().verbosity = args.verbosity
        log.info('Running infer...')
        from tools.infer \
            import Infer  # pylint: disable=import-outside-toplevel
        step = Infer()
        status = step.config(
            directory=os.path.join(
                self.__work_dir,
                Config().get['general']['directory']),
            picture=args.file,
            people=Config().get['person'])
        self._check_error(status)
        print(step.run())
        log.info('Done')

    def _check_error(self, message):
        if not message:
            return False
        if 'error' in message:
            if 'message' in message['error']:
                log.error(message['error']['message'])
            if 'exception' in message['error']:
                log.error(message['error']['exception'])
            sys.exit(True)
        return True


if __name__ == '__main__':
    IknowU()
