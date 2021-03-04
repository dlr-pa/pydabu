"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-17 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json
import os.path
import pkgutil

from dabu.analyse_data_structure import analyse_data_structure
from dabu.analyse_file_format import analyse_file_format_dict

from .check_arg_file_not_exisits import check_arg_file_not_exisits


def run_create_data_bubble(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-17 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    for path in args.directory:  # for every given directory
        check_arg_file_not_exisits(
            os.path.join(path, args.dabu_instance_file[0]))
        check_arg_file_not_exisits(
            os.path.join(path, args.dabu_schema_file[0]))
        result = analyse_data_structure(path)
        checksum_file = None
        if args.checksum_from_file is not None:
            checksum_file = args.checksum_from_file[0]
        result = analyse_file_format_dict(
            result,
            'json',
            not args.skip_creating_checksums,
            checksum_file)
        fd = open(os.path.join(path, args.dabu_instance_file[0]), mode='w')
        json.dump(result, fd, indent=args.indent[0])
        fd.close()
        schema = json.loads(pkgutil.get_data(
            'dabu', 'schemas/dabu_requires.schema'))
        fd = open(os.path.join(path, args.dabu_schema_file[0]), mode='w')
        json.dump(schema, fd, indent=args.indent[0])
        fd.close()
