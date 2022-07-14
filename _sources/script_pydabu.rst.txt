.. index::
   single: pydabu
   single: script; pydabu
   single: command line script; pydabu

command line script: :program:`pydabu`
======================================

:program:`pydabu` has a few subcommands:

.. option:: analyse_data_structure

   Analyse the data stucture of a directory tree.

.. option:: check_nasa_ames_format

   This command checks a file in the nasa ames format.

.. option:: check_netcdf_file

   This command checks a file in the format netCDF.
   It uses the CF Checker: https://github.com/cedadev/cf-checker

.. option:: check_file_format

   This command checks the file formats in a directory tree.

.. option:: common_json_format

   This command read the given json file and writes it in a common format to
   stdout.

.. option:: create_data_bubble

   This command creates a data bubble in the give directory.

.. option:: check_data_bubble

   This command checks a data bubble in the given directory.

.. option:: listschemas

   This command lists the provided and used json schemas.

.. option:: data_bubble2jsonld

   This command reads the data bubble (.dabu.json and .dabu.schema) and
   creates a json-ld data bubble (.dabu.json-ld and .dabu.json-ld.schema).

These commands are explained in more detail in the following (help output):

.. argparse::
   :module: dabu.scripts.pydabu.pydabu_main
   :func: my_argument_parser
   :prog: pydabu

   analyse_data_structure : @before
       see also: :ref:`analyse_data_structure_output.schema`

   check_file_format : @before
       see also: :ref:`dabu.schema`

   create_data_bubble : @before
       see also: :ref:`dabu.schema` and :ref:`dabu_requires.schema`

   listschemas : @before
       see also: :ref:`Provided and used json schemas`
