"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-09 (last change).
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


def analyse_data_structure(path_name='.', result=dict()):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-09 (last change).

    Analyse the data structure of the given path.

    :param path_name: directory path to analyse
    :param result: you can give a dict, where the results are appended
                   or overridden
    """
    file_names = []  # only files in the actual directory
    all_file_names = []  # all other files in the directory tree
    for (dirpath, _, filenames) in os.walk(path_name):
        for file_name in filenames:
            if os.path.samefile(dirpath, '.'):
                file_names.append(file_name)
            else:
                all_file_names.append(os.path.join(dirpath, file_name))
    analysed_file_names = []
    # find README, LICENSE, MANIFEST
    for key in ['readme', 'license', 'manifest']:
        res = check_file_available(file_names, key)
        if res is not None:
            result[key] = res
            analysed_file_names.append(res)
    # analyse if directory is a repository
    for f in file_names:
        if (f in ['.git', '.bzr']) and os.path.isdir(f):
            # assume repository
            result['repository'] = f
            analysed_file_names.append(f)
            add_append_integrate_data(
                result, 'data integrity control', 'repository')
            break
    # analyse if checksums are available (look for checksums)
    regexp = re.compile(
        '.*checksum.*|.*\.md5|.*\.sha256|.*\.sha512|.*\.sha1',
        flags=re.IGNORECASE)
    for f in file_names:
        if regexp.findall(f):
            result['checksums'] = f
            analysed_file_names.append(f)
            add_append_integrate_data(
                result, 'data integrity control', 'checksums')
            break
    result['data'] = list(set(file_names).difference(analysed_file_names))
    result['data'] += all_file_names
    if len(result['data']) == 0:
        del result['data']
    # result['author'] = [{'name': 'foo', 'email': 'bar'},
    #                    {'name': 'a', 'email': 'b'}]
    return result
