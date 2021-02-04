"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-04
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

aggregation of tests
"""


import unittest


class test_module_import(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-04
    """

    def test_module_import(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        import dabu
        import dabu.analyse_data_structure
        import dabu.check_netcdf_file
        import dabu.analyse_file_format
        import dabu.scripts


def module(suite):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-04
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    running tests for the module
    """
    print('running tests for the module')
    loader = unittest.defaultTestLoader
    suite.addTest(loader.loadTestsFromTestCase(test_module_import))
    # dabu.schemas
    suite.addTest(loader.loadTestsFromName('pydabu_unittests.package_data'))


def scripts(suite):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-04
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    running tests for the scripts
    """
    print('running tests for the scripts')
    raise NotImplementedError
