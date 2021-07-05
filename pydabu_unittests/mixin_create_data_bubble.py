"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-05
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu create_data_bubble
"""

import json
import jsonschema
import os.path
import pkgutil
import subprocess
import tempfile


class mixin_create_data_bubble():
    """
    :Author: Daniel Mohr
    :Date: 2021-03-05
    """

    def test_create_data_bubble_00(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            with open(os.path.join(tmpdir, 'foo'), 'w') as fd:
                pass
            with open(os.path.join(tmpdir, 'bar'), 'w') as fd:
                pass
            cp = subprocess.run(
                ['pydabu create_data_bubble -directory ' + tmpdir],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=self.subprocess_timeout, check=True)
            for fn in ['.dabu.schema', '.dabu.json']:
                self.assertTrue(os.path.isfile(os.path.join(tmpdir, fn)))
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
            cp = subprocess.run(
                ['pydabu create_data_bubble -directory .'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                check=True)
            for fn in ['.dabu.schema', '.dabu.json']:
                self.assertTrue(os.path.isfile(os.path.join(tmpdir, fn)))

    def test_create_data_bubble_01(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu create_data_bubble'.
        """
        import shutil
        with tempfile.TemporaryDirectory() as tmpdir:
            for fn in ['a.na', '.checksum.sha256', 'LICENSE.txt', 'README.md',
                       'test.nc']:
                shutil.copyfile(os.path.join(self.test_dir_path[4], fn),
                                os.path.join(tmpdir, fn))
            cp = subprocess.run(
                ['pydabu create_data_bubble -directory . ' +
                 '-checksum_from_file .checksum.sha256'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                check=True)
            for fn in ['.dabu.schema', '.dabu.json']:
                self.assertTrue(os.path.isfile(os.path.join(tmpdir, fn)))
            with open(os.path.join(tmpdir, '.dabu.json')) as fd:
                instance = json.load(fd)
            with open(os.path.join(tmpdir, '.dabu.schema')) as fd:
                schema = json.load(fd)
            jsonschema.validate(instance, schema)
        with tempfile.TemporaryDirectory() as tmpdir:
            for fn in ['a.na', 'LICENSE.txt', 'README.md', 'test.nc']:
                shutil.copyfile(os.path.join(self.test_dir_path[4], fn),
                                os.path.join(tmpdir, fn))
            cp = subprocess.run(
                ['pydabu create_data_bubble -directory .'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                check=True)
            for fn in ['.dabu.schema', '.dabu.json']:
                self.assertTrue(os.path.isfile(os.path.join(tmpdir, fn)))
            with open(os.path.join(tmpdir, '.dabu.json')) as fd:
                instance = json.load(fd)
            with open(os.path.join(tmpdir, '.dabu.schema')) as fd:
                schema = json.load(fd)
            with self.assertRaises(jsonschema.exceptions.ValidationError):
                # 'data integrity control' is a required property
                jsonschema.validate(instance, schema)
            for data in instance["data"]:
                if (("name" in data) and (data["name"] == "a.na")):
                    for (k, v) in [
                            ("algorithm", "sha512"),
                            ("encoding", "base64"),
                            ("hash",
                             "CZgzkcNy77d2n4W6vqbdRYFKp2rskJ3LCdRlVxiy3rmVt7w+YOmSDH0jxC6xp1AWs+HUCMbGqt6Z+dAN1dUpaA==")]:
                        self.assertEqual(data["checksum"][k], v)
        with tempfile.TemporaryDirectory() as tmpdir:
            for fn in ['a.na', '.checksum.sha256', 'LICENSE.txt', 'README.md',
                       'test.nc']:
                shutil.copyfile(os.path.join(self.test_dir_path[4], fn),
                                os.path.join(tmpdir, fn))
            os.mkdir(os.path.join(tmpdir, '.git'))
            cp = subprocess.run(
                ['pydabu create_data_bubble -directory . ' +
                 '-checksum_from_file .checksum.sha256'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                check=True)
            for fn in ['.dabu.schema', '.dabu.json']:
                self.assertTrue(os.path.isfile(os.path.join(tmpdir, fn)))
            with open(os.path.join(tmpdir, '.dabu.json')) as fd:
                instance = json.load(fd)
            with open(os.path.join(tmpdir, '.dabu.schema')) as fd:
                schema = json.load(fd)
            jsonschema.validate(instance, schema)
