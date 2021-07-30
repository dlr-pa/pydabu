"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-05
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu listschemas
"""

import subprocess

try:
    from .data_path_class import DataPathClass
except (ModuleNotFoundError, ImportError):
    from data_path_class import DataPathClass


# pylint: disable=too-few-public-methods
class MixinListschemas(DataPathClass):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-05
    """

    def test_listschemas(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05

        This script tests the script 'pydabu listschemas'.
        """
        cpi = subprocess.run(
            'pydabu listschemas',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=self.subprocess_timeout,
            check=True)
        stdout_lines = cpi.stdout.split()
        self.assertTrue(stdout_lines[0].endswith(
            b'analyse_data_structure_output.schema'))
        self.assertTrue(stdout_lines[1].endswith(b'dabu.schema'))
        self.assertTrue(stdout_lines[2].endswith(b'dabu_requires.schema'))
        subprocess.run(
            'pydabu listschemas -o json',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=self.subprocess_timeout,
            check=True)
