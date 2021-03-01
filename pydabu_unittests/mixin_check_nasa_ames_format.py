"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-19
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu.py check_nasa_ames_format
"""

import subprocess


class mixin_check_nasa_ames_format():
    """
    :Author: Daniel Mohr
    :Date: 2021-02-19
    """

    def test_check_nasa_ames_format(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-08

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu.py check_nasa_ames_format'.
        """
        # data bubble 03
        test_dir_path = self.test_dir_path[3]
        cp = subprocess.run(
            ['pydabu.py check_nasa_ames_format -f foo'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=False)
        self.assertEqual(cp.returncode, 2)  # check for error
        cp = subprocess.run(
            ['pydabu.py check_nasa_ames_format -f a.na'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=True)