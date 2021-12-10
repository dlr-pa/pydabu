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


class SchemaOrgDataAddProperty(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-19
    """

    def test_add_property(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-19
        """
        # pylint: disable=bad-option-value,import-outside-toplevel
        import dabu.compare_json_schemas
        from dabu.schema_org_data.add_property import add_property
        adict = dict()
        bdict = dict()
        add_property(adict, "foo", "bar")
        bdict["foo"] = "bar"
        dabu.compare_json_schemas.compare_json_schemas(adict, bdict)
        add_property(adict, "dict", {'k': 'v'})
        add_property(adict, "dict", {'k2': 'v2'})
        bdict["dict"] = {'k': 'v', 'k2': 'v2'}
        with self.assertRaises(TypeError):
            add_property(adict, "dict", ['k2', 'v2'])
        with self.assertRaises(TypeError):
            add_property(adict, "dict", 'k2:v2')
        dabu.compare_json_schemas.compare_json_schemas(adict, bdict)
        add_property(adict, "list", [1, 2])
        bdict["list"] = [1, 2]
        with self.assertRaises(TypeError):
            add_property(adict, "list", {1: 2})
        add_property(adict, "list", [3, 4])
        bdict["list"] += [3, 4]
        add_property(adict, "list", '5')
        bdict["list"] += ['5']
        add_property(adict, "list", 3)
        dabu.compare_json_schemas.compare_json_schemas(adict, bdict)
        add_property(adict, "foo", "baz")
        bdict["foo"] = ["bar", "baz"]
        dabu.compare_json_schemas.compare_json_schemas(adict, bdict)
        add_property(adict, "bar", "baz")
        bdict["bar"] = "baz"
        add_property(adict, "bar", {'foo': 3})
        bdict["bar"] = ["baz", {'foo': 3}]
        dabu.compare_json_schemas.compare_json_schemas(adict, bdict)
        add_property(adict, "baz", "baz")
        bdict["baz"] = "baz"
        add_property(adict, "baz", ['bar', 'foo'])
        bdict["baz"] = ["baz", "bar", 'foo']
        dabu.compare_json_schemas.compare_json_schemas(adict, bdict)


if __name__ == '__main__':
    unittest.main(verbosity=2)
