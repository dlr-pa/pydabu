"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-04
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

aggregation of tests
"""


import unittest


class test_module_import(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-04
    """

    def test_module_import(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        import dabu
        import dabu.analyse_data_structure
        import dabu.check_netcdf_file
        import dabu.analyse_file_format
        import dabu.scripts


class test_scripts_executable(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-04
    """

    def test_scripts_executable(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        import subprocess
        cp = subprocess.run(
            ["pydabu.py"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        # check at least minimal help output
        self.assertTrue(len(cp.stdout) >= 1111)
        # check begin of help output
        self.assertTrue(cp.stdout.startswith(b'usage: pydabu.py'))
        # check end of help output
        self.assertTrue(cp.stdout.endswith(
            b'License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.\n'))


def module(suite):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-04
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    add tests for the module
    """
    print('add tests for the module')
    loader = unittest.defaultTestLoader
    suite.addTest(loader.loadTestsFromTestCase(test_module_import))
    # dabu.schemas
    suite.addTest(loader.loadTestsFromName('pydabu_unittests.package_data'))


def scripts(suite):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-04
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    add tests for the scripts
    """
    print('add tests for the scripts')
    loader = unittest.defaultTestLoader
    suite.addTest(loader.loadTestsFromTestCase(test_scripts_executable))
    # pydabu.py
    suite.addTest(loader.loadTestsFromName('pydabu_unittests.script_pydabu'))
