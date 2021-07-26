"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-07-21
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the package data of the module dabu

You can run this file directly::

  env python3 script_pydabu.py
  pytest-3 script_pydabu.py

Or you can run only one test, e. g.::

  pytest-3 -k test_create_data_bubble_00 script_pydabu.py
"""

import os.path
import sys
import unittest

try:
    from .mixin_analyse_data_structure import mixin_analyse_data_structure
    from .mixin_check_nasa_ames_format import mixin_check_nasa_ames_format
    from .mixin_check_netcdf_file import mixin_check_netcdf_file
    from .mixin_check_file_format import mixin_check_file_format
    from .mixin_common_json_format import mixin_common_json_format
    from .mixin_create_data_bubble import mixin_create_data_bubble
    from .mixin_check_data_bubble import mixin_check_data_bubble
    from .mixin_listschemas import mixin_listschemas
    from .mixin_basic_sub_commands import mixin_basic_sub_commands
    from .mixin_data_bubble2jsonld import mixin_data_bubble2jsonld
except (ModuleNotFoundError, ImportError):
    from mixin_analyse_data_structure import mixin_analyse_data_structure
    from mixin_check_nasa_ames_format import mixin_check_nasa_ames_format
    from mixin_check_netcdf_file import mixin_check_netcdf_file
    from mixin_check_file_format import mixin_check_file_format
    from mixin_common_json_format import mixin_common_json_format
    from mixin_create_data_bubble import mixin_create_data_bubble
    from mixin_check_data_bubble import mixin_check_data_bubble
    from mixin_listschemas import mixin_listschemas
    from mixin_basic_sub_commands import mixin_basic_sub_commands
    from mixin_data_bubble2jsonld import mixin_data_bubble2jsonld

class mixin_data_bubble():
    """
    :Author: Daniel Mohr
    :Date: 2021-03-05
    """

    def test_data_bubble(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05

        This test checks the available test data.
        """
        for test_dir_path in self.test_dir_path[0:4]:
            self.assertTrue(os.path.isdir(test_dir_path))
            for fn in ['LICENSE.txt', 'README.md']:
                self.assertTrue(
                    os.path.isfile(os.path.join(test_dir_path, fn)))


class scripty_pydabu(
        unittest.TestCase,
        mixin_basic_sub_commands, mixin_data_bubble,
        mixin_analyse_data_structure, mixin_check_netcdf_file,
        mixin_check_nasa_ames_format, mixin_check_file_format,
        mixin_common_json_format, mixin_create_data_bubble,
        mixin_check_data_bubble, mixin_listschemas,
        mixin_data_bubble2jsonld):
    """
    :Author: Daniel Mohr
    :Date: 2021-07-21
    """
    try:
        datapath = sys.modules['pydabu_unittests'].__file__
    except KeyError:
        datapath = ''
    test_dir_path = []
    for dir_name in ['00', '01', '02', '03', '04']:
        test_dir_path.append(os.path.join(
            os.path.dirname(datapath),
            'data', 'data_bubble', dir_name))
    subprocess_timeout = 5

if __name__ == '__main__':
    unittest.main(verbosity=2)
