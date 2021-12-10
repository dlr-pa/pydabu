"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-19
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu check_file_format
"""

import json
import pkgutil
import subprocess

import jsonschema

try:
    from .data_path_class import DataPathClass
except (ModuleNotFoundError, ImportError):
    from data_path_class import DataPathClass


# pylint: disable=invalid-name
class MixinCheckFileFormat(DataPathClass):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-19
    """

    def test_check_file_format_00(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu check_file_format'.
        """
        # data bubble 00
        test_dir_path = self.test_dir_path[0]
        cps = []  # completed process instances
        cps.append(subprocess.run(
            'pydabu check_file_format',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=True))
        cps.append(subprocess.run(
            'pydabu check_file_format -d ' + test_dir_path,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=self.subprocess_timeout, check=True))
        self.assertEqual(cps[0].stdout, cps[1].stdout)
        cps.append(subprocess.run(
            'pydabu check_file_format -o json',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=True))
        schema = json.loads(pkgutil.get_data('dabu', 'schemas/dabu.schema'))
        for cpi in cps:
            instance = json.loads(cpi.stdout)
            jsonschema.validate(instance, schema)

    def test_check_file_format_01(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu check_file_format'.
        """
        # data bubble 01
        test_dir_path = self.test_dir_path[1]
        cpi = subprocess.run(
            'pydabu check_file_format -o json',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=True)
        instance = json.loads(cpi.stdout)
        for filename in ['schemas/dabu.schema',
                         'schemas/dabu_requires.schema']:
            schema = json.loads(pkgutil.get_data('dabu', filename))
            jsonschema.validate(instance, schema)

    def test_check_file_format_02(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu check_file_format'.

        env python3 script_pydabu.py script_pydabu.test_check_file_format_02
        """
        # data bubble 02
        test_dir_path = self.test_dir_path[2]
        cpi = subprocess.run(
            'pydabu check_file_format -o json',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=True)
        instance = json.loads(cpi.stdout)
        for filename in ['schemas/dabu.schema',
                         'schemas/dabu_requires.schema']:
            schema = json.loads(pkgutil.get_data('dabu', filename))
            jsonschema.validate(instance, schema)

    def test_check_file_format_03(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-08

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu check_file_format'.
        """
        # data bubble 03
        test_dir_path = self.test_dir_path[3]
        cpi = subprocess.run(
            'pydabu check_file_format -o json',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
            check=True)
        instance = json.loads(cpi.stdout)
        for filename in ['schemas/dabu.schema',
                         'schemas/dabu_requires.schema']:
            schema = json.loads(pkgutil.get_data('dabu', filename))
            jsonschema.validate(instance, schema)

    def test_check_file_format_03_output(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-08

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu check_file_format'.
        """
        # data bubble 03
        test_dir_path = self.test_dir_path[3]
        schema = json.loads(pkgutil.get_data(
            'dabu', 'schemas/dabu.schema'))
        required_schema = json.loads(pkgutil.get_data(
            'dabu', 'schemas/dabu_requires.schema'))
        for outputformat in ['', ' -o json', ' -o json1',
                             ' -o human_readable']:
            cpi = subprocess.run(
                'pydabu check_file_format' + outputformat,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=test_dir_path, timeout=self.subprocess_timeout,
                check=True)
            instance = json.loads(cpi.stdout)
            for myschema in [schema, required_schema]:
                jsonschema.validate(instance, myschema)

    def test_check_file_format_01_02_03_checksums(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-17

        This test uses the data in 'data/data_bubble' to test the checksums
        of the script 'pydabu check_file_format'.

        env python3 script_pydabu.py \
          script_pydabu.test_check_file_format_01_02_03_checksums
        """
        # data bubble 01, 02, 03
        schema = json.loads(pkgutil.get_data(
            'dabu', 'schemas/dabu.schema'))
        required_schema = json.loads(pkgutil.get_data(
            'dabu', 'schemas/dabu_requires.schema'))
        checksum_files = ['',
                          '.checksum.sha512',  # 01
                          '.checksum',  # 02
                          '.checksum.sha256']  # 03
        for test_path_n in range(1, 4):
            test_dir_path = self.test_dir_path[test_path_n]
            for flags in [
                    ' -skip_creating_checksums',
                    ' -checksum_from_file ' + checksum_files[test_path_n]]:
                # check some command line parameters
                cpi = subprocess.run(
                    'pydabu check_file_format' + flags,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True, cwd=test_dir_path,
                    timeout=self.subprocess_timeout, check=True)
                instance = json.loads(cpi.stdout)
                for myschema in [schema, required_schema]:
                    jsonschema.validate(instance, myschema)

    def test_check_file_format_02_checksums(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-17

        This test uses the data in 'data/data_bubble' to test the checksums
        of the script 'pydabu check_file_format'.
        """
        # data bubble 02
        cp1 = subprocess.run(
            'pydabu check_file_format',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=self.test_dir_path[2],
            timeout=self.subprocess_timeout, check=True)
        instance1 = json.loads(cp1.stdout)
        cp2 = subprocess.run(
            'pydabu check_file_format -checksum_from_file .checksum',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=self.test_dir_path[2],
            timeout=self.subprocess_timeout, check=True)
        instance2 = json.loads(cp2.stdout)
        for i in range(len(instance1['data'])):
            for j in range(len(instance2['data'])):
                if (instance1['data'][i]['name'] ==
                        instance2['data'][j]['name']):
                    ind1 = i
                    ind2 = j
                    break
            self.assertEqual(instance1['data'][ind1]['checksum']['hash'],
                             instance2['data'][ind2]['checksum']['hash'])
