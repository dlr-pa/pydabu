"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-04 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import warnings


def add_context(schema, context, baseuri="https://schema.org/"):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-04

    This function add a json schema for context to the schema.

    :param schema: The context will be added to this schema.
    :param context: context/word/vocable
    :param baseuri: base uri where the context is described
    """
    if not baseuri.endswith("/"):
        baseuri += "/"
    if "@context" not in schema:
        schema["@context"] = dict()
    if "required" not in schema:
        schema["required"] = ["@context"]
    elif "@context" not in schema["required"]:
        if not isinstance(schema["required"], list):
            schema["required"] = list(schema["required"])
        schema["required"].append("@context")
    if "properties" not in schema:
        schema["properties"] = dict()
    if "@context" not in schema["properties"]:
        schema["properties"]["@context"] = dict()
    if "required" not in schema["properties"]["@context"]:
        schema["properties"]["@context"]["required"] = list()
    if context in schema["properties"]["@context"]["required"]:
        warnings.warn('context already stored, will be overwritten')
    else:
        schema["properties"]["@context"]["required"].append(context)
    if "properties" not in schema["properties"]["@context"]:
        schema["properties"]["@context"]["properties"] = dict()
    schema["properties"]["@context"]["properties"][context] = dict()
    schema["properties"]["@context"]["properties"][context]["type"] = "string"
    schema["properties"]["@context"]["properties"][context]["enum"] = \
      [baseuri + context]
    #schema["properties"]["@context"]["properties"][context]["pattern"] = \
    #    "^" + baseuri + context + "$"
