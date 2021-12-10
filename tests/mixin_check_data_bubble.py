"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-05, 2021-07-30
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu check_data_bubble
"""

import json
import os.path
import shutil
import subprocess
import tempfile

try:
    from .data_path_class import DataPathClass
except (ModuleNotFoundError, ImportError):
    from data_path_class import DataPathClass


class MixinCheckDataBubble(DataPathClass):
    """
    :Author: Daniel Mohr
    :Date: 2021-07-30
    """

    def test_check_data_bubble_00(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05

        env python3 script_pydabu.py ScriptPydabu.test_check_data_bubble_00
        """
        subprocess.run(
            'pydabu check_data_bubble -directory .',
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=self.test_dir_path[4],
            timeout=self.subprocess_timeout, check=True)

    def test_check_data_bubble_01(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            for filename in ['a.na', '.checksum.sha256', 'LICENSE.txt',
                             'README.md', 'test.nc', '.dabu.json',
                             '.dabu.schema']:
                shutil.copyfile(os.path.join(self.test_dir_path[4], filename),
                                os.path.join(tmpdir, filename))
            cpi = subprocess.run(
                'pydabu check_data_bubble -directory .',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=self.subprocess_timeout, check=True)
            self.assertEqual(len(cpi.stderr), 0)
            # unknown schema error
            with open(os.path.join(tmpdir, '.dabu.schema')) as fd:
                schema = json.load(fd)
            schema["$schema"] = "foo"
            with open(os.path.join(tmpdir, '.dabu.schema'), 'w') as fd:
                json.dump(schema, fd)
            cpi = subprocess.run(
                'pydabu check_data_bubble -directory .',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=self.subprocess_timeout, check=False)
            with self.assertRaises(subprocess.CalledProcessError):
                cpi.check_returncode()
            # warning, not schema
            del schema["$schema"]
            with open(os.path.join(tmpdir, '.dabu.schema'), 'w') as fd:
                json.dump(schema, fd)
            cpi = subprocess.run(
                'pydabu check_data_bubble -directory .',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=self.subprocess_timeout, check=True)
            self.assertTrue(len(cpi.stderr) > 0)
            # check fail:
            filename = '.dabu.schema'
            shutil.copyfile(os.path.join(self.test_dir_path[4], filename),
                            os.path.join(tmpdir, filename))
            with open(os.path.join(tmpdir, '.dabu.json')) as fd:
                instance = json.load(fd)
            del instance["license"]
            for data in instance["data"]:
                if (("name" in data) and (data["name"] == "a.na")):
                    del data["checksum"]["hash"]
            with open(os.path.join(tmpdir, '.dabu.json'), 'w') as fd:
                json.dump(instance, fd)
            cpi = subprocess.run(
                'pydabu check_data_bubble -directory .',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=self.subprocess_timeout, check=True)

    def test_create_check_data_bubble(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05

        This test uses the data in 'data/data_bubble' to test the output
        of the script 'pydabu create_data_bubble' and
        'pydabu check_data_bubble'.
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
            subprocess.run(
                'pydabu check_data_bubble -directory .',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=self.subprocess_timeout, check=True)
