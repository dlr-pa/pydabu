"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-08 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import json


def print_json_output(result, output_format):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-08 (last change).

    prints the output
    """
    if 'json' in output_format:
        print(json.dumps(result))
    elif 'json1' in output_format:
        print(json.dumps(result, indent=1))
    elif 'human_readable' in output_format:
        print(json.dumps(result, indent=1))
