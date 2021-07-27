"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-19 (last change).
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""


def _includes_dict(analyse_object, content):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-26
    """
    return bool(("@id" in analyse_object) and
                (analyse_object["@id"] == content))


def _includes_list(analyse_object, content):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-26
    """
    ret = False
    for element in analyse_object:
        ret = _includes_dict(element, content)
        if ret:
            break
    return ret


def _includes(analyse_object, content):
    """
    :Author: Daniel Mohr
    :Date: 2021-02-26
    """
    if isinstance(analyse_object, dict):
        return _includes_dict(analyse_object, content)
    elif isinstance(analyse_object, list):
        return _includes_list(analyse_object, content)
    # else:
    return False


def ispending(analyse_object):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09

    We ignore work-in-progress terms marked as pending:
    https://schema.org/docs/howwework.html#pending
    """
    if "schema:isPartOf" in analyse_object:
        return _includes(analyse_object["schema:isPartOf"],
                         "https://pending.schema.org")
    return False
