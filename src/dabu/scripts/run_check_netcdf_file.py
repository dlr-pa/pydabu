"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-08 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

from dabu.check_netcdf_file import check_netcdf_file

from .print_json_output import print_json_output


def run_check_netcdf_file(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-08 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    result = dict()
    result['data'] = []
    for file in args.file:  # for every given file
        res = check_netcdf_file(file, args.output_format[0])
        result['data'].append(
            {'name': file,
             'netcdf check': res})
    print_json_output(result, args.output_format)
