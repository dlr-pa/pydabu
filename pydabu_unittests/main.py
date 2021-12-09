"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-12-09
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

aggregation of tests

You can run this file directly::

  env python3 main.py
  pytest-3 main.py

Or you can run only one test, e. g.::

  env python3 main.py TestScriptsExecutable
  pytest-3 -k TestScriptsExecutable main.py
"""


import subprocess
import unittest

try:
    from .data_path_class import DataPathClass
except (ModuleNotFoundError, ImportError):
    from data_path_class import DataPathClass


class TestModuleImport(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-04
    """

    # pylint: disable=no-self-use
    def test_module_import(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-04
        """
        # pylint: disable=unused-variable,unused-import
        # pylint: disable=bad-option-value,import-outside-toplevel
        import dabu
        import dabu.analyse_data_structure
        import dabu.check_nasa_ames_format
        import dabu.check_netcdf_file
        import dabu.analyse_file_format
        import dabu.schema_org_data
        import dabu.scripts
        import dabu.scripts.pydabu
        import dabu.scripts.json_schema_from_schema_org


class TestScriptsExecutable(unittest.TestCase, DataPathClass):
    """
    :Author: Daniel Mohr
    :Date: 2021-12-09

    env python3 main.py TestScriptsExecutable
    """

    def test_script_pydabu_executable(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-07-13

        env python3 main.py TestScriptsExecutable.test_script_pydabu_executable
        """
        cpi = subprocess.run(
            "pydabu",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=self.subprocess_timeout, check=True)
        # check at least minimal help output
        self.assertTrue(len(cpi.stdout) >= 1111)
        # check begin of help output
        self.assertTrue(cpi.stdout.startswith(b'usage: pydabu'))
        # check end of help output
        self.assertTrue(cpi.stdout.strip().endswith(
            b'License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.'))

    # pylint: disable=invalid-name
    def test_script_json_schema_from_schema_org_executable(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-07-13
        """
        # check error output
        cpi = subprocess.run(
            "json_schema_from_schema_org",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=self.subprocess_timeout, check=False)
        with self.assertRaises(subprocess.CalledProcessError):
            # parameter is necessary
            cpi.check_returncode()
        self.assertEqual(len(cpi.stdout), 0)
        self.assertTrue(len(cpi.stderr) >= 210)
        # check begin of error output
        self.assertTrue(
            cpi.stderr.startswith(b'usage: json_schema_from_schema_org'))
        # check help output
        cpi = subprocess.run(
            "json_schema_from_schema_org -h",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=self.subprocess_timeout, check=False)
        self.assertTrue(len(cpi.stdout) >= 1019)
        # check begin of help output
        self.assertTrue(
            cpi.stdout.startswith(b'usage: json_schema_from_schema_org'))
        # check end of help output
        self.assertTrue(cpi.stdout.strip().endswith(
            b'License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.'))


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
    suite.addTest(loader.loadTestsFromTestCase(TestModuleImport))
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
    suite.addTest(loader.loadTestsFromTestCase(TestScriptsExecutable))
    # pydabu
    suite.addTest(loader.loadTestsFromName('pydabu_unittests.script_pydabu'))
    # json_schema_from_schema_org
    suite.addTest(
        loader.loadTestsFromName(
            'pydabu_unittests.script_json_schema_from_schema_org'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
