"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-04 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""


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
