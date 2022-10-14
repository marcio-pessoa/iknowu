"""
---
name: config.py
description: Configuration package
people:
  developers:
  - name: Marcio Pessoa
    email: marcio.pessoa@gmail.com
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
