"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-19
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests schema_org_data from the module dabu


You can run this file directly:

env python3 schema_org_data.py

Or you can run only one test, e. g.:

env python3 schema_org_data.py schema_org_data.test_add_property
"""

import unittest


class schema_org_data_add_property(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-19
    """

    def test_add_property(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-19
        """
        import dabu.compare_json_schemas
        from dabu.schema_org_data.add_property import add_property
        a = dict()
        b = dict()
        add_property(a, "foo", "bar")
        b["foo"] = "bar"
        dabu.compare_json_schemas.compare_json_schemas(a, b)
        add_property(a, "dict", {'k': 'v'})
        add_property(a, "dict", {'k2': 'v2'})
        b["dict"] = {'k': 'v', 'k2': 'v2'}
        with self.assertRaises(TypeError):
            add_property(a, "dict", ['k2', 'v2'])
        with self.assertRaises(TypeError):
            add_property(a, "dict", 'k2:v2')
        dabu.compare_json_schemas.compare_json_schemas(a, b)
        add_property(a, "list", [1, 2])
        b["list"] = [1, 2]
        with self.assertRaises(TypeError):
            add_property(a, "list", {1: 2})
        add_property(a, "list", [3, 4])
        b["list"] += [3, 4]
        add_property(a, "list", '5')
        b["list"] += ['5']
        add_property(a, "list", 3)
        dabu.compare_json_schemas.compare_json_schemas(a, b)
        add_property(a, "foo", "baz")
        b["foo"] = ["bar", "baz"]
        dabu.compare_json_schemas.compare_json_schemas(a, b)
        add_property(a, "bar", "baz")
        b["bar"] = "baz"
        add_property(a, "bar", {'foo': 3})
        b["bar"] = ["baz", {'foo': 3}]
        dabu.compare_json_schemas.compare_json_schemas(a, b)
        add_property(a, "baz", "baz")
        b["baz"] = "baz"
        add_property(a, "baz", ['bar', 'foo'])
        b["baz"] = ["baz", "bar", 'foo']
        dabu.compare_json_schemas.compare_json_schemas(a, b)


if __name__ == '__main__':
    unittest.main(verbosity=2)
