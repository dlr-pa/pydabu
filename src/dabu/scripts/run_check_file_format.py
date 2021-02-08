"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-08 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

from dabu.analyse_data_structure import analyse_data_structure
from dabu.analyse_file_format import analyse_file_format_dict

from .print_json_output import print_json_output


def run_check_file_format(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-08 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    for path in args.directory:  # for every given directory
        result = analyse_data_structure(path)
        result = analyse_file_format_dict(path, result, args.output_format)
        print_json_output(result, args.output_format)
