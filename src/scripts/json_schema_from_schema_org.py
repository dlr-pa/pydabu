#!/usr/bin/env python3
"""
Author: Daniel Mohr.
Date: 2021-03-04 (last change).
License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

./json_schema_from_schema_org.py Thing
./json_schema_from_schema_org.py Person

./json_schema_from_schema_org.py Thing > t.json
jsonschema t.json

./json_schema_from_schema_org.py Thing | tee t.json ; jsonschema t.json
"""

from dabu.scripts.json_schema_from_schema_org import \
    json_schema_from_schema_org_main


if __name__ == "__main__":
    json_schema_from_schema_org_main()
