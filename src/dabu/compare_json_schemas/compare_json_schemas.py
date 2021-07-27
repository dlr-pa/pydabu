"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-10
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""


def dict_equal(a, b):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09
    """
    for key in a.keys():
        if key not in b:
            return False
        elif isinstance(a[key], dict):
            if not dict_equal(a[key], b[key]):
                return False
        elif isinstance(a[key], list):
            if len(a[key]) != len(b[key]):
                return False
            for i in range(len(a[key])):
                if any_element_equal_list(a[key][i], b[key]):
                    pass
                else:
                    return False
        else:
            if not a[key] == b[key]:
                return False
    return True


def equal_list_as_set(a, b):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-10

    return True if for every element in a if it is also available in b
    """
    if not len(a) == len(b):
        return False
    for i in range(len(a)):
        # is any element in b equal to i?
        if any_element_equal_list(a[i], b):
            pass
        else:
            return False
    return True


def any_element_equal_list(e, l):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-10

    checks if any element of l is in e
    """
    for i in range(len(l)):
        if isinstance(l[i], dict):
            if isinstance(e, dict) and dict_equal(e, l[i]):
                return True
        elif isinstance(l[i], list):
            if isinstance(e, list) and equal_list_as_set(e, l[i]):
                return True
        elif isinstance(e, dict) or isinstance(e, list):
            pass
        elif e == l[i]:
            return True
    return False


def compare_list_as_set(a, b, comparefct):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-10

    checks for every element in a if it is also available in b
    """
    comparefct(type(a), type(b))
    comparefct(len(a), len(b))
    for i in range(len(a)):
        # is any element in b equal to i?
        if any_element_equal_list(a[i], b):
            pass
        else:
            raise comparefct(0, 1)


def compare_dict(a, b, comparefct):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09
    """
    comparefct(set(a.keys()), set(b.keys()))
    for key in a.keys():
        if isinstance(a[key], dict):
            compare_dict(a[key], b[key], comparefct)
        elif isinstance(a[key], list):
            compare_list_as_set(a[key], b[key], comparefct)
        else:
            comparefct(a[key], b[key])


def assertEqual(a, b):
    assert(a == b)


def compare_json_schemas_one_way(a, b, comparefct=assertEqual):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09

    This function compares the json schemas a with b and checks if a
    is in b.

    :param a: json schema to compare
    :param b: json schema to compare
    :param comparefct: compare function to use;
                       e. g. self.assertEqual in unittests
    """
    if isinstance(a, dict) and isinstance(b, dict):
        compare_dict(a, b, comparefct)
    elif isinstance(a, list) and isinstance(b, list):
        compare_list_as_set(a, b, comparefct)
    else:
        comparefct(a, b)


def compare_json_schemas(a, b, comparefct=assertEqual):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-10

    This function compares the two json schemas a and b.

    :param a: json schema to compare
    :param b: json schema to compare
    :param comparefct: compare function to use;
                       e. g. self.assertEqual in unittests
    """
    compare_json_schemas_one_way(a, b, comparefct=comparefct)
    compare_json_schemas_one_way(b, a, comparefct=comparefct)