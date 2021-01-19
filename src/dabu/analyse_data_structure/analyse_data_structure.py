"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-01-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os


def check_file_available(files, key):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-01-19 (last change).
    """
    res = None
    key = key.lower()
    for f in files:
        if f.lower().startswith(key):
            res = f
    return res


def analyse_data_structure(path):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-01-19 (last change).

    Analyse the data structure of the given path.

    :param path: directory path to analyse
    """
    result = dict()
    files = os.listdir(path)
    # find README, LICENSE, MANIFEST
    for key in ['README', 'LICENSE', 'MANIFEST']:
        result[key] = check_file_available(files, key)
    result['author'] = [{'name': 'foo', 'email': 'bar'},
                        {'name': 'a', 'email': 'b'}]
    return result
