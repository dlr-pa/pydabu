"""
Author: Daniel Mohr.

Date: 2017-03-07, 2021-02-17 (last change).

License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

Ported from pfu on 2021-02-17 by Daniel Mohr
(author of original code and main author of this file).
"""

import base64
import hashlib
import os


def create_checksum(data_file_name,
                    algorithm='sha512',
                    encoding='base64',
                    buf_size=524288):  # 1024*512 Bytes = 512 kB
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-17 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    Calculate hash(es) for data_file_name

    :param data_file_name: file name of the file to analyse
    :param algorithm: algorithm from hashlib to use
                      (have to be in hashlib.algorithms_guaranteed)
    :param encoding: encoding to use (one of base16, base32 or base64)
    :param buf_size: this number of Bytes is read and processed at once

    :return: a byte array with the hash in the given encoding
    """
    codings = {'hex': base64.b16encode,
               'base16': base64.b16encode,
               'Base16': base64.b16encode,
               'base32': base64.b32encode,
               'Base32': base64.b32encode,
               'base64': base64.b64encode,
               'Base64': base64.b64encode}
    hash_byte_array = None
    cal_hash = hashlib.new(algorithm)
    encode = codings[encoding]
    with open(data_file_name, 'rb') as data_file:
        while data_file.tell() < os.path.getsize(data_file_name):
            buf = data_file.read(buf_size)
            cal_hash.update(buf)
        hash_byte_array = encode(cal_hash.digest())
    return hash_byte_array
