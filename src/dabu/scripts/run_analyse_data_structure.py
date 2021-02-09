"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-09 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os

from dabu.analyse_data_structure import analyse_data_structure

from .print_json_output import print_json_output


def run_analyse_data_structure(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-09 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    for path in args.directory:  # for every given directory
        os.chdir(path)
        result = analyse_data_structure()
        print_json_output(result, args.output_format)
