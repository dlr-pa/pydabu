"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-07-14
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu data_bubble2jsonld

Or you can run only one test from this file, e. g.::

  pytest-3 -s -k test_data_bubble2jsonld script_pydabu.py
"""

import os.path
import shutil
import subprocess
import tempfile

try:
    from .data_path_class import DataPathClass
except (ModuleNotFoundError, ImportError):
    from data_path_class import DataPathClass

# pylint: disable=too-few-public-methods


class MixinDataBubble2jsonld(DataPathClass):
    """
    :Author: Daniel Mohr
    :Date: 2021-07-14
    """

    def test_data_bubble2jsonld(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-07-14
        You can run onyl this test, e. g.::

          python3 script_pydabu.py script_pydabu.test_data_bubble2jsonld

          pytest-3 -s -k test_data_bubble2jsonld script_pydabu.py
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            for filename in ['a.na', '.checksum.sha256', '.dabu.json',
                             '.dabu.schema', 'LICENSE.txt', 'README.md',
                             'test.nc']:
                shutil.copyfile(os.path.join(self.test_dir_path[4], filename),
                                os.path.join(tmpdir, filename))
            for param in ['',
                          ' -author "Daniel Mohr"',
                          ' -author "{\\"name\\": \\"Daniel Mohr\\", '
                          '\\"identifier\\": '
                          '{\\"propertyID\\": \\"https://orcid.org/\\", '
                          '\\"name\\": \\"ORCID\\", '
                          '\\"value\\": \\"0000-0002-9382-6586\\", '
                          '\\"url\\": '
                          '\\"https://orcid.org/0000-0002-9382-6586\\"}}"',
                          ' -author "[{\\"name\\": \\"er\\"}, '
                          '{\\"name\\": \\"sie\\"}, {\\"name\\": \\"es\\"}]"']:
                cmd = 'pydabu data_bubble2jsonld -directory .' + param
                subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                    check=True)
                subprocess.run(
                    'pydabu check_data_bubble -dir .' +
                    ' -dabu_instance_file .dabu.json-ld ' +
                    '-dabu_schema_file .dabu.json-ld.schema',
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                    check=True)
                for filename in ['.dabu.json-ld', '.dabu.json-ld.schema']:
                    os.remove(os.path.join(tmpdir, filename))
