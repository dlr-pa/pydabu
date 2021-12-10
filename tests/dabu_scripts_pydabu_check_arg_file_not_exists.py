"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-05
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the module dabu.scripts.pydabu.check_arg_file_not_exists

You can run this file directly:

env python3 dabu_scripts_pydabu_check_arg_file_not_exists.py

Or you can run only one test, e. g.:

env python3 dabu_scripts_pydabu_check_arg_file_not_exists.py \
  CheckArgFileNotExists.test_check_arg_file_not_exists
"""

import argparse
import os.path
import tempfile
import unittest


class CheckArgFileNotExists(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-05
    """

    def test_check_arg_file_not_exists(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05
        """
        # pylint: disable=bad-option-value,import-outside-toplevel
        from dabu.scripts.pydabu import check_arg_file_not_exists as cafne
        with tempfile.TemporaryDirectory() as tmpdir:
            # pylint: disable=unused-variable
            with open(os.path.join(tmpdir, 'foo'), 'w') as fd:
                pass
            cafne.check_arg_file_not_exists(os.path.join(tmpdir, 'bar'))
            with self.assertRaises(argparse.ArgumentTypeError):
                cafne.check_arg_file_not_exists(os.path.join(tmpdir, 'foo'))


if __name__ == '__main__':
    unittest.main(verbosity=2)
