"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-07-30
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os.path
import sys

# pylint: disable=too-few-public-methods


class DataPathClass():
    """
    :Author: Daniel Mohr
    :Date: 2021-07-30
    """
    try:
        datapath = sys.modules['tests'].__file__
    except KeyError:
        datapath = ''
    test_dir_path = []
    for dir_name in ['00', '01', '02', '03', '04']:
        test_dir_path.append(os.path.join(
            os.path.dirname(datapath),
            'data', 'data_bubble', dir_name))
    subprocess_timeout = 5
