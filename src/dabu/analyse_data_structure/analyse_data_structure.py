"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-03 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os
import re


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
            break
    return res

def add_append_integrate_data(store, key, data):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-04 (last change).
    """
    if ((key in store) and
        store[key] != data):
        if type(store[key]) in (list, tuple):
            if data not in store[key]:
                store[key].append(data)
        else:
            store[key] = [
                store[key],
                data]
    else:
        store[key] = data

def analyse_data_structure(path, result=dict()):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-03 (last change).

    Analyse the data structure of the given path.

    :param path: directory path to analyse
    :param result: you can give a dict, where the results are appended
                   or overridden
    """
    files = os.listdir(path)
    analysed_files = []
    # find README, LICENSE, MANIFEST
    for key in ['readme', 'license', 'manifest']:
        res = check_file_available(files, key)
        if res is not None:
            result[key] = res
            analysed_files.append(res)
    # analyse if directory is a repository
    #result['repository'] = None
    for f in files:
        if (f in ['.git', '.bzr']) and os.path.isdir(f):
            # assume repository
            result['repository'] = f
            analysed_files.append(f)
            add_append_integrate_data(
                result, 'data integrity control', 'repository')
            break
    # analyse if checksums are available (look for checksums)
    #result['checksums'] = None
    regexp = re.compile(
        '.*checksum.*|.*\.md5|.*\.sha256|.*\.sha512|.*\.sha1',
        flags=re.IGNORECASE)
    for f in files:
        if regexp.findall(f):
            result['checksums'] = f
            analysed_files.append(f)
            add_append_integrate_data(
                result, 'data integrity control', 'checksums')
            break
    result['data'] = list(set(files).difference(analysed_files))
    # result['author'] = [{'name': 'foo', 'email': 'bar'},
    #                    {'name': 'a', 'email': 'b'}]
    return result
