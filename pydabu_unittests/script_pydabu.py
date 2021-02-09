"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-09
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the package data of the module dabu
"""

import json
import jsonschema
import os.path
import pkgutil
import subprocess
import sys
import unittest


class scripty_pydabu(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-08
    """
    test_dir_path = []
    for dir_name in ['00', '01', '02', '03']:
        test_dir_path.append(os.path.join(
            os.path.dirname(sys.modules['pydabu_unittests'].__file__),
            'data', 'data_bubble', dir_name))

    def test_basic_sub_commands(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-09

        This test checks for the available sub-commands of pydabu.py
        """
        # check basic sub-commands
        cp = subprocess.run(
            ["pydabu.py analyse_data_structure"],
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
        for test_dir_path in [self.test_dir_path[0], self.test_dir_path[1]]:
            self.assertTrue(os.path.isdir(test_dir_path))
            self.assertTrue(
                os.path.isfile(os.path.join(test_dir_path, 'README.md')))

    def test_analyse_data_structure(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-09

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu.py analyse_data_structure'.
        """
        # data bubble 00
        test_dir_path = self.test_dir_path[0]
        cps = []  # completed process instances
        cps.append(subprocess.run(
            ['pydabu.py analyse_data_structure'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True))
        cps.append(subprocess.run(
            ['pydabu.py analyse_data_structure -d ' + test_dir_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True))
        self.assertEqual(cps[0].stdout, cps[1].stdout)
        cps.append(subprocess.run(
            ['pydabu.py analyse_data_structure -o json'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True))
        schema = json.loads(
            pkgutil.get_data(
                'dabu', 'schemas/analyse_data_structure_output.schema'))
        for cp in cps:
            instance = json.loads(cp.stdout)
            jsonschema.validate(instance, schema)
        # data bubble 01
        test_dir_path = self.test_dir_path[1]
        self.assertTrue(os.path.isdir(test_dir_path))
        self.assertTrue(
            os.path.isfile(os.path.join(test_dir_path, 'README.md')))
        cp = subprocess.run(
            ['pydabu.py analyse_data_structure'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True)

    def test_check_netcdf_file(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu.py check_netcdf_file'.
        """
        # data bubble 01
        test_dir_path = self.test_dir_path[1]
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
            shell=True, cwd=test_dir_path, timeout=3, check=False)
        self.assertEqual(cp.returncode, 2)  # check for error
        cp = subprocess.run(
            ['pydabu.py check_nasa_ames_format -f a.na'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True)

    def test_check_file_format_00(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu.py check_file_format'.
        """
        # data bubble 00
        test_dir_path = self.test_dir_path[0]
        cps = []  # completed process instances
        cps.append(subprocess.run(
            ['pydabu.py check_file_format'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True))
        cps.append(subprocess.run(
            ['pydabu.py check_file_format -d ' + test_dir_path],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True))
        self.assertEqual(cps[0].stdout, cps[1].stdout)
        cps.append(subprocess.run(
            ['pydabu.py check_file_format -o json'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True))
        schema = json.loads(pkgutil.get_data('dabu', 'schemas/dabu.schema'))
        for cp in cps:
            instance = json.loads(cp.stdout)
            jsonschema.validate(instance, schema)

    def test_check_file_format_01(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu.py check_file_format'.
        """
        # data bubble 01
        test_dir_path = self.test_dir_path[1]
        cp = subprocess.run(
            ['pydabu.py check_file_format -o json'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True)
        instance = json.loads(cp.stdout)
        for filename in ['schemas/dabu.schema', 'schemas/dabu_requires.schema']:
            schema = json.loads(pkgutil.get_data('dabu', filename))
            jsonschema.validate(instance, schema)

    def test_check_file_format_02(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu.py check_file_format'.
        """
        # data bubble 02
        test_dir_path = self.test_dir_path[2]
        cp = subprocess.run(
            ['pydabu.py check_file_format -o json'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True)
        instance = json.loads(cp.stdout)
        for filename in ['schemas/dabu.schema', 'schemas/dabu_requires.schema']:
            schema = json.loads(pkgutil.get_data('dabu', filename))
            jsonschema.validate(instance, schema)

    def test_check_file_format_03(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-08

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu.py check_file_format'.
        """
        # data bubble 03
        test_dir_path = self.test_dir_path[3]
        cp = subprocess.run(
            ['pydabu.py check_file_format -o json'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=3, check=True)
        instance = json.loads(cp.stdout)
        for filename in ['schemas/dabu.schema', 'schemas/dabu_requires.schema']:
            schema = json.loads(pkgutil.get_data('dabu', filename))
            jsonschema.validate(instance, schema)

    def test_check_file_format_03_output(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-08

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu.py check_file_format'.
        """
        # data bubble 03
        test_dir_path = self.test_dir_path[3]
        schema = json.loads(pkgutil.get_data(
            'dabu', 'schemas/dabu.schema'))
        required_schema = json.loads(pkgutil.get_data(
            'dabu', 'schemas/dabu_requires.schema'))
        for outputformat in ['', ' -o json', ' -o json1', ' -o human_readable']:
            cp = subprocess.run(
                ['pydabu.py check_file_format' + outputformat],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=test_dir_path, timeout=3, check=True)
            instance = json.loads(cp.stdout)
            for myschema in [schema, required_schema]:
                jsonschema.validate(instance, myschema)
