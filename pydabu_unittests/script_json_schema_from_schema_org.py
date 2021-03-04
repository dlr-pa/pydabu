"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-04
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script json_schema_from_schema_org.py
"""

import unittest


class scripty_json_schema_from_schema_org(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-04
    """

    def test_dummy(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-04

        This test calls json_schema_from_schema_org.py
        """
        import subprocess
        cp = subprocess.run(
            ["json_schema_from_schema_org.py dummy"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
