"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-19
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu analyse_data_structure
"""

import json
import os.path
import pkgutil
import subprocess

import jsonschema

try:
    from .data_path_class import DataPathClass
except (ModuleNotFoundError, ImportError):
    from data_path_class import DataPathClass


# pylint: disable=too-few-public-methods
class MixinAnalyseDataStructure(DataPathClass):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-19
    """

    def test_analyse_data_structure(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-09

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu analyse_data_structure'.
        """
        # data bubble 00
        test_dir_path = self.test_dir_path[0]
        cps = []  # completed process instances
        cps.append(subprocess.run(
            'pydabu analyse_data_structure',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=True))
        cps.append(subprocess.run(
            'pydabu analyse_data_structure -d ' + test_dir_path,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=self.subprocess_timeout, check=True))
        self.assertEqual(cps[0].stdout, cps[1].stdout)
        cps.append(subprocess.run(
            'pydabu analyse_data_structure -o json',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=True))
        schema = json.loads(
            pkgutil.get_data(
                'dabu', 'schemas/analyse_data_structure_output.schema'))
        for cpi in cps:
            instance = json.loads(cpi.stdout)
            jsonschema.validate(instance, schema)
        # data bubble 01
        test_dir_path = self.test_dir_path[1]
        self.assertTrue(os.path.isdir(test_dir_path))
        self.assertTrue(
            os.path.isfile(os.path.join(test_dir_path, 'README.md')))
        subprocess.run(
            'pydabu analyse_data_structure',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=True)
