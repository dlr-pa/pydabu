"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

from .set_property import set_property


def combine(json_instance1, json_instance2):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16

    This function combines/merges 2 json instances. 
    Each are a combination of dicts and lists.

    :param json_instance1: json_instance
    :param json_instance2: json_instance, which is merged into json_instance1
    """
    for key in json_instance2:
        add_property(json_instance1, key, json_instance2[key])


def add_property(schema, key, value):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16
    """
    if key in schema:
        if isinstance(schema[key], dict):
            if isinstance(value, dict):
                combine(schema[key], value)
            elif isinstance(value, list):
                raise TypeError('no idea how to merge list in dict')
            else:  # string, int, float, bool or None
                raise TypeError(
                    'no idea to merge none interabel in dict')
        elif isinstance(schema[key], list):
            if isinstance(value, dict):
                raise TypeError('no idea how to merge dict in list')
            elif isinstance(value, list):
                schema[key] = list(set(schema[key] + value))
            else:  # string, int, float, bool or None
                if not value in schema[key]:
                    schema[key].append(value)
        else:  # string, int, float, bool or None
            if isinstance(value, dict):
                schema[key] = [schema[key], value]
            elif isinstance(value, list):
                schema[key] = [schema[key]] + \
                    value
            else:  # string, int, float, bool or None
                schema[key] = [schema[key], value]
    else:
        set_property(schema, key, value)
