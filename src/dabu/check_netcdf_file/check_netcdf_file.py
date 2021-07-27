"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-15 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import tempfile
import time


def check_netcdf_file(file, output_format='human_readable'):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-15 (last change).

    Checks the give file for the format netCDF.
    It uses the CF Checker: https://github.com/cedadev/cf-checker

    :param file: file to analyse
    """
    import cfchecker.cfchecks
    import netCDF4
    result = dict()
    result['error'] = 0
    result['log'] = []
    checker_name = 'pydabu (netcdf check)'
    result[checker_name] = dict()
    rootgrp = netCDF4.Dataset(file, "r")
    convention = None
    if hasattr(rootgrp, 'Conventions'):
        # Climate and Forecasts (CF) Metadata Convention is used
        convention = rootgrp.Conventions
    if hasattr(rootgrp, 'file_format'):
        # should be the same as data_model
        result[checker_name]['file_format'] = rootgrp.file_format
    if hasattr(rootgrp, 'data_model'):
        # data_model describes the netCDF data model version:
        #   NETCDF3_CLASSIC, NETCDF4, NETCDF4_CLASSIC, NETCDF3_64BIT_OFFSET or
        #   NETCDF3_64BIT_DATA
        result[checker_name]['data_model'] = rootgrp.data_model
    if hasattr(rootgrp, 'disk_format'):
        result[checker_name]['disk_format'] = rootgrp.disk_format
    rootgrp.close()
    result[checker_name]['created'] = time.time()
    if convention is not None:
        # check for Climate and Forecasts (CF) Metadata Convention
        inst = cfchecker.cfchecks.CFChecker(
            uploader=None,
            useFileName='yes',
            badc=None,
            coards=None,
            cfRegionNamesXML=cfchecker.cfchecks.REGIONNAMES,
            cfStandardNamesXML=cfchecker.cfchecks.STANDARDNAME,
            cfAreaTypesXML=cfchecker.cfchecks.AREATYPES,
            cacheDir=tempfile.gettempdir(),
            cacheTables=False,  # True for many files
            cacheTime=24*3600,  # 1 day as hard coded in cfchecker.cfchecks
            version=convention,
            debug=False,
            silent=True)
        inst.checker(file)
        totals = inst.get_total_counts()
        checker_name = 'CF Checker Version ' + cfchecker.cfchecks.__version__
        result[checker_name] = dict()
        result[checker_name]['created'] = time.time()
        result[checker_name]['error'] = totals["FATAL"] + totals["ERROR"]
        result[checker_name]['warning'] = totals["WARN"]
        if output_format != 'human_readable':
            result[checker_name]['result'] = inst.all_results
    return result
