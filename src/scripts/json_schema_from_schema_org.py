#!/usr/bin/python3
"""
Author: Daniel Mohr.
Date: 2021-03-01 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

./b.py Thing

./b.py Thing > t.json
jsonschema t.json

./b.py Thing | tee t.json ; jsonschema t.json
"""

import json
import sys


def _Includes_dict(object, content):
    if ("@id" in object) and (object["@id"] == content):
        return True
    else:
        return False


def _Includes_list(object, content):
    ret = False
    for element in object:
        ret = _Includes_dict(element, content)
        if ret:
            break
    return ret


def _Includes(object, content):
    if isinstance(object, dict):
        return _Includes_dict(object, content)
    elif isinstance(object, list):
        return _Includes_list(object, content)
    else:
        return False


def domainIncludes(object, content):
    if ("schema:domainIncludes" in object):
        return _Includes(object["schema:domainIncludes"], content)
    else:
        return False


def type_from_schema_id(data, newdata, i, draft=4):
    skip = ["schema:Action", "schema:CreativeWork", "schema:MediaObject",
            "schema:PropertyValue", "schema:Event", "schema:NewsArticle",
            "schema:Distance", "schema:QuantitativeValue",
            "schema:MediaSubscription",
            "schema:Organization", "schema:Duration",
            "schema:AggregateRating", "schema:Product",
            "schema:DefinedTerm", "schema:InteractionCounter",
            "schema:Demand", "schema:Offer", "schema:Rating",
            "schema:ContactPoint", "schema:OfferCatalog",
            "schema:EducationalOrganization", "schema:GenderType",
            "schema:PostalAddress", "schema:EducationalOccupationalCredential",
            "schema:Occupation", "schema:ProgramMembership",
            "schema:MonetaryAmount", "schema:PriceSpecification",
            "schema:Brand", "schema:Country", "schema:Language",
            "schema:OwnershipInfo", "schema:OpeningHoursSpecification",
            "schema:GeoCoordinates", "schema:GeoShape",
            "schema:GeospatialGeometry", "schema:Map", "schema:Review",
            "schema:Photograph", "schema:LocationFeatureSpecification",
            "schema:CorrectionComment",
            "schema:AudioObject", "schema:MusicRecording", "schema:Clip",
            "schema:VideoObject", "schema:Audience", "schema:AlignmentObject",
            "schema:PublicationEvent", "schema:ItemList"]
    handle = ["schema:ImageObject", "schema:Thing", "schema:Person",
              "schema:Place", "schema:Comment"]
    schema2json = {"schema:Text": "string",
                   "schema:Boolean": "boolean",
                   "schema:Integer": "integer",
                   "schema:Number": "number",
                   "schema:Float": "number",
                   "schema:URL": {"type": "string", "format": "uri"},
                   "schema:DateTime": {"type": "string", "format": "date-time"}}
    schema2json7 = {"schema:Date": {"type": "string", "format": "date"},
                    "schema:Time": {"type": "string", "format": "datetime"}}
    if draft == 7: # or newer
        for key in schema2json7:
            schema2json[key] = schema2json7[key]
    else:
        for key in schema2json7:
            schema2json[key] = "string"
    if data in schema2json:
        newdata["@id"] = "https://schema.org/" + data[7:]
        if isinstance(schema2json[data], str):
            newdata["type"] = schema2json[data]
        else: # dict
            for key in schema2json[data]:
                newdata[key] = schema2json[data][key]
    elif data in handle:
        newdata["$ref"] = "#/definitions/" + data
        return data
    elif data in skip:
        pass
    else:
        raise NotImplementedError(
            f'do not understand "@id" in:\n\n{data}\n\n{i}')
    return None


def schema_org_rdfs_class(item, new_schema, data):
    missing_types = []
    subclasses = []
    for i in data:
        if domainIncludes(i, item):
            # found property
            new_schema[item]["properties"][i["@id"]] = dict()
            if ("schema:rangeIncludes" in i):
                missing_type = None
                if isinstance(i["schema:rangeIncludes"], dict):
                    missing_type = type_from_schema_id(
                        i["schema:rangeIncludes"]["@id"],
                        new_schema[item]["properties"][i["@id"]],
                        i)
                elif isinstance(i["schema:rangeIncludes"], list):
                    new_schema[item]["properties"][i["@id"]]["oneOf"] = list()
                    for element in i["schema:rangeIncludes"]:
                        new_schema[item]["properties"][i["@id"]]["oneOf"].append(
                            dict())
                        missing_type = type_from_schema_id(
                            element["@id"],
                            new_schema[item]["properties"][i["@id"]
                                                           ]["oneOf"][-1],
                            i)
                else:
                    raise NotImplementedError(
                        f'do not understand "schema:rangeIncludes" in:\n{i}')
                if missing_type is not None:
                    missing_types.append(missing_type)
            else:
                raise NotImplementedError(
                    f'no "schema:rangeIncludes" in:\n\n{i}')
        # if (("rdfs:subClassOf" in i) and ("@id" in i["rdfs:subClassOf"])):
        #    if isinstance(i["rdfs:subClassOf"]["@id"], str):
        #        subclasses.append(i["rdfs:subClassOf"]["@id"])
        #    else:
        #        raise NotImplementedError('type of "rdfs:subClassOf" not str')
    # if len(subclasses) > 0:
    #    new_schema[item]["properties"] = {"allOf": [{"properties": new_schema[item]["properties"]}]}
    #    for sc in subclasses:
    #        new_schema[item]["properties"]["allOf"].append(sc)
    return missing_types


def combine_properties(properties, subclass):
    return [
        {"properties":
         properties},
        {"$ref":
         "#/definitions/" + subclass}]


def json_schema_from_schema_org(schemaorg_data, item, draft=4):
    missing_types = [item]
    final_new_schema = dict()
    if draft == 4:
        final_new_schema["$schema"] = "http://json-schema.org/draft-04/schema#"
    elif draft == 6:
        final_new_schema["$schema"] = "http://json-schema.org/draft-06/schema#"
    elif draft == 7:
        final_new_schema["$schema"] = "http://json-schema.org/draft-07/schema#"
    else:
        raise NotImplementedError('do not understand json draft version')
    final_new_schema["definitions"] = dict()
    new_schema = final_new_schema["definitions"]
    while len(missing_types) > 0:
        item = missing_types.pop(0)
        sys.stderr.write(f'extracting: {item}\n')
        #item = "schema:" + item
        new_schema[item] = dict()
        new_schema[item]["type"] = "object"
        new_schema[item]["properties"] = dict()
        new_missing_types = []
        for i in schemaorg_data['@graph']:
            if ("@id" in i) and (i["@id"] == item):
                if ("@type" in i) and (i["@type"] == "rdfs:Class"):
                    new_missing_types = schema_org_rdfs_class(
                        item, new_schema, schemaorg_data['@graph'])
                    if (("rdfs:subClassOf" in i) and
                            ("@id" in i["rdfs:subClassOf"])):
                        if isinstance(i["rdfs:subClassOf"]["@id"], str):
                            new_schema[item]["allOf"] = combine_properties(
                                new_schema[item]["properties"],
                                i["rdfs:subClassOf"]["@id"])
                            del new_schema[item]["properties"]
                            new_missing_types.append(
                                i["rdfs:subClassOf"]["@id"])
                        else:
                            raise NotImplementedError(
                                'type of "rdfs:subClassOf" not str')
                    break
                else:
                    raise NotImplementedError(json.dumps(i))
        if len(new_missing_types) > 0:
            for t in new_missing_types:
                if ((t not in missing_types) and
                        (t not in new_schema)):
                    missing_types.append(t)
    return final_new_schema


def main():
    if len(sys.argv) != 2:
        print('need exactly one parameter')
        exit()
    item = sys.argv[1]
    fd = open('schemaorg-current-http.jsonld')
    schemaorg_data = json.load(fd)
    fd.close()
    if not item.startswith('schema:'):
        item = 'schema:' + item
    new_schema = json_schema_from_schema_org(schemaorg_data, item, draft=4)
    print(json.dumps(new_schema, indent=1))


if __name__ == "__main__":
    main()
