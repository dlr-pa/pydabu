"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-01-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import argparse
import os.path

from .run_check_data_structure import run_check_data_structure

def check_arg_directory(data):
    if not os.path.isdir(data):
        msg = '"%s" is not a directory' % data
        raise argparse.ArgumentTypeError(msg)
    return data

def pydabu_main():
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-01-19 (last change).
    """
    # command line arguments:
    epilog = ""
    epilog += "Author: Daniel Mohr\n"
    epilog += "Date: 2021-01-19\n"
    epilog += "License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007."
    epilog += "\n\n"
    parser = argparse.ArgumentParser(
        description='pydabu.py is a script to check a data bubble.',
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    # parent parser to describe common argument
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument(
        '-directory',
        nargs="+",
        type=check_arg_directory,
        required=False,
        default=['.'], # this is not checked against the required type
        dest='directory',
        help='Set the directory to use. ' +
        'You can also give a list of directories separated by space. ' +
        'default: .',
        metavar='d')
    parent_parser.add_argument(
        '-output_format',
        nargs="+",
        type=str,
        choices=['human_readable', 'json'],
        required=False,
        default=['human_readable'],
        dest='output_format',
        help='Set the output format to use. ' +
        'default: json',
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
        parents=[parent_parser])
    parser_check_data_structure.set_defaults(func=run_check_data_structure)
    # -directory
    # parse arguments
    args = parser.parse_args()
    if args.subparser_name is not None:
        args.func(args)  # call the programs
    else:  # no sub command given
        parser.print_help()
