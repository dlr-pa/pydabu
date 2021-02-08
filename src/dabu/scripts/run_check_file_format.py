"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-08 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json

from dabu.analyse_data_structure import analyse_data_structure
from dabu.analyse_file_format import analyse_file_format_dict


def run_check_file_format(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-08 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    # print(args);exit()
    for path in args.directory:  # for every given directory
        result = analyse_data_structure(path)
        result = analyse_file_format_dict(path, result, args.output_format)
        # print(result)
        if 'json' in args.output_format:
            print(json.dumps(result))
        elif 'json1' in args.output_format:
            print(json.dumps(result, indent=1))
        eöif 'human_readable' in args.output_format:
            print(json.dumps(result, indent=1))
