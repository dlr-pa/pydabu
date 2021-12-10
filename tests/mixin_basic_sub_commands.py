"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-22
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script: pydabu

Or you can run only one test from this file, e. g.::

  pytest-3 -k test_basic_sub_commands script_pydabu.py
"""

import subprocess

try:
    from .data_path_class import DataPathClass
except (ModuleNotFoundError, ImportError):
    from data_path_class import DataPathClass


# pylint: disable=too-few-public-methods
class MixinBasicSubCommands(DataPathClass):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-22
    """

    def test_basic_sub_commands(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-22

        This test checks for the available sub-commands of pydabu

        You can run onyl this test, e. g.::

          pytest-3 -k test_basic_sub_commands script_pydabu.py
        """
        # check basic sub-commands
        for cmd in ['analyse_data_structure', 'check_file_format',
                    'listschemas']:
            subprocess.run(
                'pydabu ' + cmd,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=self.subprocess_timeout, check=True)
        for cmd in ['check_nasa_ames_format', 'check_netcdf_file',
                    'common_json_format', 'create_data_bubble',
                    'check_data_bubble', 'data_bubble2jsonld']:
            cpi = subprocess.run(
                'pydabu ' + cmd,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=self.subprocess_timeout, check=False)
            with self.assertRaises(subprocess.CalledProcessError):
                # parameter is necessary
                cpi.check_returncode()
        for cmd in ['analyse_data_structure', 'check_nasa_ames_format',
                    'check_netcdf_file', 'check_file_format',
                    'common_json_format', 'create_data_bubble',
                    'check_data_bubble', 'listschemas', 'data_bubble2jsonld']:
            subprocess.run(
                'pydabu ' + cmd + ' -h',
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=self.subprocess_timeout, check=True)
