"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""


def get_graph_item(schemaorg_data, word):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-16
    """
    for item in schemaorg_data['@graph']:
        if ("@id" in item) and (item["@id"] == "schema:" + word):
            return item
    return None
