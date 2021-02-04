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

        This test checks for the available sub-commands of pydabu.py
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

    def test_data_data_bubble(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test checks the available test data.
        """
        import os.path
        import sys
        test_dir_path = os.path.join(
            os.path.dirname(sys.modules['pydabu_unittests'].__file__),
            'data', 'data_bubble', '01')
        self.assertTrue(os.path.isdir(test_dir_path))
        self.assertTrue(
            os.path.isfile(os.path.join(test_dir_path, 'README.md')))
        test_dir_path = os.path.join(
            os.path.dirname(sys.modules['pydabu_unittests'].__file__),
            'data', 'data_bubble', '02')
        self.assertTrue(os.path.isdir(test_dir_path))
        self.assertTrue(
            os.path.isfile(os.path.join(test_dir_path, 'README.md')))

    def test_check_data_structure(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu.py check_data_structure'.
        """
        import json
        import jsonschema
        import os.path
        import pkgutil
        import sys
        # data bubble 01
        test_dir_path = os.path.join(
            os.path.dirname(sys.modules['pydabu_unittests'].__file__),
            'data', 'data_bubble', '01')
        cp1 = subprocess.run(
            ['pydabu.py check_data_structure'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True)
        cp2 = subprocess.run(
            ['pydabu.py check_data_structure -d ' + test_dir_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        self.assertEqual(cp1.stdout, cp2.stdout)
        cp3 = subprocess.run(
            ['pydabu.py check_data_structure -o json'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True)
        schema = json.loads(
            pkgutil.get_data(
                'dabu', 'schemas/check_data_structure_output.schema'))
        instance1 = json.loads(cp1.stdout)
        instance2 = json.loads(cp2.stdout)
        instance3 = json.loads(cp3.stdout)
        for instance in [instance1, instance2, instance3]:
            jsonschema.validate(instance, schema)
        # data bubble 02
        test_dir_path = os.path.join(
            os.path.dirname(sys.modules['pydabu_unittests'].__file__),
            'data', 'data_bubble', '02')
        self.assertTrue(os.path.isdir(test_dir_path))
        self.assertTrue(
            os.path.isfile(os.path.join(test_dir_path, 'README.md')))
        cp = subprocess.run(
            ['pydabu.py check_data_structure'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True)

    def test_check_netcdf_file(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu.py check_netcdf_file'.
        """
        import json
        import jsonschema
        import os.path
        import pkgutil
        import sys
        # data bubble 02
        test_dir_path = os.path.join(
            os.path.dirname(sys.modules['pydabu_unittests'].__file__),
            'data', 'data_bubble', '02')
        cp = subprocess.run(
            ['pydabu.py check_netcdf_file -f README.md'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=False)
        self.assertEqual(cp.returncode, 1)  # check for error
        cp = subprocess.run(
            ['pydabu.py check_netcdf_file -f foo'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=False)
        self.assertEqual(cp.returncode, 2)  # check for error

    def test_check_file_format_01(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu.py check_file_format'.
        """
        import json
        import jsonschema
        import pkgutil
        import os.path
        import sys
        # data bubble 01
        test_dir_path = os.path.join(
            os.path.dirname(sys.modules['pydabu_unittests'].__file__),
            'data', 'data_bubble', '01')
        cp1 = subprocess.run(
            ['pydabu.py check_file_format'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True)
        cp2 = subprocess.run(
            ['pydabu.py check_file_format -d ' + test_dir_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        self.assertEqual(cp1.stdout, cp2.stdout)
        cp3 = subprocess.run(
            ['pydabu.py check_file_format -o json'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True)
        schema = json.loads(pkgutil.get_data('dabu', 'schemas/dabu.schema'))
        instance1 = json.loads(cp1.stdout)
        instance2 = json.loads(cp2.stdout)
        instance3 = json.loads(cp3.stdout)
        for instance in [instance1, instance2, instance3]:
            jsonschema.validate(instance, schema)

    def test_check_file_format_02(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu.py check_file_format'.
        """
        import json
        import jsonschema
        import os.path
        import pkgutil
        import sys
        # data bubble 02
        test_dir_path = os.path.join(
            os.path.dirname(sys.modules['pydabu_unittests'].__file__),
            'data', 'data_bubble', '02')
        cp = subprocess.run(
            ['pydabu.py check_file_format -o json'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True)
        schema1 = json.loads(pkgutil.get_data('dabu', 'schemas/dabu.schema'))
        schema2 = json.loads(
            pkgutil.get_data('dabu', 'schemas/dabu_requires.schema'))
        instance = json.loads(cp.stdout)
        jsonschema.validate(instance, schema1)
        jsonschema.validate(instance, schema2)
