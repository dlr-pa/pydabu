"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json
import sys

from dabu.compare_json_schemas import compare_json_schemas
from .ispending import ispending


def set_property(schema, key, value):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16
    """
    schema[key] = value


def add_property(schema, key, value):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16
    """
    if key in schema:
        if isinstance(schema[key], dict):
            if isinstance(value, dict):
                combine(schema[key], value)
            elif isinstance(value, list):
                raise TypeError('no idea how to merge list in dict')
            else:  # string, int, float, bool or None
                raise TypeError(
                    'no idea to merge none interabel in dict')
        elif isinstance(schema[key], list):
            if isinstance(value, dict):
                raise TypeError('no idea how to merge dict in list')
            elif isinstance(value, list):
                schema[key] = list(set(schema[key] + value))
            else:  # string, int, float, bool or None
                if not value in schema[key]:
                    schema[key].append(value)
        else:  # string, int, float, bool or None
            if isinstance(value, dict):
                schema[key] = [schema[key], value]
            elif isinstance(value, list):
                schema[key] = [schema[key]] + \
                    value
            else:  # string, int, float, bool or None
                schema[key] = [schema[key], value]
    else:
        set_property(schema, key, value)


def combine(json_instance1, json_instance2):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16

    This function combines/merges 2 json instances. 
    Each are a combination of dicts and lists.

    :param json_instance1: json_instance
    :param json_instance2: json_instance, which is merged into json_instance1
    """
    for key in json_instance2:
        add_property(json_instance1, key, json_instance2[key])


def get_graph_item(schemaorg_data, word):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16
    """
    for item in schemaorg_data['@graph']:
        if ("@id" in item) and (item["@id"] == "schema:" + word):
            return item
    return None


def create_context_schema(word):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16
    """
    context = dict()
    context["required"] = [word]
    context["properties"] = {word: {"type": "string",
                                    "enum": ["https://schema.org/" + word]}}
    return context


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
            if not "oneOf" in properties[prop_name]:
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
            raise NotImplementedError(json.dumps(data, indent=2))
    store_prop["@id"] = value
    if isinstance(schema2json[item_type], str):
        store_prop["type"] = schema2json[item_type]
    else:  # dict
        for key in schema2json[item_type]:
            store_prop[key] = schema2json[item_type][key]


def create_properties_handle(
        properties, prop_name, missing_words, word, item_type_ref):
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
            if not "oneOf" in properties[prop_name]:
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
            raise NotImplementedError(json.dumps(data, indent=2))
    store_prop["$ref"] = value
    missing_words.append(item_type_ref)


def _rangeincludes_list(data, schema2json, handle):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-17
    """
    accept_list = []
    if not ("schema:rangeIncludes" in data):
        return None
    if not isinstance(data["schema:rangeIncludes"], list):
        return None
    for item in data["schema:rangeIncludes"]:
        if "@id" in item:
            item_type = item["@id"].split('schema:')[1]
            if ((item_type in schema2json) or (item_type in handle)):
                accept_list.append(item_type)
    return accept_list


def _get_property(item, data, schema2json, properties, prop_name,
                  missing_words):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-18
    """
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
        # faxNumber
        create_properties_schema2json(
            properties, schema2json, word, prop_name,
            data["schema:rangeIncludes"]["@id"].split('schema:')[1])
    elif item["@id"].split('schema:')[1] in handle:
        create_properties_handle(
            properties, prop_name, missing_words, word,  item["@id"].split('schema:')[1])
    elif (("schema:rangeIncludes" in data) and
          ("@id" in data["schema:rangeIncludes"]) and
          (data["schema:rangeIncludes"]["@id"].split('schema:')[1] in
           handle)):
        # follows
        create_properties_handle(
            properties, prop_name, missing_words, word,
            data["schema:rangeIncludes"]["@id"].split('schema:')[1])
    else:
        accept_list = _rangeincludes_list(data, schema2json, handle)
        if accept_list is not None:
            if len(accept_list) > 1:
                for item_type in accept_list:
                    if item_type in schema2json:
                        create_properties_schema2json(
                            properties, schema2json, word, prop_name, item_type)
                    elif item_type in handle:
                        create_properties_handle(
                            properties, prop_name, missing_words,
                            word, item_type)
            elif len(accept_list) == 1:
                item_type = accept_list[0]
                if item_type in schema2json:
                    create_properties_schema2json(
                        properties, schema2json, word, prop_name, item_type)
                elif item_type in handle:
                    create_properties_handle(
                        properties, prop_name, missing_words, word, item_type)
        else:
            pass  # not implemented now


def get_property(schemaorg_data, properties, prop_name, missing_words,
                 draft='draft-04'):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-18

    data:

    {
      "@id": "schema:additionalName",
      "@type": "rdf:Property",
      "rdfs:comment": "An additional name for a Person, can be used for a middle name.",
      "rdfs:label": "additionalName",
      "schema:domainIncludes": {
        "@id": "schema:Person"
      },
      "schema:rangeIncludes": {
        "@id": "schema:Text"
      }
    },
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
    schema2json7 = {"Date": {"type": "string", "format": "date"},
                    "Time": {"type": "string", "format": "datetime"}}
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
                if not "@id" in data["schema:rangeIncludes"]:
                    raise NotImplementedError(json.dumps(data, indent=2))
                _get_property(
                    data["schema:rangeIncludes"], data, schema2json,
                    properties, prop_name, missing_words)
            elif isinstance(data["schema:rangeIncludes"], list):
                for item in data["schema:rangeIncludes"]:
                    _get_property(
                        item, data, schema2json, properties, prop_name,
                        missing_words)
            else:
                raise NotImplementedError(json.dumps(data, indent=2))
        else:
            raise NotImplementedError(json.dumps(data, indent=2))
    elif "@type":
        raise NotImplementedError(json.dumps(data, indent=2))
    return None


def add_property_to_object(schemaorg_data, item, domainIncludes, word, properties, missing_words):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16
    """
    if not "@id" in domainIncludes:
        raise NotImplementedError(json.dumps(item, indent=2))
    elif domainIncludes["@id"] == "schema:" + word:
        if not "@id" in item:
            raise NotImplementedError(json.dumps(data, indent=2))
        prop_name = item["@id"].split('schema:')[1]  # e. g.: additionalName
        get_property(schemaorg_data, properties, prop_name, missing_words)
    # if item["@type"] == "rdf:Property":
    #    pass


def add_properties_to_object(schemaorg_data, word, properties, missing_words):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16

    item:

    {
      "@id": "schema:additionalName",
      "@type": "rdf:Property",
      "rdfs:comment": "An additional name for a Person, can be used for a middle name.",
      "rdfs:label": "additionalName",
      "schema:domainIncludes": {
        "@id": "schema:Person"
      },
      "schema:rangeIncludes": {
        "@id": "schema:Text"
      }
    },
    """
    for item in schemaorg_data['@graph']:
        if (("schema:domainIncludes" in item) and (not ispending(item))):
            if isinstance(item["schema:domainIncludes"], dict):
                add_property_to_object(
                    schemaorg_data, item, item["schema:domainIncludes"],
                    word, properties, missing_words)
            elif isinstance(item["schema:domainIncludes"], list):
                for subitem in item["schema:domainIncludes"]:
                    add_property_to_object(
                        schemaorg_data, item, subitem, word, properties,
                        missing_words)
            else:
                raise NotImplementedError(json.dumps(item, indent=2))
            # and (item["@id"] == "schema:" + word):


def add_word(schemaorg_data, word, draft='draft-04'):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16

    This function generates a json schema from https://schema.org , which
    desribes the given word.

    :param schemaorg_data: json-ld data from https://schema.org as returned
                           from :func:`get_schema_org_data`.
    :param word: word, which are a Schema.org Type (Schema.org vocabulary)
    :param draft: the used json schema, could be:

                  * 'draft-04'
                  * 'draft-06'
                  * 'draft-07'
                  * '2019-09'
    :return: return a list of:

             * missing words
             * json schema describing a json-ld for the given word
    """
    missing_words = []
    schema = dict()
    data = get_graph_item(schemaorg_data, word)
    if data is None:
        return [], None
    if ("@type" in data) and (data["@type"] == "rdfs:Class"):
        # found json object description
        schema["definitions"] = dict()
        schema["definitions"][word] = dict()
        schema["definitions"][word]["type"] = "object"
        if "rdfs:comment" in data:
            schema["definitions"][word]["description"] = data["rdfs:comment"]
        schema["definitions"][word]["required"] = ["@context"]
        schema["definitions"][word]["properties"] = dict()
        properties = schema["definitions"][word]["properties"]
        properties["@context"] = create_context_schema(word)
        if "rdfs:subClassOf" in data:
            subClassOf = []
            if isinstance(data["rdfs:subClassOf"], dict):
                if data["rdfs:subClassOf"]["@id"].startswith('schema:'):
                    subClassOf.append(data["rdfs:subClassOf"]["@id"])
            elif isinstance(data["rdfs:subClassOf"], list):
                for sco in data["rdfs:subClassOf"]:
                    if sco["@id"].startswith('schema:'):
                        subClassOf.append(sco["@id"])
            else:
                raise NotImplementedError(
                    'data type of "rdfs:subClassOf" not handled')
            if len(subClassOf) > 0:
                schema["definitions"][word]["allOf"] = list()
                schema["definitions"][word]["allOf"].append(properties)
                properties = schema["definitions"][word]["allOf"][0]
                for sco in subClassOf:
                    new_word = sco.split('schema:')[1]
                    schema["definitions"][word]["allOf"].append(
                        {"$ref": "#/definitions/" + new_word})
                    missing_words.append(new_word)
                del schema["definitions"][word]["properties"]
        # add other properties to: properties
        add_properties_to_object(
            schemaorg_data, word, properties, missing_words)
        # items with: "schema:domainIncludes": {"@id": "schema:Person"}
        # example: "@id": "schema:additionalName",
        schema["required"] = ["@context"]
        schema["properties"] = dict()
        schema["properties"]["@context"] = create_context_schema(word)
    return missing_words, schema


def json_schema_from_schema_org(schemaorg_data, vocabulary, draft='draft-04'):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-19

    This function generates a json schema from https://schema.org , which
    desribes the vocabulary.

    :param schemaorg_data: json-ld data from https://schema.org as returned
                           from :func:`get_schema_org_data`.
    :param vocabulary: list of words, which are a 
                       Schema.org Type (Schema.org vocabulary)
    :param draft: the used json schema, could be:

                  * 'draft-04'
                  * 'draft-06'
                  * 'draft-07'
                  * '2019-09'
    :return: json schema describing a json-ld for the given vocabulary
    """
    missing_words = set()
    for word in vocabulary:
        missing_words.add(word)
    schema = dict()
    schema_declaration = {
        'draft-04': "http://json-schema.org/draft-04/schema#",
        'draft-06': "http://json-schema.org/draft-06/schema#",
        'draft-07': "http://json-schema.org/draft-07/schema#",
        '2019-09': "http://json-schema.org/draft/2019-09/schema#"}
    if draft in schema_declaration:
        schema["$schema"] = schema_declaration[draft]
    else:
        raise NotImplementedError('do not understand json draft version')
    add_property(schema,
                 "title",
                 "json schema to define json-ld based on schema.org")
    add_property(schema,
                 "description",
                 "The vocabulary %s " % ', '.join(vocabulary) +
                 "from schema.org is defined as a json schema. "
                 "It should be a valid json-ld file. "
                 "All necessary words should be defined.")
    update_description = False
    found_vocabulary = []
    while len(missing_words) > 0:
        word = missing_words.pop()
        sys.stderr.write(f'searching: {word}\n')
        new_missing_words, word_schema = add_word(
            schemaorg_data, word, draft=draft)
        if word_schema is None:
            del vocabulary[vocabulary.index(word)]
            update_description = True
        else:
            found_vocabulary.append(word)
            combine(schema, word_schema)
            if len(new_missing_words) > 0:
                for t in new_missing_words:
                    if t not in schema["definitions"]:
                        missing_words.add(t)
        sys.stderr.write(f'finished: {word}\n')
        # return schema  # workaround for debugging
    if update_description:
        set_property(schema,
                     "description",
                     "The vocabulary %s " % ', '.join(vocabulary) +
                     "from schema.org is defined as a json schema. "
                     "It should be a valid json-ld file. "
                     "All necessary words should be defined.")
    if len(found_vocabulary) == 0:
        sys.stderr.write('nothing found\n')
        schema = dict()
    return schema
