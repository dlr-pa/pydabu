"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-19
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu check_nasa_ames_format
"""

import subprocess

try:
    from .data_path_class import DataPathClass
except (ModuleNotFoundError, ImportError):
    from data_path_class import DataPathClass


# pylint: disable=too-few-public-methods
class MixinCheckNasaAmesFormat(DataPathClass):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-19
    """

    def test_check_nasa_ames_format(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-08

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu check_nasa_ames_format'.
        """
        # data bubble 03
        test_dir_path = self.test_dir_path[3]
        cpi = subprocess.run(
            'pydabu check_nasa_ames_format -f foo',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=False)
        self.assertEqual(cpi.returncode, 2)  # check for error
        subprocess.run(
            'pydabu check_nasa_ames_format -f a.na',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=True)
