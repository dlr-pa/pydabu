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
import subprocess
import tempfile


class mixin_data_bubble2jsonld():
    """
    :Author: Daniel Mohr
    :Date: 2021-07-14
    """

    def test_data_bubble2jsonld(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-07-14
        You can run onyl this test, e. g.::

          pytest-3 -s -k test_data_bubble2jsonld script_pydabu.py
        """
        import shutil
        with tempfile.TemporaryDirectory() as tmpdir:
            for fn in ['a.na', '.checksum.sha256', '.dabu.json',
                       '.dabu.schema', 'LICENSE.txt', 'README.md',
                       'test.nc']:
                shutil.copyfile(os.path.join(self.test_dir_path[4], fn),
                                os.path.join(tmpdir, fn))
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
                cp = subprocess.run(
                    cmd,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                    check=True)
                cp = subprocess.run(
                    'pydabu check_data_bubble -dir .' +
                    ' -dabu_instance_file .dabu.json-ld ' +
                    '-dabu_schema_file .dabu.json-ld.schema',
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    shell=True, cwd=tmpdir, timeout=self.subprocess_timeout,
                    check=True)
                for fn in ['.dabu.json-ld', '.dabu.json-ld.schema']:
                    os.remove(os.path.join(tmpdir, fn))
