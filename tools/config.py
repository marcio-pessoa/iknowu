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
    with open(config_file, 'r', encoding='UTF-8') as reader:
        return json.loads(reader.read())
    return \
        {
            'error': {
                'message': 'Can\'t parse configuration file.',
                'exception': ''
            }
        }
