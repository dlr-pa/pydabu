"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-19
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu check_netcdf_file
"""

import subprocess

try:
    from .data_path_class import DataPathClass
except (ModuleNotFoundError, ImportError):
    from data_path_class import DataPathClass


# pylint: disable=too-few-public-methods
class MixinCheckNetcdfFile(DataPathClass):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-19
    """

    def test_check_netcdf_file(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu check_netcdf_file'.
        """
        # data bubble 01
        test_dir_path = self.test_dir_path[1]
        cpi = subprocess.run(
            'pydabu check_netcdf_file -f README.md',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=False)
        self.assertEqual(cpi.returncode, 1)  # check for error
        cpi = subprocess.run(
            'pydabu check_netcdf_file -f foo',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=False)
        self.assertEqual(cpi.returncode, 2)  # check for error
