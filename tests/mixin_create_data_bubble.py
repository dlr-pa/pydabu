"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-05
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu create_data_bubble
"""

import json
import os.path
import pkgutil
import shutil
import subprocess
import tempfile

import jsonschema

try:
    from .data_path_class import DataPathClass
except (ModuleNotFoundError, ImportError):
    from data_path_class import DataPathClass


class MixinCreateDataBubble(DataPathClass):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-05
    """

    def test_create_data_bubble_00(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05

        env python3 script_pydabu.py ScriptPydabu.test_create_data_bubble_00
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, 'foo'), 'w') as fd:
                pass
            with open(os.path.join(tmpdir, 'bar'), 'w') as fd:
                pass
            subprocess.run(
                'pydabu create_data_bubble -directory ' + tmpdir,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=self.subprocess_timeout, check=True)
            for filename in ['.dabu.schema', '.dabu.json']:
                self.assertTrue(os.path.isfile(os.path.join(tmpdir, filename)))
            with open(os.path.join(tmpdir, '.dabu.json')) as fd:
                instance = json.load(fd)
            schema = json.loads(pkgutil.get_data(
                'dabu', 'schemas/dabu.schema'))
            jsonschema.validate(instance, schema)
            with open(os.path.join(tmpdir, '.dabu.schema')) as fd:
                schema = json.load(fd)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                # 'data integrity control' is a required property
                jsonschema.validate(instance, schema)
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, 'foo'), 'w') as fd:
                pass
            with open(os.path.join(tmpdir, 'bar'), 'w') as fd:
                pass
            subprocess.run(
                'pydabu create_data_bubble -directory .',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                check=True)
            for filename in ['.dabu.schema', '.dabu.json']:
                self.assertTrue(os.path.isfile(os.path.join(tmpdir, filename)))

    def test_create_data_bubble_01(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu create_data_bubble'.

        env python3 script_pydabu.py ScriptPydabu.test_create_data_bubble_01
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            for filename in ['a.na', '.checksum.sha256', 'LICENSE.txt',
                             'README.md', 'test.nc']:
                shutil.copyfile(os.path.join(self.test_dir_path[4], filename),
                                os.path.join(tmpdir, filename))
            subprocess.run(
                'pydabu create_data_bubble -directory . ' +
                '-checksum_from_file .checksum.sha256',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                check=True)
            for filename in ['.dabu.schema', '.dabu.json']:
                self.assertTrue(os.path.isfile(os.path.join(tmpdir, filename)))
            with open(os.path.join(tmpdir, '.dabu.json')) as fd:
                instance = json.load(fd)
            with open(os.path.join(tmpdir, '.dabu.schema')) as fd:
                schema = json.load(fd)
            jsonschema.validate(instance, schema)
        with tempfile.TemporaryDirectory() as tmpdir:
            for filename in ['a.na', 'LICENSE.txt', 'README.md', 'test.nc']:
                shutil.copyfile(os.path.join(self.test_dir_path[4], filename),
                                os.path.join(tmpdir, filename))
            subprocess.run(
                'pydabu create_data_bubble -directory .',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                check=True)
            for filename in ['.dabu.schema', '.dabu.json']:
                self.assertTrue(os.path.isfile(os.path.join(tmpdir, filename)))
            with open(os.path.join(tmpdir, '.dabu.json')) as fd:
                instance = json.load(fd)
            with open(os.path.join(tmpdir, '.dabu.schema')) as fd:
                schema = json.load(fd)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                # 'data integrity control' is a required property
                jsonschema.validate(instance, schema)
            for data in instance["data"]:
                if (("name" in data) and (data["name"] == "a.na")):
                    for (key, value) in [
                            ("algorithm", "sha512"),
                            ("encoding", "base64"),
                            ("hash",
                             "CZgzkcNy77d2n4W6vqbdRYFKp2rskJ3LCdRlVxiy3rmV"
                             "t7w+YOmSDH0jxC6xp1AWs+HUCMbGqt6Z+dAN1dUpaA==")]:
                        self.assertEqual(data["checksum"][key], value)
        with tempfile.TemporaryDirectory() as tmpdir:
            for filename in ['a.na', '.checksum.sha256', 'LICENSE.txt',
                             'README.md', 'test.nc']:
                shutil.copyfile(os.path.join(self.test_dir_path[4], filename),
                                os.path.join(tmpdir, filename))
            os.mkdir(os.path.join(tmpdir, '.git'))
            subprocess.run(
                'pydabu create_data_bubble -directory . ' +
                '-checksum_from_file .checksum.sha256',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                check=True)
            for filename in ['.dabu.schema', '.dabu.json']:
                self.assertTrue(os.path.isfile(os.path.join(tmpdir, filename)))
            with open(os.path.join(tmpdir, '.dabu.json')) as fd:
                instance = json.load(fd)
            with open(os.path.join(tmpdir, '.dabu.schema')) as fd:
                schema = json.load(fd)
            jsonschema.validate(instance, schema)
