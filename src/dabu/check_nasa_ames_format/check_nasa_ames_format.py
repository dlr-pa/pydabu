"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-08 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import datetime
import re
import time


def date_rdate2isoformat(data):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-08 (last change).
    """
    splited = data.split()
    return datetime.date(int(splited[0]),
                         int(splited[1]),
                         int(splited[2])).isoformat()


def check_nasa_ames_format(filename, output_format='human_readable'):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-08 (last change).

    Checks the given file for the nasa ames format, see:

      * http://cedadocs.ceda.ac.uk/73/
      * http://cedadocs.ceda.ac.uk/73/4/index.html
      * http://cedadocs.ceda.ac.uk/73/4/FFI-summary.html

    :param filename: file to analyse
    """
    # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    result = dict()
    checker_name = 'pydabu (nasa ames format check)'
    addresult = dict()
    result[checker_name] = dict()
    result[checker_name]['error'] = 0
    result[checker_name]['warning'] = 0
    result[checker_name]['log'] = []
    metadata_part = []
    with open(filename, mode='r') as fd:
        # pylint: disable=unused-variable
        for i in range(7):
            metadata_part += [fd.readline()]
    if len(metadata_part) == 7:
        nlhead_ffi = metadata_part[0].strip().split()
        if isinstance(nlhead_ffi, list) and len(nlhead_ffi) == 2:
            # NLHEAD: Number of lines in file header
            # FFI: File format index
            addresult['NLHEAD'], addresult['FFI'] = map(int, nlhead_ffi)
        else:
            result[checker_name]['log'] += [
                'error: '
                'no nasa ames format detected (cannot analyse first line)']
            result[checker_name]['error'] += 1
        if result[checker_name]['error'] == 0:
            if bool(metadata_part[5]):  # len(metadata_part[5]) > 0
                ivol_nvol = metadata_part[5].strip().split()
                if isinstance(ivol_nvol, list) and len(ivol_nvol) == 2:
                    # IVOL: Number of the file in the above dataset
                    #       (between 1 and NVOL).
                    # NVOL: Total number of files belonging to the considered
                    #       dataset (i.e. with same ONAME, ORG, SNAME, MNAME).
                    ivol, nvol = map(int, ivol_nvol)
                    # if ((nvol >= 1) and (ivol >= 1) and (ivol <= nvol)):
                    if ((ivol >= 1) and (ivol <= nvol)):
                        addresult['IVOL'] = ivol
                        addresult['NVOL'] = nvol
                    else:
                        result[checker_name]['log'] += [
                            'error: do not understand IVOL and NVOL']
                        result[checker_name]['error'] += 1
                else:
                    result[checker_name]['log'] += [
                        'error: cannot extract IVOL and NVOL']
                    result[checker_name]['error'] += 1
            else:
                result[checker_name]['log'] += [
                    'error: IVOL and NVOL not found']
                result[checker_name]['error'] += 1
        if result[checker_name]['error'] == 0:
            if bool(metadata_part[1]):  # len(metadata_part[1]) > 0
                if len(metadata_part[1]) < 132 + 1:
                    # ONAME: List of author(s) in the format Lastname,
                    #        Firstname; separated by an arbitrary character
                    #        (for example, a hyphen or a semi-colon).
                    # since it is hard to automatic split at an arbitrary
                    # character, we only check for a comma
                    if ',' in metadata_part[1]:
                        addresult['ONAME'] = metadata_part[1].strip()
                    else:
                        result[checker_name]['log'] += [
                            'warning: do not understand ONAME format']
                        result[checker_name]['warning'] += 1
                else:
                    result[checker_name]['log'] += [
                        'warning: ONAME too long']
                    result[checker_name]['warning'] += 1
            else:
                result[checker_name]['log'] += [
                    'warning: ONAME is empty']
                result[checker_name]['warning'] += 1
            for (pos, tag) in [(2, 'ORG'), (3, 'SNAME'), (4, 'MNAME')]:
                # ORG: Organisation name (university, institute, etc).
                #      May include address and phone numbers.
                # SNAME: Source of data, i.e. instrument, platform, model name,
                #        etc.
                # MNAME: Name of mission, campaign, programme and/or project.
                # NVOL: Total number of files belonging to the considered
                #       dataset (i.e. with same ONAME, ORG, SNAME, MNAME).
                if bool(metadata_part[pos]):  # len(metadata_part[pos]) > 0
                    if len(metadata_part[pos]) < 132 + 1:
                        addresult[tag] = metadata_part[pos].strip()
                    else:
                        result[checker_name]['log'] += [
                            'warning: ' + tag + ' too long']
                        result[checker_name]['warning'] += 1
            if bool(metadata_part[6]):  # len(metadata_part[6]) > 0
                date_rdate = re.findall(
                    r'([0-9]{4}[ ]{1,2}[0-9]{1,2}[ ]{1,2}[0-9]{1,2})',
                    metadata_part[6].strip())
                if len(date_rdate) > 2:
                    result[checker_name]['log'] += [
                        'warning: too many "dates" in DATE RDATE']
                    result[checker_name]['warning'] += 1
                elif len(date_rdate) == 1:
                    addresult['DATE'] = date_rdate2isoformat(date_rdate[0])
                elif len(date_rdate) == 2:
                    date_rdate = re.findall(
                        r'([0-9]{4}[ ]{1,2}[0-9]{1,2}[ ]{1,2}[0-9]{1,2})'
                        r'\s*'
                        r'([0-9]{4}[ ]{1,2}[0-9]{1,2}[ ]{1,2}[0-9]{1,2})',
                        metadata_part[6].strip())
                    if date_rdate:
                        addresult['DATE'] = date_rdate2isoformat(
                            date_rdate[0][0])
                        addresult['RDATE'] = date_rdate2isoformat(
                            date_rdate[0][1])
                    else:
                        result[checker_name]['log'] += [
                            'warning: do not understand DATE RDATE']
                        result[checker_name]['warning'] += 1
                else:
                    result[checker_name]['log'] += [
                        'warning: do not understand DATE RDATE']
                    result[checker_name]['warning'] += 1
    result[checker_name]['created'] = time.time()
    if output_format != 'human_readable':
        for key in addresult:
            result[checker_name][key] = addresult[key]
    return result
