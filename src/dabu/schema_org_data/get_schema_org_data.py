"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-09 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import bz2
import gzip
import json
import lzma
import os
import os.path
import ssl
import urllib.request


def lzma_open(filename, mode, format=lzma.FORMAT_ALONE, *params):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09
    """
    return lzma.open(filename, mode, format=format, *params)


def get_schema_org_data(cachefilepath='', cachefilename=''):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09

    This function returns the data from
    https://schema.org/version/latest/schemaorg-current-https.jsonld
    as a json-ld structure (parsed by the python module json).

    :param cachefilepath: This path is used as the path for the cachefilename.
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
                '.lzma': lzma_open,
                '.xz': lzma.open,
                '.bz2': bz2.open}
    cachefilenamepath = os.path.join(cachefilepath, cachefilename)
    if len(cachefilename) > 0:
        _, ext = os.path.splitext(cachefilenamepath)
        ext = ext.lower()
        if ext in opencmds:
            open_cmd = opencmds[ext]
        else:
            open_cmd = opencmds['default']
    if (len(cachefilename) > 0) and os.path.isfile(cachefilenamepath):
        with open_cmd(cachefilenamepath, 'rb') as fd:
            schema_org_data = json.load(fd)
    else:
        url = \
          'https://schema.org/version/latest/schemaorg-current-https.jsonld'
        context = ssl.create_default_context()
        with urllib.request.urlopen(url, context=context) as fd:
            schema_org_data = json.load(fd)
        if (schema_org_data is not None) and (len(cachefilename) > 0):
            if (len(cachefilepath) > 0) and (not os.path.isdir(cachefilepath)):
                os.mkdir(cachefilepath)
            with open_cmd(cachefilenamepath, 'wb') as fd:
                fd.write(json.dumps(schema_org_data,).encode())
    return schema_org_data
