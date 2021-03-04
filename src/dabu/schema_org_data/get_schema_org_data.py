"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-04 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import bz2
import gzip
import json
import lzma
import os.path
import ssl
import urllib.request


def get_schema_org_data(cachefilename=''):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-04

    This function returns the data from
    https://schema.org/version/latest/schemaorg-current-https.jsonld
    as a json-ld structure (parsed by the python module json).

    :param cachefilename: If not set to an empty string, the data is read
                          from this file. If this file does not exists,
                          the data is loadd from the website and stored
                          in this file.

    :return: json-ld structure (parsed by the python module json) as 
             dicts and lists
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
