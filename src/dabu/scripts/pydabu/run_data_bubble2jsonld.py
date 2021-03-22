"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-22 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json
import jsonschema
import os.path
import sys

import dabu.schema_org_data

from .check_arg_file import check_arg_file
from .check_arg_file_not_exists import check_arg_file_not_exists


def run_data_bubble2jsonld(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-03-22 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    for path in args.directory:  # for every given directory
        check_arg_file(os.path.join(path, args.dabu_instance_file[0]))
        check_arg_file(os.path.join(path, args.dabu_schema_file[0]))
        check_arg_file_not_exists(
            os.path.join(path, args.dabu_jsonld_instance_file[0]))
        check_arg_file_not_exists(
            os.path.join(path, args.dabu_jsonld_schema_file[0]))
    if args.vocabulary[0] == 'schema.org':
        sys.stderr.write('read vocabularay:\n')
        schema_org_data = dabu.schema_org_data.get_schema_org_data(
            args.cachefilepath[0], args.cachefilename[0])
        jsonld_schema = dabu.schema_org_data.json_schema_from_schema_org(
            schema_org_data, ['DataCatalog'],
            draft='draft-04')
        sys.stderr.write('read vocabularay.\n\n')
    for path in args.directory:  # for every given directory
        with open(os.path.join(path, args.dabu_instance_file[0]),
                  mode='r') as fd:
            instance = json.load(fd)
        with open(os.path.join(path, args.dabu_schema_file[0]),
                  mode='r') as fd:
            schema = json.load(fd)
        validater = jsonschema.Draft4Validator(schema)
        # we should call run_check_data_bubble here!
        dabu.schema_org_data.combine(schema, jsonld_schema)
        validater = jsonschema.Draft4Validator(schema)
        schema["required"].append("@type")
        instance["@type"] = "DataCatalog"
        schema["required"].append("type")
        instance["type"] = "DataCatalog"
        schema["properties"]["DataCatalog"] = {
            "$ref": "#/definitions/DataCatalog"}
        schema["required"].append("author")
        instance["@context"] = dict()
        prop = schema["properties"]["@context"]["properties"]
        for key in schema["properties"]["@context"]["required"]:
            instance["@context"][key] = prop[key]["enum"][0]
        if args.author is not None:
            try:
                author = json.loads(args.author[0])
            except json.JSONDecodeError:
                author = {"name": args.author[0]}
            instance["author"] = author
        if "data" in instance:
            instance["dataset"] = instance["data"]
            del instance["data"]
        del schema["properties"]["data"]
        if isinstance(schema["$schema"], list):
            index = len(schema["$schema"]) - 1
            while 0 < index:
                item = schema["$schema"][index]
                nindex = schema["$schema"].index(
                    schema["$schema"][index])
                if nindex != index:
                    schema["$schema"].pop(index)
                index -= 1
            if len(schema["$schema"]) == 1:
                schema["$schema"] = schema["$schema"][0]
        with open(os.path.join(path, args.dabu_jsonld_instance_file[0]),
                  mode='w') as fd:
            json.dump(instance, fd, indent=args.indent[0])
        with open(os.path.join(path, args.dabu_jsonld_schema_file[0]),
                  mode='w') as fd:
            json.dump(schema, fd, indent=args.indent[0])
