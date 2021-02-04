"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-04 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os
import tempfile
import time


def check_netcdf_file(file):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-04 (last change).

    Checks the give file for the format netCDF.
    It uses the CF Checker: https://github.com/cedadev/cf-checker

    :param file: file to analyse
    """
    import cfchecker.cfchecks
    from netCDF4 import Dataset
    rootgrp = Dataset(file, "r")
    version = rootgrp.Conventions
    rootgrp.close()
    result = dict()
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
        version=version,
        debug=False,
        silent=True)
    inst.checker(file)
    totals = inst.get_total_counts()
    checker_name = 'CF Checker Version ' + cfchecker.cfchecks.__version__
    result[checker_name] = dict()
    result[checker_name]['created'] = time.time()
    result[checker_name]['error'] = totals["FATAL"] + totals["ERROR"]
    result[checker_name]['warning'] = totals["WARN"]
    result[checker_name]['result'] = inst.all_results
    return result, checker_name
