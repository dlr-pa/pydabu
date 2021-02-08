"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-08 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os
import re
import sys

from .analyse_file_format import analyse_file_format
from dabu.check_netcdf_file import check_netcdf_file


def analyse_file_format_dict(path, result, output_format):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-08 (last change).

    Analyse the file format of the files stored in result.

    :param path: directory path to analyse
    :param result: a dict; only the key 'data' will be read
    """
    files = result['data'].copy()
    result['data'] = []
    for f in files:
        file_extension = analyse_file_format(f)
        resitem = {'name': f, 'file_extension': file_extension}
        if file_extension.lower() == ".nc":  # NetCDF file
            try:
                res = check_netcdf_file(f)
                if 'human_readable' in output_format:
                    del res[checker_name]['result']
                resitem['netcdf check'] = res
            except:
                sys.stderr.write('Could not check NetCDF file.\n')
                resitem['netcdf check'] = dict()
        result['data'].append(resitem)
    return result
