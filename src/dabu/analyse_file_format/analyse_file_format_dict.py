"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import sys

from dabu.check_nasa_ames_format import check_nasa_ames_format
from dabu.check_netcdf_file import check_netcdf_file

from .analyse_file_format import analyse_file_format
from .create_checksum import create_checksum
from .extract_hash_from_checksum_file import ExtractHashFromChecksumFile


def analyse_file_format_dict(
        result, output_format, store_checksums=True, checksum_file=None):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-17 (last change).

    Analyse the file format of the files stored in result.

    :param result: a dict; only the key 'data' will be adapted
    :param output_format: describes the output format in a list
    :param store_checksums: if True find/calculate checksums for each file
    :param checksum_file: the file to import the checksums from
    """
    if 'data' not in result:
        return result  # nothing to do, no data files available
    if checksum_file is not None:
        hash_from_checksum_file = ExtractHashFromChecksumFile(
            checksum_file)
    files = result['data'].copy()
    result['data'] = []
    for filename in files:
        file_extension = analyse_file_format(filename)
        resitem = {'name': filename, 'file_extension': file_extension}
        if store_checksums:
            checksum = None
            if checksum_file is not None:
                hash_info = hash_from_checksum_file(
                    filename, encoding='base64')
                if hash_info is not None:
                    checksum = {'hash': hash_info[0],
                                'algorithm': hash_info[1][0],
                                'encoding': hash_info[1][1]}
            if checksum is None:
                hash_byte_array = create_checksum(filename,
                                                  algorithm='sha512',
                                                  encoding='base64')
                checksum = {'hash': hash_byte_array.decode(encoding='utf-8'),
                            'algorithm': 'sha512',
                            'encoding': 'base64'}
            if checksum is not None:
                resitem['checksum'] = checksum
        if file_extension.lower() == ".nc":  # NetCDF file
            try:
                resitem['netcdf check'] = check_netcdf_file(filename,
                                                            output_format)
            except Exception:
                sys.stderr.write('Could not check NetCDF file.\n')
                resitem['netcdf check'] = dict()
                resitem['netcdf check']['error'] = 1
                resitem['netcdf check']['log'] = \
                    ['Could not check NetCDF file.']
        if file_extension.lower() in ['.nas', '.na']:  # NASA Ames Format
            resitem['nasa ames format check'] = check_nasa_ames_format(
                filename, output_format)
        result['data'].append(resitem)
    return result
