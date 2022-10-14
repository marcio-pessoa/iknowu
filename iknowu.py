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
import logging
import logging.handlers
import json
import argparse

from tools.config import config

if not (sys.version_info.major == 3 and sys.version_info.minor >= 6):
    print("This program requires Python 3.6 or higher!")
    print(
        'You are using Python '
        f'{sys.version_info.major}.{sys.version_info.minor}.'
    )
    sys.exit(True)


class IknowU():  # pylint: disable=too-few-public-methods
    """ InowU class

    argparse reference:
      - https://docs.python.org/2/library/argparse.html
      - http://chase-seibert.github.io/blog/
    """

    __version__ = 0.02
    __date__ = "2020-03-09"

    def __init__(self):
        self.__name = "iknowu.py"
        self.__work_dir = os.path.dirname(os.path.realpath(__file__))
        self.__logger = logging.getLogger(self.__name)
        self._logger()
        self.__logger.setLevel(logging.DEBUG)
        self.__logger.debug('Starting %s [%s]', self.__name, self.__version__)
        self.__config = None
        self._config()

        header = (
            f'{self.__name} <command> [<args>]\n\n'
            'commands:\n'
            '  obtain         Obtain data (import pictures)\n'
            '  train          Train model\n'
            '  infer          Do an infer\n\n'
        )
        parser = argparse.ArgumentParser(
            prog=self.__name,
            description='Machine Learning image categorisation',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=(
                'examples:\n'
                f'  {self.__name} --help\n'
                f'  {self.__name} -v\n'
                '\n'
                'Copyright (c) 2020 Marcio Pessoa' + '\n'
                'License: ' + 'GPLv2. There is NO WARRANTY.' + '\n'
                'Website: ' + 'https://github.com/marcio-pessoa/iknowu\n'
                'Contact: ' + 'Marcio Pessoa <marcio.pessoa@gmail.com>\n'
            ),
            add_help=True,
            usage=header
        )
        parser.add_argument('command', help='command to run')
        parser.add_argument(
            '-V', '--version',
            action='version',
            help='show version information and exit',
            version=f'{self.__name} {self.__version__} {self.__date__}',
        )

        if len(sys.argv) < 2:
            print(header)
            sys.exit(True)

        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            sys.exit(True)

        getattr(self, args.command)()

    def obtain(self):
        """
        description:
        """
        parser = argparse.ArgumentParser(
            prog=self.__name + ' obtain',
            description='Obtain data')
        parser.add_argument(
            '-d', '--directory',
            required=True,
            help='Directory')
        parser.add_argument(
            '-n', '--name',
            required=True,
            help='Personal name')
        parser.add_argument(
            '-p', '--purpose',
            required=True,
            default='training',
            choices=['training', 'evaluate'],
            help='Desired purpose')
        parser.add_argument(
            '-v', '--verbosity',
            required=False,
            help='DEBUG, INFO, WARNING, ERROR (default) or CRITICAL')
        args = parser.parse_args(sys.argv[2:])
        self._verbosity(args.verbosity)
        from tools.obtain \
            import Obtain  # pylint: disable=import-outside-toplevel
        self.__logger.info('Running obtain...')
        step = Obtain()
        status = step.config(
            source_directory=args.directory,
            destination_directory=os.path.join(
                self.__work_dir,
                self.__config['general']['directory']),
            purpose=args.purpose,
            name=args.name)
        self._check_error(status)
        self.__logger.info(step.info())
        result = step.run()
        self._check_error(result)
        self.__logger.info('Done')

    def train(self):
        """
        description:
        """
        parser = argparse.ArgumentParser(
            prog=self.__name + ' train',
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
        self._verbosity(args.verbosity)
        from tools.train \
            import Train  # pylint: disable=import-outside-toplevel
        self.__logger.info('Running train...')
        step = Train()
        step.epochs = args.epochs
        status = step.config(
            directory=os.path.join(
                self.__work_dir,
                self.__config['general']['directory']))
        self._check_error(status)
        # self.__logger.info(step.info())
        result = step.run()
        self._check_error(result)
        print(json.dumps(result, indent=2, separators=(", ", ": ")))
        self.__logger.info(result)
        self.__logger.info('Done')

    def infer(self):
        """
        description:
        """
        parser = argparse.ArgumentParser(
            prog=self.__name + ' infer',
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
        self._verbosity(args.verbosity)
        from tools.infer \
            import Infer  # pylint: disable=import-outside-toplevel
        self.__logger.info('Running infer...')
        step = Infer()
        status = step.config(
            directory=os.path.join(
                self.__work_dir,
                self.__config['general']['directory']),
            picture=args.file,
            people=self.__config['person'])
        self._check_error(status)
        result = step.run()['results']
        self._check_error(result)
        print(result['person'])
        self.__logger.info('Person: %s', result['person'])
        self.__logger.info('Class: %s', result['classes'])
        self.__logger.info('Done')

    def _logger(self):
        _format = ' [%(process)d]: %(levelname)s: %(message)s'
        formatter = logging.Formatter(fmt=self.__name + _format)
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        handler.setFormatter(formatter)
        self.__logger.addHandler(handler)

    def _verbosity(self, level):
        """
        description: Set verbosity
        """
        if level == 'DEBUG':
            self.__logger.setLevel(logging.DEBUG)
        elif level == 'INFO':
            self.__logger.setLevel(logging.INFO)
        elif level == 'WARNING':
            self.__logger.setLevel(logging.WARNING)
        elif level == 'ERROR':
            self.__logger.setLevel(logging.ERROR)
        elif level == 'CRITICAL':
            self.__logger.setLevel(logging.CRITICAL)
        else:
            self.__logger.error("Unknown verbosity level, setting to: 'ERROR'")
            self.__logger.setLevel(logging.ERROR)

    def _config(self):
        config_file = os.path.join(self.__work_dir, 'config.json')
        self.__config = config(config_file)
        self._check_error(self.__config)

    def _check_error(self, message):
        if not message:
            return False
        if 'error' in message:
            if 'message' in message['error']:
                self.__logger.error(message['error']['message'])
            if 'exception' in message['error']:
                self.__logger.error(message['error']['exception'])
            sys.exit(True)
        return True


if __name__ == '__main__':
    IknowU()
