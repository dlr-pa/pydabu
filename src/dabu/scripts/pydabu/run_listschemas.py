"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json
import os

import dabu


def run_listschemas(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-19 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    schema_list = os.listdir(os.path.join(dabu.__path__[0], 'schemas'))

    def add_path(path):
        # a kind of lambda function
        return os.path.join(dabu.__path__[0], 'schemas', path)

    schema_list = list(map(add_path, schema_list))
    schema_list.sort()
    if 'simple' in args.output_format:
        for schema_name in schema_list:
            print(schema_name)
    else:
        print(json.dumps(list(schema_list)))
