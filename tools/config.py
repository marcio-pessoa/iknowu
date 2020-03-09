"""
---
name: config.py
description: Configuration package
copyright: 2020 Marcio Pessoa
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@telefonica.com
change-log: Check CHANGELOG.md file.
"""

import json

def config(config_file):
    """
    description:
    """
    try:
        data = open(config_file, 'r')
    except IOError as err:
        return \
            {
                'error': {
                    'message': 'Failed to read file.',
                    'exception': str(err)
                }
            }
    try:
        data = data.read()
        return json.loads(data)
    except BaseException:
        return \
            {
                'error': {
                    'message': 'Can\'t parse configuration file.',
                    'exception': ''
                }
            }
    return \
        {
            'error': {
                'message': 'Unknown problem.',
                'exception': ''
            }
        }
