"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-19
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu.py listschemas
"""

import subprocess


class mixin_listschemas():
    """
    :Author: Daniel Mohr
    :Date: 2021-02-19
    """

    def test_listschemas(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-19

        This script tests the script 'pydabu.py listschemas'.
        """
        cp = subprocess.run(
            ['pydabu.py listschemas'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=self.subprocess_timeout,
            check=True)
        stdout_lines = cp.stdout.split()
        self.assertTrue(stdout_lines[0].endswith(
            b'analyse_data_structure_output.schema'))
        self.assertTrue(stdout_lines[1].endswith(b'dabu.schema'))
        self.assertTrue(stdout_lines[2].endswith(b'dabu_requires.schema'))
