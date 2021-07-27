"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json

from .ispending import ispending
from .get_property import get_property


def add_property_to_object(
        schemaorg_data, item, domainIncludes, word, properties, missing_words):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16
    """
    if "@id" not in domainIncludes:
        raise NotImplementedError(json.dumps(item, indent=2))
    elif domainIncludes["@id"] == "schema:" + word:
        if "@id" not in item:
            raise NotImplementedError(json.dumps(item, indent=2))
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
      "rdfs:comment": "An additional name for a Person,
                       can be used for a middle name.",
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
