#!/usr/bin/python3
"""
Author: Daniel Mohr.
Date: 2021-03-02 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

./json_schema_from_schema_org.py Thing
./json_schema_from_schema_org.py Person
./json_schema_from_schema_org.py email

./json_schema_from_schema_org.py Thing > t.json
jsonschema t.json

./json_schema_from_schema_org.py Thing | tee t.json ; jsonschema t.json
"""

import argparse
import bz2
import gzip
import json
import lzma
import os.path
import ssl
import sys
import tempfile
import urllib.request


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
    if draft in ['draft-07', '2019-09']:
        for key in schema2json7:
            schema2json[key] = schema2json7[key]
    else:
        for key in schema2json7:
            schema2json[key] = "string"
    if data in schema2json:
        newdata["@id"] = "https://schema.org/" + data[7:]
        if isinstance(schema2json[data], str):
            newdata["type"] = schema2json[data]
        else:  # dict
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
    """
    :Author: Daniel Mohr
    :Date: 2021-03-01
    """
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
        if not word.startswith('schema:'):
            word = 'schema:' + word
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
    while len(missing_words) > 0:
        item = missing_words.pop(0)
        sys.stderr.write(f'extracting: {item}\n')
        #item = "schema:" + item
        new_schema[item] = dict()
        new_schema[item]["type"] = "object"
        new_schema[item]["properties"] = dict()
        new_missing_words = []
        for i in schemaorg_data['@graph']:
            if ("@id" in i) and (i["@id"] == item):
                if ("@type" in i) and (i["@type"] == "rdfs:Class"):
                    new_missing_words = schema_org_rdfs_class(
                        item, new_schema, schemaorg_data['@graph'])
                    if (("rdfs:subClassOf" in i) and
                            ("@id" in i["rdfs:subClassOf"])):
                        if isinstance(i["rdfs:subClassOf"]["@id"], str):
                            new_schema[item]["allOf"] = combine_properties(
                                new_schema[item]["properties"],
                                i["rdfs:subClassOf"]["@id"])
                            del new_schema[item]["properties"]
                            new_missing_words.append(
                                i["rdfs:subClassOf"]["@id"])
                        else:
                            raise NotImplementedError(
                                'type of "rdfs:subClassOf" not str')
                    break
                elif ("@type" in i) and ("schema:DataType" in i["@type"]):
                    raise NotImplementedError('Your word is a data type.')
                else:
                    raise NotImplementedError(json.dumps(i))
        if len(new_missing_words) > 0:
            for t in new_missing_words:
                if ((t not in missing_words) and
                        (t not in new_schema)):
                    missing_words.append(t)
    return final_new_schema


def get_schemaorg_data(cachefilename):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-02
    """
    schema_org_data = None
    opencmds = {'default': open,
                '.jsonld': open,
                '.gz': gzip.open,
                '.lzma': lzma.open,
                '.xz': lzma.open,
                '.bz2': bz2.open}
    if len(cachefilename) > 0:
        _, ext = os.path.splitext(cachefilename)
        ext = ext.lower()
        if ext in opencmds:
            open_cmd = opencmds[ext]
        else:
            open_cmd = opencmds['default']
    if (len(cachefilename) > 0) and os.path.isfile(cachefilename):
        with open_cmd(cachefilename, 'rb') as fd:
            schema_org_data = json.load(fd)
    else:
        url = 'https://schema.org/version/latest/schemaorg-current-https.jsonld'
        context = ssl.create_default_context()
        with urllib.request.urlopen(url, context=context) as fd:
            schema_org_data = json.load(fd)
        if (schema_org_data is not None) and (len(cachefilename) > 0):
            with open_cmd(cachefilename, 'wb') as fd:
                fd.write(json.dumps(schema_org_data,).encode())
    return schema_org_data


def my_argument_parser():
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-03-02 (last change).
    """
    epilog = ""
    description = 'json_schema_from_schema_org.py is a script ' \
        'to define json-ld based on schema.org as a json schema.'
    parser = argparse.ArgumentParser(
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'vocabulary',
        nargs='+',
        type=str,
        help='For these words from schema.org the output is generated.',
        metavar='word')
    parser.add_argument(
        '-indent',
        nargs=1,
        type=int,
        required=False,
        default=[4],
        dest='indent',
        help='In the output the elements will be indented ' +
        'by this number of spaces.',
        metavar='i')
    cachefilename = os.path.join(
        tempfile.gettempdir(),
        'json_schema_from_schema_org_schemaorg-current-https.jsonld.lzma')
    parser.add_argument(
        '-cachefilename',
        nargs=1,
        type=str,
        required=False,
        default=[cachefilename],
        dest='cachefilename',
        help='We need data from schema.org. '
        'If you set cachefilename to an empty string, nothing is cached. '
        'If the file ends with common extension for compression, '
        'this comperession is used (e. g.: .gz, .lzma, .xz, .bz2).'
        'default: "%s"' % cachefilename,
        metavar='f')
    return parser


def main():
    """
    :Author: Daniel Mohr
    :Date: 2021-03-02
    """
    # command line arguments:
    parser = my_argument_parser()
    # parse arguments
    args = parser.parse_args()
    schema_org_data = get_schemaorg_data(args.cachefilename[0])
    new_schema = json_schema_from_schema_org(
        schema_org_data, args.vocabulary, draft='draft-04')
    print(json.dumps(new_schema, indent=args.indent[0]))


if __name__ == "__main__":
    main()
