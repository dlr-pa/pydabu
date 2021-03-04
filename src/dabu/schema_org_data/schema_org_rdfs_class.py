"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-04 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

from .add_context import add_context
from .domainIncludes import domainIncludes
from .type_from_schema_id import type_from_schema_id


def schema_org_rdfs_class(item, new_schema, data):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-04
    """
    missing_types = []
    subclasses = []
    for i in data:
        if domainIncludes(i, "schema:" + item):
            # found property
            prop_name = i["@id"].split(':')[1]
            add_context(new_schema[item], item, "https://schema.org/")
            new_schema[item]["properties"][prop_name] = dict()
            if ("schema:rangeIncludes" in i):
                missing_type = None
                if isinstance(i["schema:rangeIncludes"], dict):
                    missing_type = type_from_schema_id(
                        i["schema:rangeIncludes"]["@id"],
                        new_schema[item]["properties"][prop_name],
                        i)
                elif isinstance(i["schema:rangeIncludes"], list):
                    new_schema[item]["properties"][prop_name]["oneOf"] = \
                        list()
                    for element in i["schema:rangeIncludes"]:
                        new_schema[item]["properties"][prop_name]["oneOf"].append(
                            dict())
                        missing_type = type_from_schema_id(
                            element["@id"],
                            new_schema[item]["properties"][prop_name]["oneOf"][-1],
                            i)
                else:
                    raise NotImplementedError(
                        f'do not understand "schema:rangeIncludes" in:\n{i}')
                if missing_type is not None:
                    missing_types.append(missing_type)
            else:
                raise NotImplementedError(
                    f'no "schema:rangeIncludes" in:\n\n{i}')
    return missing_types
