"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-09 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json

import dabu.schema_org_data

from .argument_parser import argument_parser


# pylint: disable=invalid-name
def json_schema_from_schema_org_main():
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09
    """
    # command line arguments:
    parser = argument_parser()
    # parse arguments
    args = parser.parse_args()
    schema_org_data = dabu.schema_org_data.get_schema_org_data(
        args.cachefilepath[0], args.cachefilename[0])
    new_schema = dabu.schema_org_data.json_schema_from_schema_org(
        schema_org_data, args.vocabulary, draft='draft-04')
    print(json.dumps(new_schema, indent=args.indent[0]))
