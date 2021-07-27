"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-04
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the package data of the module dabu
"""

import unittest


class package_data(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-04
    """

    def test_package_data_available(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        import os.path
        import sys
        import dabu
        for dataname in ['dabu.schema', 'dabu_requires.schema']:
            self.assertTrue(
                os.path.isfile(
                    os.path.join(os.path.dirname(sys.modules['dabu'].__file__),
                                 'schemas',
                                 dataname)))

    def test_package_data_readable(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        import json
        import jsonschema
        import pkgutil
        import dabu
        for dataname in ['schemas/dabu.schema',
                         'schemas/dabu_requires.schema']:
            data = pkgutil.get_data('dabu', dataname)
            schema = json.loads(data)
            jsonschema.Draft4Validator.check_schema(schema)
