"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-18
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

tests the script json_schema_from_schema_org

You can run this file directly:

env python3 script_json_schema_from_schema_org.py

Or you can run only one test, e. g.:

env python3 script_json_schema_from_schema_org.py \
  script_json_schema_from_schema_org.test_dummy_1
"""

import json
import os.path
import tempfile
import unittest

import jsonschema


class ScriptJsonSchemaFromSchemaOrg(unittest.TestCase):
    """
    :Author: Daniel Mohr
    :Date: 2021-03-18
    """

    # pylint: disable=no-self-use
    def test_dummy_1(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-10

        This test calls json_schema_from_schema_org dummy
        """
        import subprocess
        cpi = subprocess.run(
            "json_schema_from_schema_org dummy",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        schema = json.loads(cpi.stdout)
        instance = dict()
        jsonschema.validate(instance, schema)

    def test_dummy_2(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-05

        This test calls json_schema_from_schema_org dummy
        """
        import subprocess
        cpi = subprocess.run(
            "json_schema_from_schema_org -cachefilename '' dummy",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        schema = json.loads(cpi.stdout)
        instance = dict()
        jsonschema.validate(instance, schema)
        with tempfile.TemporaryDirectory() as tmpdir:
            cpi = subprocess.run(
                "json_schema_from_schema_org -cachefilename " +
                os.path.join(tmpdir, 'foo') + " dummy",
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                shell=True, timeout=3, check=True)
            schema = json.loads(cpi.stdout)
            jsonschema.validate(instance, schema)

    def test_person_1(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-18

        This test calls json_schema_from_schema_org Person
        """
        import subprocess
        cpi = subprocess.run(
            "json_schema_from_schema_org Person",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        schema = json.loads(cpi.stdout)
        instance = dict()
        instance["$schema"] = "http://json-schema.org/draft-04/schema#"
        instance["type"] = "object"
        instance["@context"] = dict()
        for key in ["Person", "Place", "Thing"]:
            instance["@context"][key] = "https://schema.org/" + key
        with self.assertRaises(jsonschema.exceptions.ValidationError):
            jsonschema.validate(instance, schema)
        for key in [
                "Photograph",
                "Demand",
                "ItemList",
                "VirtualLocation",
                "Offer",
                "CreativeWork",
                "AudioObject",
                "Event",
                "ContactPoint",
                "Person",
                "CorrectionComment",
                "CivicStructure",
                "PriceSpecification",
                "ImageObject",
                "MonetaryAmount",
                "MediaObject",
                "Country",
                "Intangible",
                "Place",
                "Language",
                "AdministrativeArea",
                "StructuredValue",
                "InteractionCounter",
                "Brand",
                "DefinedTerm",
                "EducationalOrganization",
                "Organization",
                "Comment",
                "ProgramMembership",
                "QuantitativeValue",
                "Occupation",
                "Distance",
                "Product",
                "Quantity",
                "PropertyValue",
                "OwnershipInfo",
                "Thing",
                "OfferCatalog"
        ]:
            instance["@context"][key] = "https://schema.org/" + key
        jsonschema.validate(instance, schema)

    def test_person_2(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-03-10

        This test calls json_schema_from_schema_org Person
        """
        import subprocess
        import dabu.compare_json_schemas
        cp1 = subprocess.run(
            "json_schema_from_schema_org Person",
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=True, timeout=3, check=True)
        cp2 = subprocess.run(
            "json_schema_from_schema_org dummy Person",
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
