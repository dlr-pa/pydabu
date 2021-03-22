"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-22
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu.py data_bubble2jsonld

Or you can run only one test from this file, e. g.::

  pytest-3 -k test_data_bubble2jsonld script_pydabu.py
"""

import os.path
import subprocess
import tempfile

class mixin_data_bubble2jsonld():
    """
    :Author: Daniel Mohr
    :Date: 2021-03-22
    """

    def test_data_bubble2jsonld(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-22
        You can run onyl this test, e. g.::

          pytest-3 -k test_basic_sub_commands script_pydabu.py
        """
        import shutil
        with tempfile.TemporaryDirectory() as tmpdir:
            for fn in ['a.na', '.checksum.sha256', '.dabu.json',
                       '.dabu.schema', 'LICENSE.txt', 'README.md',
                       'test.nc']:
                shutil.copyfile(os.path.join(self.test_dir_path[4], fn),
                                os.path.join(tmpdir, fn))
            cp = subprocess.run(
                ['pydabu.py data_bubble2jsonld -directory .'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                check=True)
            cp = subprocess.run(
                ['pydabu.py check_data_bubble -dir .' +
                 ' -dabu_instance_file .dabu.json-ld ' +
                 '-dabu_schema_file .dabu.json-ld.schema'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                check=True)
        with tempfile.TemporaryDirectory() as tmpdir:
            for fn in ['a.na', '.checksum.sha256', '.dabu.json',
                       '.dabu.schema', 'LICENSE.txt', 'README.md',
                       'test.nc']:
                shutil.copyfile(os.path.join(self.test_dir_path[4], fn),
                                os.path.join(tmpdir, fn))
            cp = subprocess.run(
                ['pydabu.py data_bubble2jsonld -directory . ' +
                 '-author "Daniel Mohr"'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                check=True)
            cp = subprocess.run(
                ['pydabu.py check_data_bubble -dir .' +
                 ' -dabu_instance_file .dabu.json-ld ' +
                 '-dabu_schema_file .dabu.json-ld.schema'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                check=True)
