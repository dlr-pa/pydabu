"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-10 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os

import dabu


def run_listschemas(args):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-10 (last change).

    :param args: namespace return from ArgumentParser.parse_args
    """
    for schema_name in os.listdir(os.path.join(dabu.__path__[0], 'schemas')):
        print(os.path.join(dabu.__path__[0], 'schemas', schema_name))
