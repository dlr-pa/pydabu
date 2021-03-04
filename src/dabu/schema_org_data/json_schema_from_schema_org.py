"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-04 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json
import sys


def _Includes_dict(object, content):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-26
    """
    if ("@id" in object) and (object["@id"] == content):
        return True
    else:
        return False


def _Includes_list(object, content):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-26
    """
    ret = False
    for element in object:
        ret = _Includes_dict(element, content)
        if ret:
            break
    return ret


def _Includes(object, content):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-26
    """
    if isinstance(object, dict):
        return _Includes_dict(object, content)
    elif isinstance(object, list):
        return _Includes_list(object, content)
    else:
        return False


def domainIncludes(object, content):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-26
    """
    if ("schema:domainIncludes" in object):
        return _Includes(object["schema:domainIncludes"], content)
    else:
        return False


def type_from_schema_id(data, newdata, i, draft='draft-04'):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-02
    """
    skip = ["Action", "CreativeWork", "MediaObject",
            "PropertyValue", "Event", "NewsArticle",
            "Distance", "QuantitativeValue",
            "MediaSubscription",
            "Organization", "Duration",
            "AggregateRating", "Product",
            "DefinedTerm", "InteractionCounter",
            "Demand", "Offer", "Rating",
            "ContactPoint", "OfferCatalog",
            "EducationalOrganization", "GenderType",
            "PostalAddress", "EducationalOccupationalCredential",
            "Occupation", "ProgramMembership",
            "MonetaryAmount", "PriceSpecification",
            "Brand", "Country", "Language",
            "OwnershipInfo", "OpeningHoursSpecification",
            "GeoCoordinates", "GeoShape",
            "GeospatialGeometry", "Map", "Review",
            "Photograph", "LocationFeatureSpecification",
            "CorrectionComment",
            "AudioObject", "MusicRecording", "Clip",
            "VideoObject", "Audience", "AlignmentObject",
            "PublicationEvent", "ItemList"]
    handle = ["ImageObject", "Thing", "Person",
              "Place", "Comment"]
    schema2json = {"Text": "string",
                   "Boolean": "boolean",
                   "Integer": "integer",
                   "Number": "number",
                   "Float": "number",
                   "URL": {"type": "string", "format": "uri"},
                   "DateTime": {"type": "string", "format": "date-time"}}
    schema2json7 = {"Date": {"type": "string", "format": "date"},
                    "Time": {"type": "string", "format": "datetime"}}
    if draft in ['draft-07', '2019-09']:
        for key in schema2json7:
            schema2json[key] = schema2json7[key]
    else:
        for key in schema2json7:
            schema2json[key] = "string"
    word = data.split(':')[1]
    if word in schema2json:
        newdata["@id"] = "https://schema.org/" + word
        if isinstance(schema2json[word], str):
            newdata["type"] = schema2json[word]
        else:  # dict
            for key in schema2json[word]:
                newdata[key] = schema2json[word][key]
    elif word in handle:
        newdata["$ref"] = "#/definitions/" + word
        return word
    elif word in skip:
        pass
    else:
        raise NotImplementedError(
            f'do not understand "@id" in:\n\n{data}\n\n{i}')
    return None


def schema_org_rdfs_class(item, new_schema, data):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-02
    """
    missing_types = []
    subclasses = []
    for i in data:
        if domainIncludes(i, "schema:" + item):
            # found property
            prop_name = i["@id"].split(':')[1]
            new_schema[item]["@context"][prop_name] = \
                "https://schema.org/" + prop_name
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
    :Date: 2021-03-02
    """
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
    final_new_schema["@context"] = dict()
    final_new_schema["definitions"] = dict()
    new_schema = final_new_schema["definitions"]
    while len(missing_words) > 0:
        item = missing_words.pop(0)
        sys.stderr.write(f'extracting: {item}\n')
        #item = "schema:" + item
        new_schema[item] = dict()
        new_schema[item]["type"] = "object"
        final_new_schema["@context"][item] = \
            "https://schema.org/" + item
        new_schema[item]["@context"] = dict()
        new_schema[item]["properties"] = dict()
        new_missing_words = []
        for i in schemaorg_data['@graph']:
            if ("@id" in i) and (i["@id"] == "schema:" + item):
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
                    raise NotImplementedError('Your word is a data type.')
                elif ("@type" in i) and ("rdf:Property" in i["@type"]):
                    raise NotImplementedError('Your word is a property.')
                else:
                    raise NotImplementedError(json.dumps(i))
        if len(new_missing_words) > 0:
            for t in new_missing_words:
                if ((t not in missing_words) and
                        (t not in new_schema)):
                    missing_words.append(t)
    return final_new_schema
