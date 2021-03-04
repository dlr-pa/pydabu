"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-08 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import argparse
import os.path


def check_arg_file(data):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-01-29 (last change).
    """
    if not os.path.isfile(data):
        msg = '"%s" is not a file' % data
        raise argparse.ArgumentTypeError(msg)
    return data
