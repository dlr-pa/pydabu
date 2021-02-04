"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-04
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the package data of the module dabu
"""

import subprocess
import unittest


class scripty_pydabu(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-04
    """

    def test_basic_sub_commands(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        # check basic sub-commands
        cp = subprocess.run(
            ["pydabu.py check_data_structure"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        cp = subprocess.run(
            ["pydabu.py check_netcdf_file"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=False)
        with self.assertRaises(subprocess.CalledProcessError):
            # parameter is necessary
            cp.check_returncode()
        cp = subprocess.run(
            ["pydabu.py check_file_format"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
