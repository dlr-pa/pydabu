"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-09
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script json_schema_from_schema_org.py

You can run this file directly:

env python3 script_json_schema_from_schema_org.py

Or you can run only one test, e. g.:

env python3 script_json_schema_from_schema_org.py scripty_json_schema_from_schema_org.test_dummy
"""

import json
import jsonschema
import os.path
import tempfile
import unittest


def dict_equal(a, b):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09
    """
    for key in a.keys():
        if not key in b:
            return False
        elif isinstance(a[key], dict):
            if not dict_equal(a[key], b[key]):
                return False
        elif isinstance(a[key], list):
            if len(a[key]) != len(b[key]):
                return False
            for i in range(len(a[key])):
                if any_element_equal(a[key][i], b[key]):
                    pass
                else:
                    return False
        else:
            if not a[key] == b[key]:
                return False
    return True


def any_element_equal(e, l):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09
    """
    for i in range(len(l)):
        if isinstance(l[i], dict) and dict_equal(e, l[i]):
            return True
        elif isinstance(l[i], list) and any_element_equal(a, l[i]):
            return True
        elif e == l[i]:
            return True
    return False


def compare_list_as_set(a, b, comparefct):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09
    """
    comparefct(len(a), len(b))
    for i in range(len(a)):
        # is any element in b equal to i?
        if any_element_equal(a[i], b):
            pass
        else:
            raise foo


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


def compare_schemas(a, b, comparefct):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09
    """
    if isinstance(a, dict) and isinstance(b, dict):
        compare_dict(a, b, comparefct)
    elif isinstance(a, list) and isinstance(b, list):
        compare_list_as_set(a, b, comparefct)
    else:
        comparefct(a, b)


class scripty_json_schema_from_schema_org(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-09
    """

    def test_dummy_1(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-04

        This test calls json_schema_from_schema_org.py dummy
        """
        import subprocess
        cp = subprocess.run(
            ["json_schema_from_schema_org.py dummy"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        schema = json.loads(cp.stdout)
        instance = {"@context": {"dummy": "https://schema.org/dummy"}}
        jsonschema.validate(instance, schema)
        instance = {"$schema": "http://json-schema.org/draft-04/schema#",
                    "@context": {"dummy": "https://schema.org/dummy"},
                    "dummy": "foo"}
        jsonschema.validate(instance, schema)

    def test_dummy_2(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05

        This test calls json_schema_from_schema_org.py dummy
        """
        import subprocess
        cp = subprocess.run(
            ["json_schema_from_schema_org.py -cachefilename '' dummy"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        schema = json.loads(cp.stdout)
        instance = {"@context": {"dummy": "https://schema.org/dummy"}}
        jsonschema.validate(instance, schema)
        with tempfile.TemporaryDirectory() as tmpdir:
            cp = subprocess.run(
                ["json_schema_from_schema_org.py -cachefilename " +
                 os.path.join(tmpdir, 'foo') + " dummy"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=3, check=True)
            schema = json.loads(cp.stdout)
            instance = {"@context": {"dummy": "https://schema.org/dummy"}}
            jsonschema.validate(instance, schema)

    def test_person_1(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-04

        This test calls json_schema_from_schema_org.py Person
        """
        import subprocess
        cp = subprocess.run(
            ["json_schema_from_schema_org.py Person"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        schema = json.loads(cp.stdout)
        instance = dict()
        instance["$schema"] = "http://json-schema.org/draft-04/schema#"
        instance["type"] = "object"
        instance["@context"] = dict()
        for key in ["Person", "Place", "Thing"]:
            instance["@context"][key] = "https://schema.org/" + key
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(instance, schema)
        for key in ["ImageObject", "MediaObject", "CreativeWork", "Comment"]:
            instance["@context"][key] = "https://schema.org/" + key
        jsonschema.validate(instance, schema)

    def test_person_2(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-09

        This test calls json_schema_from_schema_org.py Person
        """
        import subprocess
        cp1 = subprocess.run(
            ["json_schema_from_schema_org.py Person"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        cp2 = subprocess.run(
            ["json_schema_from_schema_org.py dummy Person"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        schema1 = json.loads(cp1.stdout)
        schema2 = json.loads(cp2.stdout)
        # To compare the 2 schemas we assume all lists as sets.
        # This should be fine in most cases. But not in all cases!
        compare_schemas(schema1, schema2, self.assertEqual)


if __name__ == '__main__':
    unittest.main(verbosity=2)
