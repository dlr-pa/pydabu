"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-23, 2021-07-29 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json
import os.path
import sys
import types

import jsonschema

import dabu.schema_org_data

from .check_arg_file import check_arg_file
from .check_arg_file_not_exists import check_arg_file_not_exists
from .run_check_data_bubble import run_check_data_bubble


def run_data_bubble2jsonld(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-03-23 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    # pylint: disable=too-many-branches
    # pylint: disable=too-many-statements
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
            dabuinstance = json.load(fd)
        with open(os.path.join(path, args.dabu_schema_file[0]),
                  mode='r') as fd:
            schema = json.load(fd)
        jsonschema.Draft4Validator(schema)
        # call run_check_data_bubble:
        sys.stderr.write(
            f'run: pydabu.py check_data_bubble -directory {path}\n')
        check_data_bubble_args = types.SimpleNamespace()
        check_data_bubble_args.directory = [path]
        check_data_bubble_args.dabu_instance_file = args.dabu_instance_file
        check_data_bubble_args.dabu_schema_file = args.dabu_schema_file
        if not run_check_data_bubble(args):
            sys.stderr.write(
                f'your data bubble at {path} is not valid. exit.\n')
            exit()
        sys.stderr.write(' ok\n')
        # create json-ld output:
        # create schema
        for key in ["title", "description"]:
            del jsonld_schema[key]
        del schema["type"]
        jsonld_schema["definitions"]["DataCatalog"]["allOf"].append(
            schema["properties"])
        del schema["properties"]
        if "required" not in jsonld_schema["definitions"]["DataCatalog"]:
            jsonld_schema["definitions"]["DataCatalog"]["required"] = []
        required = jsonld_schema["definitions"]["DataCatalog"]["required"]
        for prop in schema["required"]:
            if prop not in required:
                required.append(prop)
        if not bool(jsonld_schema["definitions"]["DataCatalog"]["required"]):
            del jsonld_schema["definitions"]["DataCatalog"]["required"]
        schema["required"] = ["DataCatalog"]
        jsonld_schema["definitions"]["DataCatalog"]["dependencies"] = \
            schema["dependencies"]
        del schema["dependencies"]
        dabu.schema_org_data.combine(schema, jsonld_schema)
        del jsonld_schema
        if isinstance(schema["$schema"], list):
            index = len(schema["$schema"]) - 1
            while index > 0:
                nindex = schema["$schema"].index(
                    schema["$schema"][index])
                if nindex != index:
                    schema["$schema"].pop(index)
                index -= 1
            if len(schema["$schema"]) == 1:
                schema["$schema"] = schema["$schema"][0]
        schema["properties"]["DataCatalog"] = {"$ref":
                                               "#/definitions/DataCatalog"}
        # create instance
        jsonld_instance = dict()
        jsonld_instance["DataCatalog"] = dabuinstance
        if "data" in jsonld_instance["DataCatalog"]:
            jsonld_instance["DataCatalog"]["dataset"] = \
                jsonld_instance["DataCatalog"]["data"]
            del jsonld_instance["DataCatalog"]["data"]
        jsonld_instance["@context"] = dict()
        prop = schema["properties"]["@context"]["properties"]
        for key in schema["properties"]["@context"]["required"]:
            jsonld_instance["@context"][key] = prop[key]["enum"][0]
        if args.author is not None:
            try:
                author = json.loads(args.author[0])
            except json.JSONDecodeError:
                author = {"name": args.author[0]}
            jsonld_instance["DataCatalog"]["author"] = author

        with open(os.path.join(path, args.dabu_jsonld_instance_file[0]),
                  mode='w') as fd:
            json.dump(jsonld_instance, fd, indent=args.indent[0])
        with open(os.path.join(path, args.dabu_jsonld_schema_file[0]),
                  mode='w') as fd:
            json.dump(schema, fd, indent=args.indent[0])
