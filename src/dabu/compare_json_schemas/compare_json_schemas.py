"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-10
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

# pylint: disable=invalid-name


def assertEqual(a, b):
    """
    a simple assert function
    """
    assert a == b


def dict_equal(a, b):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09
    """
    for key in a.keys():
        if key not in b:
            return False
        if isinstance(a[key], dict):
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

    return True if for every element in a it is also available in b
    """
    if not len(a) == len(b):
        return False
    for e in a:
        # is any element in b equal to e?
        if any_element_equal_list(e, b):
            pass
        else:
            return False
    return True


def any_element_equal_list(e, mylist):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-10

    checks if any element of mylist is in e
    """
    for el in mylist:
        if isinstance(el, dict):
            if isinstance(e, dict) and dict_equal(e, el):
                return True
        elif isinstance(el, list):
            if isinstance(e, list) and equal_list_as_set(e, el):
                return True
        elif isinstance(e, (dict, list)):
            pass
        elif e == el:
            return True
    return False


def compare_list_as_set(a, b, comparefct=assertEqual):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-10

    checks for every element in a if it is also available in b
    and if a and b have the same type and the same number of elements
    """
    comparefct(type(a), type(b))
    comparefct(len(a), len(b))
    for e in a:
        # is any element in b equal to e?
        if any_element_equal_list(e, b):
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
    # pylint: disable=bad-option-value,arguments-out-of-order
    compare_json_schemas_one_way(b, a, comparefct=comparefct)
