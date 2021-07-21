"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-15 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os

from dabu.analyse_data_structure import analyse_data_structure
from dabu.analyse_file_format import analyse_file_format_dict

from .print_json_output import print_json_output


def run_check_file_format(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-15 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    actpath = os.getcwd()
    for path in args.directory:  # for every given directory
        os.chdir(actpath)
        os.chdir(path)
        result = analyse_data_structure()
        checksum_file = None
        if args.checksum_from_file is not None:
            checksum_file = args.checksum_from_file[0]
        result = analyse_file_format_dict(
            result,
            args.output_format,
            not args.skip_creating_checksums,
            checksum_file)
        print_json_output(result, args.output_format)
