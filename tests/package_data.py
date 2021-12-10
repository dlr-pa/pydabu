"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-04
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the package data of the module dabu
"""

import json
import os.path
import pkgutil
import sys
import unittest

import jsonschema


class PackageData(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-04
    """

    def test_package_data_available(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        # pylint: disable=unused-variable,unused-import
        # pylint: disable=bad-option-value,import-outside-toplevel
        import dabu
        for dataname in ['dabu.schema', 'dabu_requires.schema']:
            self.assertTrue(
                os.path.isfile(
                    os.path.join(os.path.dirname(sys.modules['dabu'].__file__),
                                 'schemas',
                                 dataname)))

    # pylint: disable=no-self-use
    def test_package_data_readable(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        # pylint: disable=unused-variable,unused-import
        # pylint: disable=bad-option-value,import-outside-toplevel
        import dabu
        for dataname in ['schemas/dabu.schema',
                         'schemas/dabu_requires.schema']:
            data = pkgutil.get_data('dabu', dataname)
            schema = json.loads(data)
            jsonschema.Draft4Validator.check_schema(schema)
