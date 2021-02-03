"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-03 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import argparse
import os.path

from .run_check_data_structure import run_check_data_structure
from .run_check_file_format import run_check_file_format
from .run_check_netcdf_file import run_check_netcdf_file

def check_arg_directory(data):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-01-19 (last change).
    """
    if not os.path.isdir(data):
        msg = '"%s" is not a directory' % data
        raise argparse.ArgumentTypeError(msg)
    return data

def check_arg_file(data):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-01-29 (last change).
    """
    if not os.path.isfile(data):
        msg = '"%s" is not a file' % data
        raise argparse.ArgumentTypeError(msg)
    return data


def my_argument_parser():
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-03 (last change).
    """
    epilog = ""
    epilog += "You can few the json output for example in firefox, "
    epilog += "e. g. in bash:\n\n"
    epilog += "output=$(tempfile --suffix='.json'); "
    epilog += "pydabu.py check_file_format -output_format json > "
    epilog += "$output && firefox $output; "
    epilog += "sleep 3; rm $output\n\n"
    epilog += "output=$(tempfile --suffix='.json'); "
    epilog += "pydabu.py check_netcdf_file -f $(find . -iname '*.nc') "
    epilog += "-output_format json > $output && firefox $output; "
    epilog += "sleep 3; rm $output\n\n"
    epilog += "Author: Daniel Mohr\n"
    epilog += "Date: 2021-01-29\n"
    epilog += "License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007."
    epilog += "\n\n"
    parser = argparse.ArgumentParser(
        description='pydabu.py is a script to check a data bubble.',
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # parent parser to describe common argument
    common_parser1 = argparse.ArgumentParser(add_help=False)
    common_parser1.add_argument(
        '-output_format',
        nargs=1,
        type=str,
        choices=['human_readable', 'json'],
        required=False,
        default=['human_readable'],
        dest='output_format',
        help='Set the output format to use. ' +
        'default: human_readable',
        metavar='f')
    common_parser2 = argparse.ArgumentParser(add_help=False)
    common_parser2.add_argument(
        '-directory',
        nargs="+",
        type=check_arg_directory,
        required=False,
        default=['.'],  # this is not checked against the required type
        dest='directory',
        help='Set the directory to use. ' +
        'You can also give a list of directories separated by space. ' +
        'default: .',
        metavar='d')
    common_parser3 = argparse.ArgumentParser(add_help=False)
    common_parser3.add_argument(
        '-file',
        nargs="+",
        type=check_arg_file,
        required=True,
        dest='file',
        help='Set the file(s) to use. ',
        metavar='f')
    # subparsers
    subparsers = parser.add_subparsers(
        dest='subparser_name',
        help='There are different sub-commands with there own flags.')
    # subparser check_data_structure
    parser_check_data_structure = subparsers.add_parser(
        'check_data_structure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py check_data_structure -h',
        description='',
        epilog='',
        parents=[common_parser1, common_parser2])
    parser_check_data_structure.set_defaults(func=run_check_data_structure)
    # subparser check_netcdf_file
    description = 'This command checks a file in the format netCDF.'
    description += 'It uses the CF Checker: '
    description += 'https://github.com/cedadev/cf-checker'
    epilog = 'Example:\n\n'
    epilog += '  pydabu.py check_netcdf_file -f a.nc > dabu_netcdf.json\n'
    epilog += '  jsonschema -i dabu_netcdf.json '
    epilog += '~/lib/python/dabu/schemas/dabu.schema\n'
    epilog += '  jsonschema -i dabu_netcdf.json '
    epilog += '~/lib/python/dabu/schemas/examples/dabu_requires.schema\n'
    parser_check_netcdf_file = subparsers.add_parser(
        'check_netcdf_file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py check_netcdf_file -h',
        description=description,
        epilog=epilog,
        parents=[common_parser1, common_parser3])
    parser_check_netcdf_file.set_defaults(func=run_check_netcdf_file)
    # subparser check_file_format
    description = 'This command checks the file formats. '
    description += 'In a first step the data structure is analysed like the '
    description += 'command "check_data_structure" does. '
    description += 'Each file is checked by a tool choosen by the '
    description += 'file extension. '
    description += 'For the file extension ".nc" the command '
    description += 'check_netcdf_file is used. '
    epilog = 'Example:\n\n'
    epilog += '  pydabu.py check_file_format -d . > dabu.json\n'
    epilog += '  jsonschema -i dabu.json '
    epilog += '~/lib/python/dabu/schemas/dabu.schema\n'
    epilog += '  jsonschema -i dabu.json '
    epilog += '~/lib/python/dabu/schemas/examples/dabu_requires.schema\n'
    parser_check_file_format = subparsers.add_parser(
        'check_file_format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py check_file_format -h',
        description=description,
        epilog=epilog,
        parents=[common_parser1, common_parser2])
    parser_check_file_format.set_defaults(func=run_check_file_format)
    return parser


def pydabu_main():
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-01-25 (last change).
    """
    # command line arguments:
    parser = my_argument_parser()
    # parse arguments
    args = parser.parse_args()
    if args.subparser_name is not None:
        args.func(args)  # call the programs
    else:  # no sub command given
        parser.print_help()
