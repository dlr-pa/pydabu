"""
Author: Daniel Mohr.

Date: 2017-03-07, 2021-02-17 (last change).

License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

Ported from pfu on 2021-02-17 by Daniel Mohr
(author of original code and main author of this file).
"""

import base64
import hashlib
import logging
import os
import re


class ExtractHashFromChecksumFile():
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-17 (last change).
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    class to extract check checksums from a file
    """
    # pylint: disable=too-few-public-methods
    # we allow here many hash functions, but better only use common ones,
    # e. g.: md5, sha256, sha512
    # (md5 is only acceptable for very small files!)
    hashfcts = hashlib.algorithms_guaranteed
    hashtype = {128: ('sha512', 'base16'),  # other hashes are hard to
                104: ('sha512', 'base32'),  # detect by length
                88: ('sha512', 'base64'),
                64: ('sha256', 'base16'),
                56: ('sha256', 'base32'),
                44: ('sha256', 'base64'),
                32: ('md5', 'base16 or base32'),
                24: ('md5', 'base64')}
    decodings = {'hex': base64.b16decode,
                 'base16': base64.b16decode,
                 'Base16': base64.b16decode,
                 'base32': base64.b32decode,
                 'Base32': base64.b32decode,
                 'base64': base64.b64decode,
                 'Base64': base64.b64decode}
    codings = {'hex': base64.b16encode,
               'base16': base64.b16encode,
               'Base16': base64.b16encode,
               'base32': base64.b32encode,
               'Base32': base64.b32encode,
               'base64': base64.b64encode,
               'Base64': base64.b64encode}
    regexps = [
        re.compile(
            r"(?P<hash>[0-9a-zA-Z/+=]+) [ \*]{1}(?P<filename>.+) \(bytes "
            r"(?P<start>[0-9]+) - (?P<stop>[0-9]+)\)$"),
        re.compile(r"(?P<hash>[0-9a-zA-Z/+=]+) [ \*]{1}(?P<filename>.+)$"),
        re.compile(r"(?P<type>MD5|SHA256|SHA512|SHA1|SHA224|SHA384)[ ]{0,1}\("
                   r"(?P<filename>.+)\)[ ]{0,1}= (?P<hash>[0-9a-zA-Z/+=]+)$")]

    def __init__(self,
                 checksum_file,
                 buf_size=524288,  # 1024*512 Bytes = 512 kB
                 level=20):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-02-25, 2021-02-17 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        class to extract check checksums from a file

        :param checksum_file: File to read the checksums from.
        :param buf_size: Files will be read in chunks of the given amount of
                         Bytes. This should be a factor of the data handled by
                         the hash function (e. g. 64 Bytes for md5, 64 Bytes
                         for sha256, 128 Bytes for sha512).
        :param level: Set how verbose should be the output. This is the level
                      of logging. Lower numbers give more output. The parameter
                      is a number between 1 and 50.
        """
        self.hash_file_name = checksum_file
        self.buf_size = buf_size
        self.level = level
        # extract hash from checksum file
        self.log = logging.getLogger("ehfcf")
        self.log.setLevel(self.level)
        self.hash_dict = dict()
        self._read_hash_file()  # read and analyse checksum file

    def __call__(self, file_name, encoding=None):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2021-02-17 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        :param file_name: file_name to search
        :param encoding: define the encoding of the returned hash string

        :return: return the hash string, the hash encoding and the source
                 file name (where the data was read from)
                 or None (if file_name not available)
        """
        if file_name in self.hash_dict:
            # only return first hash
            hash_info = self.hash_dict[file_name][0]
            if encoding is not None:  # adapt hash string
                hash_info = list(hash_info)
                # RFC 3548 defines the following alphabets:
                # base64: ABCDEFGHIJKLMNOPQRSTUVWXYZ
                #         abcdefghijklmnopqrstuvwxyz0123456789-_
                # base32: abcdefghijklmnopqrstuvwxyz234567
                # base16: 0123456789ABCDEF
                if hash_info[1][1] in ['hex', 'base16', 'Base16']:
                    hash_info[0] = hash_info[0].upper()
                elif hash_info[1][1] in ['base32', 'Base32']:
                    hash_info[0] = hash_info[0].lower()
                hash_info[0] = self.decodings[hash_info[1][1]](hash_info[0])
                hash_info[0] = self.codings[encoding](hash_info[0])
                if isinstance(hash_info[0], bytes):
                    hash_info[0] = hash_info[0].decode(encoding='utf-8')
                hash_info = tuple(hash_info)
            return hash_info
        else:
            return None

    def _determine_hash_encode(self, hash_string, hashfilename=None):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-03-02 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        Try to determine hash function and encode from hash.
        If this is not possible assume the file extension gives the hash type.

        :param hash_string: the hash to analyse
        :param hashfilename: file name of the hash
                             (if hash is not unique the file extension is used)

        :return: tuple of hash algorithm and encoding
                 or None on error
        """
        hash_encode = None
        if len(hash_string) in self.hashtype:
            hash_encode = self.hashtype[len(hash_string)]
            if hash_encode[1] == 'base16 or base32':
                if hash_string[-6:] == '======':
                    hash_encode = (hash_encode[0], 'base32')
                else:
                    hash_encode = (hash_encode[0], 'base16')
        if (hash_encode is None) and (hashfilename is not None):
            extension = os.path.splitext(hashfilename)[1][1:].strip().lower()
            if extension in self.hashfcts:
                # assume file extension gives the hash type
                # the coding is really hard to detect, therefore assume base16
                # RFC 3548 defines the following alphabets:
                # base64: ABCDEFGHIJKLMNOPQRSTUVWXYZ
                #         abcdefghijklmnopqrstuvwxyz0123456789-_
                # base32: abcdefghijklmnopqrstuvwxyz234567
                # base16: 0123456789ABCDEF
                # Unfortunately typical used tools like *sum (e. g. md5sum)
                # gives the output as base16 in lower letters.
                hash_encode = (extension, 'base16')
        return hash_encode

    def _analyse_hashline_of_file(self, sres, hashfilename):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-03-02 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        Analyse line of a hash file describing hash of complete file.
        This method should not be called from outside.

        :param sres: re instance
        :param hashfilename: file name of the hash
                             (normaly only path is used, if hash is not unique
                             the file extension is used)
        """
        hash_encode = self._determine_hash_encode(sres.group('hash'),
                                                  hashfilename)
        if hash_encode is not None:
            relfilename = os.path.normpath(
                os.path.join(
                    os.path.dirname(hashfilename),
                    sres.group('filename')))
            if hash_encode[1] == 'base64':
                hash_string = sres.group('hash')
            else:
                hash_string = sres.group('hash').lower()
            if relfilename in self.hash_dict:
                self.hash_dict[relfilename] += [(
                    hash_string,
                    hash_encode,
                    hashfilename)]
            else:
                self.hash_dict[relfilename] = [(
                    hash_string,
                    hash_encode,
                    hashfilename)]

    def _analyse_hashline_of_file_bsd(self, sres, hashfilename):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-03-01 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        Analyse line of a hash file describing hash of complete file in
        BSD-style.
        This method should not be called from outside.

        :param sres: re instance
        :param hashfilename: file name of the hash (here only path is used)
        """
        relfilename = os.path.normpath(
            os.path.join(
                os.path.dirname(hashfilename),
                sres.group('filename')))
        if relfilename in self.hash_dict:
            self.hash_dict[relfilename] += [(
                sres.group('hash').lower(),
                (sres.group('type').lower(), 'base16'),
                hashfilename)]
        else:
            self.hash_dict[relfilename] = [(
                sres.group('hash').lower(),
                (sres.group('type').lower(), 'base16'),
                hashfilename)]

    def _read_hash_file(self):
        """
        :Author: Daniel Mohr
        :Email: daniel.mohr@dlr.de
        :Date: 2017-02-25, 2021-02-17 (last change).
        :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

        read hash file
        """
        if (os.path.isfile(self.hash_file_name) and
                os.access(self.hash_file_name, os.R_OK)):
            self.log.debug("read hash file \"%s\"", self.hash_file_name)
            with open(self.hash_file_name, 'r', newline=None) as hash_file:
                for line in hash_file:
                    sres = self.regexps[0].search(line)
                    if sres:  # hash of a chunk
                        # this is ignored here
                        self.log.info("ignoring chunk hashes")
                    else:
                        sres = self.regexps[1].search(line)
                        if sres:  # hash of a complete file
                            self._analyse_hashline_of_file(
                                sres, self.hash_file_name)
                        else:
                            sres = self.regexps[2].search(line)
                            if sres:  # hash of a complete file (BSD-style)
                                self._analyse_hashline_of_file_bsd(
                                    sres, self.hash_file_name)
                            else:
                                self.log.warning(
                                    "do not understand line in hash file "
                                    "\"%s\": %s", self.hash_file_name, line)
        elif not os.access(self.hash_file_name, os.R_OK):
            self.log.warning('hash file "%s" is not readable',
                             self.hash_file_name)
        else:
            self.log.warning('hash file "%s" not existing (anymore?)',
                             self.hash_file_name)
