"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-01-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os
import re

from .analyse_file_format import analyse_file_format


def analyse_file_format_dict(path, result):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-01-19 (last change).

    Analyse the file format of the files stored in result.

    :param path: directory path to analyse
    :param result: a dict; only the key 'data' will be read
    """
    files = result['data'].copy()
    result['data'] = []
    for f in files:
        result['data'].append({'name': f, 'format': analyse_file_format(f)})
    return result
