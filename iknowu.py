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
from functools import wraps

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

    @staticmethod
    def __config(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            Config().file = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), 'config.yaml'
            )
            func(*args, **kwargs)
        return wrapper

    @staticmethod
    def __logger(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            Log().name = 'IknowU'
            Log().verbosity = 'WARNING'
            Log().start()
            func(*args, **kwargs)
        return wrapper

    @__logger
    @__config
    def train(self):
        """ Train """
        parser = argparse.ArgumentParser(
            prog=f'{self.__name} train',
            description='Train model')
        parser.add_argument(
            '-e', '--epochs',
            required=False,
            default=15,
            type=int,
            help='Epochs')
        parser.add_argument(
            '-r', '--report',
            required=False,
            action='store_true',
            help='Save report',
        )
        parser.add_argument(
            '-v', '--verbosity',
            required=False,
            help='DEBUG, INFO, WARNING, ERROR (default) or CRITICAL')
        args = parser.parse_args(sys.argv[2:])
        Log().verbosity = args.verbosity
        log.info('Running train...')
        from tools.train \
            import Train  # pylint: disable=import-outside-toplevel
        from tools.report \
            import Report  # pylint: disable=import-outside-toplevel
        train = Train()
        train.epochs = args.epochs
        history = train.run()
        train.save()
        if args.report:
            report = Report(history)
            report.save()
        log.info('Done')

    @__logger
    @__config
    def infer(self):
        """ Infer """
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
        infer = Infer()
        infer.picture = args.file
        print(infer.run())
        log.info('Done')


if __name__ == '__main__':
    IknowU()
