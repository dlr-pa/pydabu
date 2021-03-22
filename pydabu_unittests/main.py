"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-19
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

aggregation of tests
"""


import unittest


class test_module_import(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-04
    """

    def test_module_import(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-04
        """
        import dabu
        import dabu.analyse_data_structure
        import dabu.check_nasa_ames_format
        import dabu.check_netcdf_file
        import dabu.analyse_file_format
        import dabu.schema_org_data
        import dabu.scripts
        import dabu.scripts.pydabu
        import dabu.scripts.json_schema_from_schema_org


class test_scripts_executable(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-04
    """

    def test_script_pydabu_executable(self):
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

    def test_script_json_schema_from_schema_org_executable(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-04
        """
        import subprocess
        # check error output
        cp = subprocess.run(
            ["json_schema_from_schema_org.py"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=False)
        with self.assertRaises(subprocess.CalledProcessError):
            # parameter is necessary
            cp.check_returncode()
        self.assertEqual(len(cp.stdout), 0)
        self.assertTrue(len(cp.stderr) >= 210)
        # check begin of error output
        self.assertTrue(
            cp.stderr.startswith(b'usage: json_schema_from_schema_org.py'))
        # check help output
        cp = subprocess.run(
            ["json_schema_from_schema_org.py -h"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        self.assertTrue(len(cp.stdout) >= 1019)
        # check begin of help output
        self.assertTrue(
            cp.stdout.startswith(b'usage: json_schema_from_schema_org.py'))
        # check end of help output
        self.assertTrue(cp.stdout.endswith(
            b'License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.\n'))


def module(suite):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-03-19
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    add tests for the module
    """
    print('add tests for the module')
    loader = unittest.defaultTestLoader
    suite.addTest(loader.loadTestsFromTestCase(test_module_import))
    # dabu.schemas
    suite.addTest(loader.loadTestsFromName('pydabu_unittests.package_data'))
    # dabu.scripts.pydabu.check_arg_file_not_exists.py
    suite.addTest(loader.loadTestsFromName(
        'pydabu_unittests.dabu_scripts_pydabu_check_arg_file_not_exists'))
    # dabu.compare_json_schemas
    suite.addTest(
        loader.loadTestsFromName('pydabu_unittests.compare_json_schemas'))
    # dabut.schema_org_data
    suite.addTest(
        loader.loadTestsFromName('pydabu_unittests.schema_org_data'))


def scripts(suite):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-03-04
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    add tests for the scripts
    """
    print('add tests for the scripts')
    loader = unittest.defaultTestLoader
    suite.addTest(loader.loadTestsFromTestCase(test_scripts_executable))
    # pydabu.py
    suite.addTest(loader.loadTestsFromName('pydabu_unittests.script_pydabu'))
    # json_schema_from_schema_org.py
    suite.addTest(
        loader.loadTestsFromName(
            'pydabu_unittests.script_json_schema_from_schema_org'))
