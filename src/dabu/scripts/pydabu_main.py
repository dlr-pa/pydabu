"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-10 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import argparse
import os.path

from .check_arg_file_not_exisits import check_arg_file_not_exisits
from .check_arg_file import check_arg_file
from .run_analyse_data_structure import run_analyse_data_structure
from .run_check_file_format import run_check_file_format
from .run_check_netcdf_file import run_check_netcdf_file
from .run_check_nasa_ames_format import run_check_nasa_ames_format
from .run_common_json_format import run_common_json_format
from .run_create_data_bubble import run_create_data_bubble
from .run_check_data_bubble import run_check_data_bubble
from .run_listschemas import run_listschemas


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


def my_argument_parser():
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-10 (last change).
    """
    epilog = ""
    epilog += "You can few the json output for example in firefox, "
    epilog += "e. g. in bash:\n\n"
    epilog += "  output=$(tempfile --suffix='.json'); "
    epilog += "pydabu.py analyse_data_structure -output_format json > "
    epilog += "$output && firefox $output; "
    epilog += "sleep 3; rm $output\n\n"
    epilog += "  output=$(tempfile --suffix='.json'); "
    epilog += "pydabu.py check_netcdf_file -f $(find . -iname '*.nc') "
    epilog += "-output_format json > $output && firefox $output; "
    epilog += "sleep 3; rm $output\n\n"
    epilog += "Author: Daniel Mohr\n"
    epilog += "Date: 2021-02-09\n"
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
        choices=['human_readable', 'json', 'json1'],
        required=False,
        default=['json1'],
        dest='output_format',
        help='Set the output format to use. ' +
        'human_readable gives a nice json output with skipped data. ' +
        'json is the normal json output. json1 is the full data with ' +
        'nice output like human_readable. ' +
        'default: json1',
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
    common_parser2_required = argparse.ArgumentParser(add_help=False)
    common_parser2_required.add_argument(
        '-directory',
        nargs="+",
        type=check_arg_directory,
        required=True,
        dest='directory',
        help='Set the directory to use. ' +
        'You can also give a list of directories separated by space.',
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
    common_parser4 = argparse.ArgumentParser(add_help=False)
    common_parser4.add_argument(
        '-indent',
        nargs=1,
        type=int,
        required=False,
        default=[4],
        dest='indent',
        help='In the output the elements will be indented ' +
        'by this number of spaces.',
        metavar='i')
    # subparsers
    subparsers = parser.add_subparsers(
        dest='subparser_name',
        help='There are different sub-commands with there own flags.')
    # subparser analyse_data_structure
    parser_analyse_data_structure = subparsers.add_parser(
        'analyse_data_structure',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py analyse_data_structure -h',
        description='',
        epilog='',
        parents=[common_parser1, common_parser2])
    parser_analyse_data_structure.set_defaults(func=run_analyse_data_structure)
    # subparser check_nasa_ames_format
    description = 'This command checks a file in the nasa ames format.'
    epilog = 'Example:\n\n'
    epilog += '  pydabu.py check_nasa_ames_format -f a.na > dabu_ames.json\n'
    epilog += '  jsonschema -i dabu_ames.json '
    epilog += '~/lib/python/dabu/schemas/dabu.schema\n'
    epilog += '  jsonschema -i dabu_ames.json '
    epilog += '~/lib/python/dabu/schemas/dabu_requires.schema\n'
    parser_check_nasa_ames_format = subparsers.add_parser(
        'check_nasa_ames_format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py check_nasa_ames_format -h',
        description=description,
        epilog=epilog,
        parents=[common_parser1, common_parser3])
    parser_check_nasa_ames_format.set_defaults(func=run_check_nasa_ames_format)
    # subparser check_netcdf_file
    description = 'This command checks a file in the format netCDF. '
    description += 'It uses the CF Checker: '
    description += 'https://github.com/cedadev/cf-checker'
    epilog = 'Example:\n\n'
    epilog += '  pydabu.py check_netcdf_file -f a.nc > dabu_netcdf.json\n'
    epilog += '  jsonschema -i dabu_netcdf.json '
    epilog += '~/lib/python/dabu/schemas/dabu.schema\n'
    epilog += '  jsonschema -i dabu_netcdf.json '
    epilog += '~/lib/python/dabu/schemas/dabu_requires.schema\n'
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
    description += 'command "analyse_data_structure" does. '
    description += 'Each file is checked by a tool choosen by the '
    description += 'file extension. '
    description += 'For the file extension ".nc" the command '
    description += 'check_netcdf_file is used. '
    epilog = 'Example:\n\n'
    epilog += '  pydabu.py check_file_format -d . > dabu.json\n'
    epilog += '  jsonschema -i dabu.json '
    epilog += '~/lib/python/dabu/schemas/dabu.schema\n'
    epilog += '  jsonschema -i dabu.json '
    epilog += '~/lib/python/dabu/schemas/dabu_requires.schema\n'
    parser_check_file_format = subparsers.add_parser(
        'check_file_format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py check_file_format -h',
        description=description,
        epilog=epilog,
        parents=[common_parser1, common_parser2])
    parser_check_file_format.set_defaults(func=run_check_file_format)
    # subparser common_json_format
    description = 'This command read the given json file and writes it '
    description += 'in a common format to stdout.'
    epilog = 'Example:\n\n'
    epilog += '  pydabu.py common_json_format -f .dabu.json\n\n'
    epilog += '  pydabu.py common_json_format -f .dabu.json > foo\n'
    epilog += '  mv foo .dabu.json\n'
    parser_common_json_format = subparsers.add_parser(
        'common_json_format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py common_json_format -h',
        description=description,
        epilog=epilog,
        parents=[common_parser3, common_parser4])
    parser_common_json_format.set_defaults(func=run_common_json_format)
    # subparser create_data_bubble
    description = 'This command creates a data bubble in the give directory. '
    description += 'The data is generated with the command "check_file_format" '
    description += 'from the data in the directory. '
    description += 'Also the resulting files are not a data management plan, '
    description += 'you can enhance it to become one.'
    epilog = 'Example:\n\n'
    epilog += '  pydabu.py create_data_bubble -d mydata\n\n'
    epilog += '  pydabu.py create_data_bubble -d .\n'
    epilog += '  jsonschema -i .dabu.json .dabu.schema\n'
    parser_create_data_bubble = subparsers.add_parser(
        'create_data_bubble',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py create_data_bubble -h',
        description=description,
        epilog=epilog,
        parents=[common_parser2_required, common_parser4])
    parser_create_data_bubble.set_defaults(func=run_create_data_bubble)
    parser_create_data_bubble.add_argument(
        '-dabu_instance_file',
        nargs=1,
        type=check_arg_file_not_exisits,
        required=False,
        default=['.dabu.json'],   # this is not checked
        dest='dabu_instance_file',
        help='Gives the name of the file describing the content ' +
        'of a data bubble. If this file already exists an erroris raised. ' +
        ' The name is relative to the given directory.',
        metavar='f')
    parser_create_data_bubble.add_argument(
        '-dabu_schema_file',
        nargs=1,
        type=check_arg_file_not_exisits,
        required=False,
        default=['.dabu.schema'],  # this is not checked
        dest='dabu_schema_file',
        help='Gives the name of the file describing the necessary content ' +
        'of a data bubble. If this file already exists an erroris raised. ' +
        ' The name is relative to the given directory.',
        metavar='f')
    # subparser check_data_bubble
    description = 'This command checks a data bubble in the given directory. '
    description += 'The data bubble should be created with '
    description += '"pydabu.py create_data_bubble" and manually enhanced. '
    description += 'Instead of this script you can also use your preferred '
    description += 'tool to check a json instance (e. g. .dabu.json) against '
    description += 'a json schema (e. g. .dabu.schema) -- see examples.'
    epilog = 'Examples:\n\n'
    epilog += '  pydabu.py check_data_bubble -d mydata\n\n'
    epilog += '  cd mydata && jsonschema -i .dabu.json .dabu.schema\n\n'
    parser_check_data_bubble = subparsers.add_parser(
        'check_data_bubble',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py check_data_bubble -h',
        description=description,
        epilog=epilog,
        parents=[common_parser2_required])
    parser_check_data_bubble.set_defaults(func=run_check_data_bubble)
    parser_check_data_bubble.add_argument(
        '-dabu_instance_file',
        nargs=1,
        type=check_arg_file,
        required=False,
        default=['.dabu.json'],   # this is not checked
        dest='dabu_instance_file',
        help='Gives the name of the file describing the content ' +
        'of a data bubble. The name is relative to the given directory.',
        metavar='f')
    parser_check_data_bubble.add_argument(
        '-dabu_schema_file',
        nargs=1,
        type=check_arg_file,
        required=False,
        default=['.dabu.schema'],  # this is not checked
        dest='dabu_schema_file',
        help='Gives the name of the file describing the necessary content ' +
        'of a data bubble. The name is relative to the given directory.',
        metavar='f')
    # subparser listschemas
    description = 'This command lists the provided and used json schemas.'
    epilog = 'Examples:\n\n'
    epilog += '  pydabu.py listschemas\n\n'
    parser_listschemas = subparsers.add_parser(
        'listschemas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py listschemas -h',
        description=description,
        epilog=epilog)
    parser_listschemas.set_defaults(func=run_listschemas)
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
