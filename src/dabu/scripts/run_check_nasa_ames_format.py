"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-08 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

from dabu.check_nasa_ames_format import check_nasa_ames_format

from .print_json_output import print_json_output


def run_check_nasa_ames_format(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-08 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    result = dict()
    result['data'] = []
    for file in args.file:  # for every given file
        res = check_nasa_ames_format(file, args.output_format[0])
        result['data'].append(
            {'name': file,
             'nasa ames format check': res})
    print_json_output(result, args.output_format)
