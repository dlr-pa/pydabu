"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-22, 2021-07-01 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import argparse
import getpass
import os.path
import tempfile

from .check_arg_file_not_exists import check_arg_file_not_exists
from .check_arg_file import check_arg_file
from .run_analyse_data_structure import run_analyse_data_structure
from .run_check_file_format import run_check_file_format
from .run_check_netcdf_file import run_check_netcdf_file
from .run_check_nasa_ames_format import run_check_nasa_ames_format
from .run_common_json_format import run_common_json_format
from .run_create_data_bubble import run_create_data_bubble
from .run_check_data_bubble import run_check_data_bubble
from .run_listschemas import run_listschemas
from .run_data_bubble2jsonld import run_data_bubble2jsonld


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
    :Date: 2021-07-01 (last change).
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
    epilog += "Date: 2021-07-01\n"
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
    common_parser5 = argparse.ArgumentParser(add_help=False)
    common_parser5.add_argument(
        '-skip_creating_checksums',
        action='store_true',
        required=False,
        dest='skip_creating_checksums',
        help='Skip creating checksums, which could take a while.')
    common_parser5.add_argument(
        '-checksum_from_file',
        nargs=1,
        type=check_arg_file,
        required=False,
        dest='checksum_from_file',
        help='Try to get checksums from the given file.',
        metavar='f')
    common_parser6 = argparse.ArgumentParser(add_help=False)
    common_parser6.add_argument(
        '-dabu_instance_file',
        nargs=1,
        type=check_arg_file,
        required=False,
        default=['.dabu.json'],   # this is not checked
        dest='dabu_instance_file',
        help='Gives the name of the file describing the content ' +
        'of a data bubble. The name is relative to the given directory.',
        metavar='f')
    common_parser6.add_argument(
        '-dabu_schema_file',
        nargs=1,
        type=check_arg_file,
        required=False,
        default=['.dabu.schema'],  # this is not checked
        dest='dabu_schema_file',
        help='Gives the name of the file describing the necessary content ' +
        'of a data bubble. The name is relative to the given directory.',
        metavar='f')
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
    epilog = 'Examples:\n\n'
    epilog += '  pydabu.py check_file_format -d . > dabu.json\n'
    epilog += '  jsonschema -i dabu.json '
    epilog += '~/lib/python/dabu/schemas/dabu.schema\n'
    epilog += '  jsonschema -i dabu.json '
    epilog += '~/lib/python/dabu/schemas/dabu_requires.schema\n\n'
    epilog += '  pydabu.py check_file_format -skip_creating_checksums\n\n'
    epilog += '  pydabu.py check_file_format -checksum_from_file .checksum.sha512'
    parser_check_file_format = subparsers.add_parser(
        'check_file_format',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py check_file_format -h',
        description=description,
        epilog=epilog,
        parents=[common_parser1, common_parser2, common_parser5])
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
    epilog += '  pydabu.py create_data_bubble -dir .\n'
    epilog += '  jsonschema -i .dabu.json .dabu.schema\n'
    parser_create_data_bubble = subparsers.add_parser(
        'create_data_bubble',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py create_data_bubble -h',
        description=description,
        epilog=epilog,
        parents=[common_parser2_required, common_parser4, common_parser5])
    parser_create_data_bubble.set_defaults(func=run_create_data_bubble)
    parser_create_data_bubble.add_argument(
        '-dabu_instance_file',
        nargs=1,
        type=check_arg_file_not_exists,
        required=False,
        default=['.dabu.json'],   # this is not checked
        dest='dabu_instance_file',
        help='Gives the name of the file describing the content ' +
        'of a data bubble. If this file already exists an error is raised. ' +
        'The name is relative to the given directory.',
        metavar='f')
    parser_create_data_bubble.add_argument(
        '-dabu_schema_file',
        nargs=1,
        type=check_arg_file_not_exists,
        required=False,
        default=['.dabu.schema'],  # this is not checked
        dest='dabu_schema_file',
        help='Gives the name of the file describing the necessary content ' +
        'of a data bubble. If this file already exists an error is raised. ' +
        'The name is relative to the given directory.',
        metavar='f')
    # subparser check_data_bubble
    description = 'This command checks a data bubble in the given directory. '
    description += 'The data bubble should be created with '
    description += '"pydabu.py create_data_bubble" and manually enhanced. '
    description += 'Instead of this script you can also use your preferred '
    description += 'tool to check a json instance (e. g. .dabu.json) against '
    description += 'a json schema (e. g. .dabu.schema) -- see examples.'
    epilog = 'Examples:\n\n'
    epilog += '  pydabu.py check_data_bubble -dir mydata\n\n'
    epilog += '  cd mydata && jsonschema -i .dabu.json .dabu.schema\n\n'
    parser_check_data_bubble = subparsers.add_parser(
        'check_data_bubble',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py check_data_bubble -h',
        description=description,
        epilog=epilog,
        parents=[common_parser2_required, common_parser6])
    parser_check_data_bubble.set_defaults(func=run_check_data_bubble)
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
    # the following artificial parameter is necessary to build the documentation
    # with sphinx-argparse or rather sphinxarg.ext
    parser_listschemas.add_argument(
        '-output_format',
        nargs=1,
        type=str,
        choices=['simple', 'json'],
        required=False,
        default=['simple'],
        dest='output_format',
        help='Set the output format to use. ' +
        'simple lists the json schmeas in lines. ' +
        'json leads to a json output. ' +
        'default: simple',
        metavar='f')
    # subparser data_bubble2jsonld
    description = 'This command reads the data bubble '
    description += '(.dabu.json and .dabu.schema) and creates a '
    description += 'json-ld data bubble '
    description += '(.dabu.json-ld and .dabu.json-ld.schema). '
    description += 'If you are fine with these new files, you should delete '
    description += 'the old ones by youself.'
    epilog = 'Examples:\n\n'
    epilog += '  pydabu.py data_bubble2jsonld -dir .\n\n'
    epilog += '  pydabu.py data_bubble2jsonld -dir . -author "Daniel Mohr"\n\n'
    epilog += '  pydabu.py data_bubble2jsonld -dir . -author \'{"name": "Daniel Mohr", "identifier": {"propertyID": "https://orcid.org/", "name": "ORCID", "value": "0000-0002-9382-6586", "url": "https://orcid.org/0000-0002-9382-6586"}}\'\n\n'
    epilog += '  pydabu.py data_bubble2jsonld -dir . -author \'[{"name": "er"}, {"name": "sie"}, {"name": "es"}]\'\n\n'
    epilog += 'Example to check the result:\n\n'
    epilog += '  pydabu.py check_data_bubble -dir . '
    epilog += '-dabu_instance_file .dabu.json-ld '
    epilog += '-dabu_schema_file .dabu.json-ld.schema\n\n'
    parser_data_bubble2jsonld = subparsers.add_parser(
        'data_bubble2jsonld',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        help='For more help: pydabu.py data_bubble2jsonld -h',
        description=description,
        epilog=epilog,
        parents=[common_parser2_required, common_parser4, common_parser6])
    parser_data_bubble2jsonld.set_defaults(func=run_data_bubble2jsonld)
    parser_data_bubble2jsonld.add_argument(
        '-dabu_jsonld_instance_file',
        nargs=1,
        type=check_arg_file_not_exists,
        required=False,
        default=['.dabu.json-ld'],   # this is not checked
        dest='dabu_jsonld_instance_file',
        help='Gives the name of the file describing the content ' +
        'of a data bubble as jsonld. ' +
        'If this file already exists an error is raised. ' +
        'The name is relative to the given directory. ' +
        'default: .dabu.json-ld',
        metavar='f')
    parser_data_bubble2jsonld.add_argument(
        '-dabu_jsonld_schema_file',
        nargs=1,
        type=check_arg_file_not_exists,
        required=False,
        default=['.dabu.json-ld.schema'],  # this is not checked
        dest='dabu_jsonld_schema_file',
        help='Gives the name of the file describing the necessary content ' +
        'of a data bubble with json-ld. ' +
        'If this file already exists an error is raised. ' +
        'The name is relative to the given directory. ' +
        'default: .dabu.json-ld.schema',
        metavar='f')
    parser_data_bubble2jsonld.add_argument(
        '-vocabulary',
        nargs=1,
        type=str,
        choices=['schema.org'],
        required=False,
        default=['schema.org'],
        dest='vocabulary',
        help='Sets the vocabulary to use. ' +
        'At the moment only schema.org is implemented. ' +
        'default: schema.org',
        metavar='v')
    cachefilename = 'schemaorg-current-https.jsonld.bz2'
    parser_data_bubble2jsonld.add_argument(
        '-cachefilename',
        nargs=1,
        type=str,
        required=False,
        default=[cachefilename],
        dest='cachefilename',
        help='We need data from schema.org. '
        'If you set cachefilename to an empty string, nothing is cached. '
        'If the file ends with common extension for compression, '
        'this comperession is used (e. g.: .gz, .lzma, .xz, .bz2). '
        'The file is created in the cachefilepath (see this option). '
        'default: "%s"' % cachefilename,
        metavar='f')
    cachefilepath = os.path.join(
        tempfile.gettempdir(),
        'json_schema_from_schema_org_' + getpass.getuser())
    parser_data_bubble2jsonld.add_argument(
        '-cachefilepath',
        nargs=1,
        type=str,
        required=False,
        default=[cachefilepath],
        dest='cachefilepath',
        help='This path is used for the cachefilename. '
        'If necessary, this directory will be created '
        '(not the directory tree!). '
        'default: "%s"' % cachefilepath,
        metavar='p')
    parser_data_bubble2jsonld.add_argument(
        '-author',
        nargs=1,
        type=str,
        required=False,
        dest='author',
        help='Sets the author of the data bubble. ' +
        'If not given, it is not added to the dabu_jsonld_instance_file. ' +
        'Anyway the dabu_jsonld_schema_file will require it. ' +
        'You can just give a string or any json object.',
        metavar='p')
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
