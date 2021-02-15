"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-15 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os
import re
import sys

from .analyse_file_format import analyse_file_format
from dabu.check_netcdf_file import check_netcdf_file
from dabu.check_nasa_ames_format import check_nasa_ames_format

def analyse_file_format_dict(
        result, output_format, store_checksums=True, checksum_file=None):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-15 (last change).

    Analyse the file format of the files stored in result.

    :param result: a dict; only the key 'data' will be adapted
    :param output_format: describes the output format in a list
    :param store_checksums: if True find/calculate checksums for each file
    :param checksum_file: the file to import the checksums from
    """
    if not 'data' in result:
        return result  # nothing to do, no data files available
    files = result['data'].copy()
    result['data'] = []
    for f in files:
        file_extension = analyse_file_format(f)
        resitem = {'name': f, 'file_extension': file_extension}
        if store_checksums:
            checksum = None
            if checksum_file is not None:
                raise NotImplementedError
                # adapt pfu_module.check_checksum.CheckChecksumsClass
            if checksum is None:
                raise NotImplementedError
                # adapt pfu_module.create_checksum.CreateChecksumsClass
        if file_extension.lower() == ".nc":  # NetCDF file
            try:
                resitem['netcdf check'] = check_netcdf_file(f, output_format)
            except:
                sys.stderr.write('Could not check NetCDF file.\n')
                resitem['netcdf check'] = dict()
                resitem['netcdf check']['error'] = 1
                resitem['netcdf check']['log'] = \
                  ['Could not check NetCDF file.']
        if file_extension.lower() in ['.nas', '.na']:  # NASA Ames Format
            resitem['nasa ames format check'] = check_nasa_ames_format(
                f, output_format)
        result['data'].append(resitem)
    return result
