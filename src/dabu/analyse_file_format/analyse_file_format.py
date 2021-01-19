"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-01-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os.path


def analyse_file_format(path):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-01-19 (last change).

    Analyse the file format of the files stored in result.

    :param path: directory path to analyse
    """
    _, file_extension = os.path.splitext(path)
    return file_extension
