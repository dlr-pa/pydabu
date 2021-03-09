"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-09 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json
import sys

from .add_context import add_context
from .schema_org_rdfs_class import schema_org_rdfs_class


def combine_properties(properties, subclass):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-01
    """
    return [
        {"properties":
         properties},
        {"$ref":
         "#/definitions/" + subclass}]


def json_schema_from_schema_org(schemaorg_data, vocabulary, draft='draft-04'):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09

    This function generates a json schema from https://schema.org , which
    desribes the vocabulary.

    :param schemaorg_data: json-ld data from https://schema.org as returned
                           from :func:`get_schema_org_data`.
    :param vocabulary: list of words, which are a 
                       Schema.org Type (Schema.org vocabulary )
    :param draft: the used json schema, could be:

                  * 'draft-04'
                  * 'draft-06'
                  * 'draft-07'
                  * '2019-09'
    :return: json schema describing a json-ld for the given vocabulary
    """
    # https://www.jsonschemavalidator.net/
    # https://json-ld.org/playground/
    missing_words = []
    for word in vocabulary:
        # if not word.startswith('schema:'):
        #    word = 'schema:' + word
        missing_words.append(word)
    final_new_schema = dict()
    schema_declaration = {
        'draft-04': "http://json-schema.org/draft-04/schema#",
        'draft-06': "http://json-schema.org/draft-06/schema#",
        'draft-07': "http://json-schema.org/draft-07/schema#",
        '2019-09': "http://json-schema.org/draft/2019-09/schema#"}
    if draft in schema_declaration:
        final_new_schema["$schema"] = schema_declaration[draft]
    else:
        raise NotImplementedError('do not understand json draft version')
    final_new_schema["title"] = \
        "json schema to define json-ld based on schema.org"
    final_new_schema["description"] = \
        "The vocabulary %s " % ', '.join(vocabulary) + \
        "from schema.org is defined as a json schema. " \
        "It should be a valid json-ld file. " \
        "All necessary words should be defined."
    final_new_schema["definitions"] = dict()
    new_schema = final_new_schema["definitions"]
    found_words = []
    while len(missing_words) > 0:
        item = missing_words.pop(0)
        sys.stderr.write(f'searching: {item}\n')
        #item = "schema:" + item
        new_schema[item] = dict()
        new_schema[item]["type"] = "object"
        add_context(final_new_schema, item, "https://schema.org/")
        #new_schema[item]["@context"] = dict()
        new_schema[item]["properties"] = dict()
        new_missing_words = []
        for i in schemaorg_data['@graph']:
            if ("@id" in i) and (i["@id"] == "schema:" + item):
                sys.stderr.write(f'extracting: {item}\n')
                found_words.append(item)
                if ("@type" in i) and (i["@type"] == "rdfs:Class"):
                    new_missing_words = schema_org_rdfs_class(
                        item, new_schema, schemaorg_data['@graph'])
                    if (("rdfs:subClassOf" in i) and
                            ("@id" in i["rdfs:subClassOf"])):
                        if isinstance(i["rdfs:subClassOf"]["@id"], str):
                            new_schema[item]["allOf"] = combine_properties(
                                new_schema[item]["properties"],
                                i["rdfs:subClassOf"]["@id"].split(':')[1])
                            del new_schema[item]["properties"]
                            new_missing_words.append(
                                i["rdfs:subClassOf"]["@id"].split(':')[1])
                        else:
                            raise NotImplementedError(
                                'type of "rdfs:subClassOf" not str')
                    break
                elif ("@type" in i) and ("schema:DataType" in i["@type"]):
                    raise NotImplementedError(
                        f'Your word "{item}" is a data type.')
                elif ("@type" in i) and ("rdf:Property" in i["@type"]):
                    raise NotImplementedError(
                        f'Your word "{item}" is a property.')
                else:
                    raise NotImplementedError(json.dumps(i))
        if len(new_missing_words) > 0:
            for t in new_missing_words:
                if ((t not in missing_words) and
                        (t not in new_schema)):
                    missing_words.append(t)
    if len(found_words) == 0:
        sys.stderr.write('nothing found\n')
        final_new_schema = dict()
        # print(found_words)
    sys.stderr.write('\n')
    return final_new_schema
