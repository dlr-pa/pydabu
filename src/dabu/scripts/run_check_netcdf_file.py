"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-01-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json

from dabu.check_netcdf_file import check_netcdf_file


def run_check_netcdf_file(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-01-29 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    result = dict()
    result['data'] = []
    for file in args.file:  # for every given file
        res, checker_name = check_netcdf_file(file)
        if 'human_readable' in args.output_format:
            del res[checker_name]['result']
        result['data'].append(
            {'name': file,
             'netcdf check': res})
    if 'json' in args.output_format:
        print(json.dumps(result))
    if 'human_readable' in args.output_format:
        print(json.dumps(result, indent=1))
