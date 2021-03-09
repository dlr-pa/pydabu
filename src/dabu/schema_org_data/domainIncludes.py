"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-09 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""


def _Includes_dict(object, content):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-26
    """
    if ("@id" in object) and (object["@id"] == content):
        return True
    else:
        return False


def _Includes_list(object, content):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-26
    """
    ret = False
    for element in object:
        ret = _Includes_dict(element, content)
        if ret:
            break
    return ret


def _Includes(object, content):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-26
    """
    if isinstance(object, dict):
        return _Includes_dict(object, content)
    elif isinstance(object, list):
        return _Includes_list(object, content)
    else:
        return False


def ispending(object):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09

    We ignore work-in-progress terms marked as pending:
    https://schema.org/docs/howwework.html#pending
    """
    if "schema:isPartOf" in object:
        return _Includes(object["schema:isPartOf"],
                         "https://pending.schema.org")
    return False


def domainIncludes(object, content):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09
    """
    if ("schema:domainIncludes" in object) and (not ispending(object)):
        return _Includes(object["schema:domainIncludes"], content)
    else:
        return False
