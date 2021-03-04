"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-04 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import argparse
import os.path
import tempfile


def argument_parser():
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-03-04 (last change).
    """
    epilog = ""
    epilog += "Author: Daniel Mohr\n"
    epilog += "Date: 2021-03-04\n"
    epilog += "License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007."
    epilog += "\n\n"
    description = 'json_schema_from_schema_org.py is a script ' \
        'to define json-ld based on schema.org as a json schema.'
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'vocabulary',
        nargs='+',
        type=str,
        help='For these words from schema.org the output is generated.',
        metavar='word')
    parser.add_argument(
        '-indent',
        nargs=1,
        type=int,
        required=False,
        default=[4],
        dest='indent',
        help='In the output the elements will be indented ' +
        'by this number of spaces.',
        metavar='i')
    cachefilename = os.path.join(
        tempfile.gettempdir(),
        'json_schema_from_schema_org_schemaorg-current-https.jsonld.lzma')
    parser.add_argument(
        '-cachefilename',
        nargs=1,
        type=str,
        required=False,
        default=[cachefilename],
        dest='cachefilename',
        help='We need data from schema.org. '
        'If you set cachefilename to an empty string, nothing is cached. '
        'If the file ends with common extension for compression, '
        'this comperession is used (e. g.: .gz, .lzma, .xz, .bz2).'
        'default: "%s"' % cachefilename,
        metavar='f')
    return parser
