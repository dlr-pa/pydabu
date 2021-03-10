"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-10
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


class scripty_json_schema_from_schema_org(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-10
    """

    def test_dummy_1(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-10

        This test calls json_schema_from_schema_org.py dummy
        """
        import subprocess
        cp = subprocess.run(
            ["json_schema_from_schema_org.py dummy"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        schema = json.loads(cp.stdout)
        instance = dict()
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
        instance = dict()
        jsonschema.validate(instance, schema)
        with tempfile.TemporaryDirectory() as tmpdir:
            cp = subprocess.run(
                ["json_schema_from_schema_org.py -cachefilename " +
                 os.path.join(tmpdir, 'foo') + " dummy"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=3, check=True)
            schema = json.loads(cp.stdout)
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
        :Date: 2021-03-10

        This test calls json_schema_from_schema_org.py Person
        """
        import subprocess
        import dabu.compare_json_schemas
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
        dabu.compare_json_schemas.compare_json_schemas(
            schema1, schema2, self.assertEqual)


if __name__ == '__main__':
    unittest.main(verbosity=2)
