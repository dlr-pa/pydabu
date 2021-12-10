"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-07-30
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the package data of the module dabu

You can run this file directly::

  env python3 script_pydabu.py
  pytest-3 script_pydabu.py

Or you can run only one test, e. g.::

  pytest-3 -k test_create_data_bubble_00 script_pydabu.py
"""

import os.path
import unittest

try:
    from .data_path_class import DataPathClass
    from .mixin_analyse_data_structure import MixinAnalyseDataStructure
    from .mixin_check_nasa_ames_format import MixinCheckNasaAmesFormat
    from .mixin_check_netcdf_file import MixinCheckNetcdfFile
    from .mixin_check_file_format import MixinCheckFileFormat
    from .mixin_common_json_format import MixinCommonJsonFormat
    from .mixin_create_data_bubble import MixinCreateDataBubble
    from .mixin_check_data_bubble import MixinCheckDataBubble
    from .mixin_listschemas import MixinListschemas
    from .mixin_basic_sub_commands import MixinBasicSubCommands
    from .mixin_data_bubble2jsonld import MixinDataBubble2jsonld
except (ModuleNotFoundError, ImportError):
    from data_path_class import DataPathClass
    from mixin_analyse_data_structure import MixinAnalyseDataStructure
    from mixin_check_nasa_ames_format import MixinCheckNasaAmesFormat
    from mixin_check_netcdf_file import MixinCheckNetcdfFile
    from mixin_check_file_format import MixinCheckFileFormat
    from mixin_common_json_format import MixinCommonJsonFormat
    from mixin_create_data_bubble import MixinCreateDataBubble
    from mixin_check_data_bubble import MixinCheckDataBubble
    from mixin_listschemas import MixinListschemas
    from mixin_basic_sub_commands import MixinBasicSubCommands
    from mixin_data_bubble2jsonld import MixinDataBubble2jsonld


# pylint: disable=too-few-public-methods
class MixinDataBubble(DataPathClass):
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
            for filename in ['LICENSE.txt', 'README.md']:
                self.assertTrue(
                    os.path.isfile(os.path.join(test_dir_path, filename)))


# pylint: disable=too-many-ancestors
class ScriptPydabu(
        unittest.TestCase,
        MixinBasicSubCommands, MixinDataBubble,
        MixinAnalyseDataStructure, MixinCheckNetcdfFile,
        MixinCheckNasaAmesFormat, MixinCheckFileFormat,
        MixinCommonJsonFormat, MixinCreateDataBubble,
        MixinCheckDataBubble, MixinListschemas,
        MixinDataBubble2jsonld):
    """
    :Author: Daniel Mohr
    :Date: 2021-07-21
    """


if __name__ == '__main__':
    unittest.main(verbosity=2)
