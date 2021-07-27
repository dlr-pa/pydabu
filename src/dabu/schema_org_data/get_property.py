"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json

from dabu.compare_json_schemas import compare_json_schemas

from .get_graph_item import get_graph_item


def _are_types_equal(type1, type2):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-19
    """
    iseq = True
    try:
        compare_json_schemas(type1, type2)
    except AssertionError:
        iseq = False
    return iseq


def create_properties_schema2json(
        properties, schema2json, prop_name, word, item_type):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-19
    """
    value = "https://schema.org/" + word
    if prop_name not in properties:
        properties[prop_name] = dict()
        store_prop = properties[prop_name]
    else:
        if isinstance(properties[prop_name], dict):
            if "oneOf" not in properties[prop_name]:
                if (("@id" in properties[prop_name]) and
                        (properties[prop_name]["@id"] == value)):
                    return
                properties[prop_name] = {"oneOf": [properties[prop_name]]}
                properties[prop_name]["oneOf"].append(dict())
                store_prop = properties[prop_name]["oneOf"][-1]
            else:  # properties[prop_name]["oneOf"] is list
                newtype = dict()
                newtype["@id"] = value
                if isinstance(schema2json[item_type], str):
                    newtype["type"] = schema2json[item_type]
                else:  # dict
                    for key in schema2json[item_type]:
                        newtype[key] = schema2json[item_type][key]
                for item in properties[prop_name]["oneOf"]:
                    if _are_types_equal(newtype, item):
                        return
                properties[prop_name]["oneOf"].append(dict())
                store_prop = properties[prop_name]["oneOf"][-1]
        else:
            raise NotImplementedError(json.dumps(properties, indent=2))
    store_prop["@id"] = value
    if isinstance(schema2json[item_type], str):
        store_prop["type"] = schema2json[item_type]
    else:  # dict
        for key in schema2json[item_type]:
            store_prop[key] = schema2json[item_type][key]


def create_properties_handle(
        properties, prop_name, missing_words, item_type_ref):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-17
    """
    value = "#/definitions/" + item_type_ref
    if prop_name not in properties:
        properties[prop_name] = dict()
        store_prop = properties[prop_name]
    else:
        if isinstance(properties[prop_name], dict):
            if "oneOf" not in properties[prop_name]:
                if (("$ref" in properties[prop_name]) and
                        (properties[prop_name]["$ref"] == value)):
                    return
                properties[prop_name] = {"oneOf": [properties[prop_name]]}
            else:  # properties[prop_name]["oneOf"] is list
                for item in properties[prop_name]["oneOf"]:
                    if (("$ref" in item) and
                            (item["$ref"] == value)):
                        return
            properties[prop_name]["oneOf"].append(dict())
            store_prop = properties[prop_name]["oneOf"][-1]
        else:
            raise NotImplementedError(json.dumps(properties, indent=2))
    store_prop["$ref"] = value
    missing_words.append(item_type_ref)


def _rangeincludes_list(data, schema2json, handle):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-17
    """
    accept_list = []
    if "schema:rangeIncludes" not in data:
        return None
    if not isinstance(data["schema:rangeIncludes"], list):
        return None
    for item in data["schema:rangeIncludes"]:
        if "@id" in item:
            item_type = item["@id"].split('schema:')[1]
            if ((item_type in schema2json) or (item_type in handle)):
                accept_list.append(item_type)
    return accept_list


def _get_property(item, data, properties, prop_name,
                  missing_words, draft='draft-04'):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-19
    """
    # schema.org datatypes to handle ("schema:DataType"):
    schema2json = {"Text": "string",
                   "Boolean": "boolean",
                   "Integer": "integer",
                   "Number": "number",
                   "Float": "number",
                   "URL": {"type": "string", "format": "uri"},
                   "DateTime": {"type": "string", "format": "date-time"},
                   "Date": {"type": "string", "format": "date-time"},
                   "Time": "string",
                   "email": {"oneOf": [{"type": "string"},
                                       {"type": "string", "format": "email"}]}}
    if draft in ['draft-06']:
        schema2json["URL"] = {
            "oneOf": [{"type": "string", "format": "uri"},
                      {"type": "string", "format": "uri-reference"}]}
    if draft in ['draft-07', '2019-09']:
        schema2json["Date"] = {"type": "string", "format": "date"}
        schema2json["Time"] = {"type": "string", "format": "datetime"}
        schema2json["email"] = {
            "oneOf": [{"type": "string"},
                      {"type": "string", "format": "email"},
                      {"type": "string", "format": "idn-email"}]}
        schema2json["URL"] = {
            "oneOf": [{"type": "string", "format": "uri"},
                      {"type": "string", "format": "uri-reference"},
                      {"type": "string", "format": "iri"},
                      {"type": "string", "format": "iri-reference"}]}
    handle = ["ImageObject", "MediaObject",
              "Distance", "CreativeWork",
              "DefinedTerm",
              "Thing", "Person",
              "Place", "Comment",
              "DataCatalog", "Dataset", "DataDownload",
              "Organization", "AdministrativeArea", "VirtualLocation",
              "EducationalOrganization", "Photograph", "CorrectionComment",
              "AudioObject", "Brand", "ContactPoint", "Language", "Occupation",
              "hasOfferCatalog", "OfferCatalog", "InteractionCounter", "Offer",
              "ProgramMembership", "Country", "MonetaryAmount",
              "PriceSpecification", "OwnershipInfo", "Product", "Event",
              "Demand", "QuantitativeValue", "PropertyValue"]
    word = data["@id"].split('schema:')[1]
    if word in schema2json:
        create_properties_schema2json(
            properties, schema2json, prop_name, word, word)
    elif (("schema:rangeIncludes" in data) and
          ("@id" in data["schema:rangeIncludes"]) and
          (data["schema:rangeIncludes"]["@id"].split('schema:')[1] in
           schema2json)):
        # e. g.: faxNumber
        create_properties_schema2json(
            properties, schema2json, word, prop_name,
            data["schema:rangeIncludes"]["@id"].split('schema:')[1])
    elif item["@id"].split('schema:')[1] in handle:
        create_properties_handle(
            properties, prop_name, missing_words,
            item["@id"].split('schema:')[1])
    elif (("schema:rangeIncludes" in data) and
          ("@id" in data["schema:rangeIncludes"]) and
          (data["schema:rangeIncludes"]["@id"].split('schema:')[1] in
           handle)):
        # e. g.: follows
        create_properties_handle(
            properties, prop_name, missing_words,
            data["schema:rangeIncludes"]["@id"].split('schema:')[1])
    else:
        accept_list = _rangeincludes_list(data, schema2json, handle)
        if accept_list is not None:
            if len(accept_list) > 1:
                for item_type in accept_list:
                    if item_type in schema2json:
                        create_properties_schema2json(
                            properties, schema2json, word, prop_name,
                            item_type)
                    elif item_type in handle:
                        create_properties_handle(
                            properties, prop_name, missing_words, item_type)
            elif len(accept_list) == 1:
                item_type = accept_list[0]
                if item_type in schema2json:
                    create_properties_schema2json(
                        properties, schema2json, word, prop_name, item_type)
                elif item_type in handle:
                    create_properties_handle(
                        properties, prop_name, missing_words, item_type)
        else:
            pass  # not implemented now


def get_property(schemaorg_data, properties, prop_name, missing_words,
                 draft='draft-04'):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-19
    """
    data = get_graph_item(schemaorg_data, prop_name)
    if ("@type" in data) and (data["@type"] == "rdfs:Class"):
        new_missing_word = data["@id"].split('schema:')[1]
        properties[prop_name] = dict()
        properties[prop_name]["$ref"] = "#/definitions/" + new_missing_word
        missing_words.append(new_missing_word)
        return None
    elif ("@type" in data) and (data["@type"] == "rdf:Property"):
        if "schema:rangeIncludes" in data:
            if isinstance(data["schema:rangeIncludes"], dict):
                if "@id" not in data["schema:rangeIncludes"]:
                    raise NotImplementedError(json.dumps(data, indent=2))
                _get_property(
                    data["schema:rangeIncludes"], data,
                    properties, prop_name, missing_words, draft)
            elif isinstance(data["schema:rangeIncludes"], list):
                for item in data["schema:rangeIncludes"]:
                    _get_property(
                        item, data, properties, prop_name,
                        missing_words, draft)
            else:
                raise NotImplementedError(json.dumps(data, indent=2))
        else:
            raise NotImplementedError(json.dumps(data, indent=2))
    else:
        raise NotImplementedError(json.dumps(data, indent=2))
    return None
