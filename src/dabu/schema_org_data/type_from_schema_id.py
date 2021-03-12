"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-12 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json


def get_type_element_from_schema_org_data(type_element, schemaorg_data_graph):
    for i in schemaorg_data_graph:
        if ("@id" in i) and (i["@id"] == type_element):
            return i
    return None


def type_from_schema_id(
        data, newdata, i, schemaorg_data_graph, draft='draft-04'):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-12
    """
    skip = ["Action",
            "PropertyValue", "Event", "NewsArticle",
            "QuantitativeValue",
            "MediaSubscription",
            "Duration",
            "AggregateRating", "Product",
            "DefinedTerm", "InteractionCounter",
            "Demand", "Offer", "Rating",
            "ContactPoint", "OfferCatalog",
            "GenderType",
            "PostalAddress", "EducationalOccupationalCredential",
            "Occupation", "ProgramMembership",
            "MonetaryAmount", "PriceSpecification",
            "Brand", "Country", "Language",
            "OwnershipInfo", "OpeningHoursSpecification",
            "GeoCoordinates", "GeoShape",
            "GeospatialGeometry", "Map", "Review",
            "LocationFeatureSpecification",
            "MusicRecording", "Clip",
            "VideoObject", "Audience", "AlignmentObject",
            "PublicationEvent", "ItemList", "valueReference",
            "MeasurementTypeEnumeration", "Enumeration"]
    #skip = []
    # schema.org types to handle ("rdfs:Class"):
    handle = ["ImageObject", "MediaObject",
              "Distance", "CreativeWork",
              "DefinedTerm",
              "Thing", "Person",
              "Place", "Comment",
              "DataCatalog", "Dataset", "DataDownload",
              "Organization", "AdministrativeArea", "VirtualLocation",
              "EducationalOrganization", "Photograph", "CorrectionComment",
              "AudioObject"]
    # schema.org datatypes to handle ("schema:DataType"):
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
        itext = json.dumps(i, indent=4)
        data_json = json.dumps(
            get_type_element_from_schema_org_data(data, schemaorg_data_graph),
            indent=4)
        raise NotImplementedError(
            f'do not understand "@id" = {data} in:\n\n{itext}\n\n'
            '{data} is:\n{data_json}')
    return None
