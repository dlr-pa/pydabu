Provided and used json schemas
==============================

The script :program:`pydabu` uses json schemas which are displayed in the
next sections. You can find the schemas in the directory of the python module
:mod:`dabu`, e. g.::

  $ python3 -c "import dabu,os;print(os.path.join(dabu.__path__[0], 'schemas'))"
  /home/mohr/lib/python/dabu/schemas

Or you can ask :option:`pydabu listschemas`, e. g.::

  $ pydabu listschemas
  /home/mohr/lib/python/dabu/schemas/dabu.schema
  /home/mohr/lib/python/dabu/schemas/dabu_requires.schema
  /home/mohr/lib/python/dabu/schemas/analyse_data_structure_output.schema


analyse_data_structure_output.schema
------------------------------------

The command :option:`pydabu analyse_data_structure` leeds to an output
holding the following json schema:

  .. jsonschema:: ../../src/dabu/schemas/analyse_data_structure_output.schema

dabu.schema
-----------

The command :option:`pydabu check_file_format` leeds to an output
holding the following json schema. The output file :file:`.dabu.json` of
:option:`pydabu create_data_bubble` holds also this json schema:

  .. jsonschema:: ../../src/dabu/schemas/dabu.schema

dabu_requires.schema
--------------------

The following json schema is used in :option:`pydabu create_data_bubble`
as :file:`.dabu.schema` (bold attributes are required):

  .. jsonschema:: ../../src/dabu/schemas/dabu_requires.schema
