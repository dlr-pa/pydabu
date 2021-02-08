"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-08 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json
import jsonschema
import os.path

from .check_arg_file import check_arg_file


def run_check_data_bubble(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-08 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    for path in args.directory:  # for every given directory
        check_arg_file(os.path.join(path, args.dabu_instance_file[0]))
        check_arg_file(os.path.join(path, args.dabu_schema_file[0]))
        with open(os.path.join(path, args.dabu_instance_file[0]),
                  mode='r') as fd:
            instance = json.load(fd)
        with open(os.path.join(path, args.dabu_schema_file[0]),
                  mode='r') as fd:
            schema = json.load(fd)
        jsonschema.validate(instance, schema)
