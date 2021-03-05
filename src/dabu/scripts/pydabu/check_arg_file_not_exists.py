"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-05 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import argparse
import os.path


def check_arg_file_not_exists(data):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-08 (last change).
    """
    if os.path.isfile(data):
        msg = '"%s" exists already' % data
        raise argparse.ArgumentTypeError(msg)
    return data
