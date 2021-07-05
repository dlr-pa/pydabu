"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-05
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu check_data_bubble
"""

import json
import os.path
import subprocess
import tempfile


class mixin_check_data_bubble():
    """
    :Author: Daniel Mohr
    :Date: 2021-03-05
    """

    def test_check_data_bubble_00(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05
        """
        cp = subprocess.run(
            ['pydabu check_data_bubble -directory .'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, cwd=self.test_dir_path[4],
            timeout=self.subprocess_timeout, check=True)

    def test_check_data_bubble_01(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05
        """
        import shutil
        with tempfile.TemporaryDirectory() as tmpdir:
            for fn in ['a.na', '.checksum.sha256', 'LICENSE.txt', 'README.md',
                       'test.nc', '.dabu.json', '.dabu.schema']:
                shutil.copyfile(os.path.join(self.test_dir_path[4], fn),
                                os.path.join(tmpdir, fn))
            cp = subprocess.run(
                ['pydabu check_data_bubble -directory .'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=self.subprocess_timeout, check=True)
            self.assertEqual(len(cp.stderr), 0)
            # unknown schema error
            with open(os.path.join(tmpdir, '.dabu.schema')) as fd:
                schema = json.load(fd)
            schema["$schema"] = "foo"
            with open(os.path.join(tmpdir, '.dabu.schema'), 'w') as fd:
                json.dump(schema, fd)
            cp = subprocess.run(
                ['pydabu check_data_bubble -directory .'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=self.subprocess_timeout, check=False)
            with self.assertRaises(subprocess.CalledProcessError):
                cp.check_returncode()
            # warning, not schema
            del schema["$schema"]
            with open(os.path.join(tmpdir, '.dabu.schema'), 'w') as fd:
                json.dump(schema, fd)
            cp = subprocess.run(
                ['pydabu check_data_bubble -directory .'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=self.subprocess_timeout, check=True)
            self.assertTrue(len(cp.stderr) > 0)
            # check fail:
            fn = '.dabu.schema'
            shutil.copyfile(os.path.join(self.test_dir_path[4], fn),
                            os.path.join(tmpdir, fn))
            with open(os.path.join(tmpdir, '.dabu.json')) as fd:
                instance = json.load(fd)
            del instance["license"]
            for data in instance["data"]:
                if (("name" in data) and (data["name"] == "a.na")):
                    del data["checksum"]["hash"]
            with open(os.path.join(tmpdir, '.dabu.json'), 'w') as fd:
                json.dump(instance, fd)
            cp = subprocess.run(
                ['pydabu check_data_bubble -directory .'],
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
            cp = subprocess.run(
                ['pydabu check_data_bubble -directory .'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir,
                timeout=self.subprocess_timeout, check=True)
