walk-through pydabu
===================

your data
---------

Your data is nothing more than a data bubble, until it is:

  * described
  * shared
  * published

pydabu can help you to describe your data. Think of a simple kind of a
basic data management plan (cf. [wikipedia:DMP]_; [RDA_DMP]_),
which is good research practice (cf. [DFG]_; [Helmholtz]_).

Like your data itself, a description of your data can be shared.
For example if in-house a search platform (e. g. [Solr]_) is running, you
could share your description of your data and enable your colleagues to find
your data.

During publication you will most probably need a description of your data
in terms of metadata.

.. only:: html

  References:
  ___________

.. [wikipedia:DMP] https://en.wikipedia.org/wiki/Data_management_plan
.. [RDA_DMP] Miksa, Tomasz and Walk, Paul and Neish, Peter;
	     RDA DMP Common Standard for Machine-actionable
	     Data Management Plans
	     https://doi.org/10.15497/rda00039
.. [DFG] Deutsche Forschungsgemeinschaft;
	 Guidelines for Safeguarding Good Research Practice. Code of Conduct
	 https://doi.org/10.5281/zenodo.3923602
.. [Helmholtz] Good scientific practice
	       https://www.helmholtz.de/en/about-us/the-association/good-scientific-practice/
.. [Solr] https://lucene.apache.org/solr/

creating a data bubble
----------------------

First of all you have to collect all data belonging to you data bubble in a
directory. Use you preferred way to copy/move your data. The directory could
look like::

  $ cd pydabu && ls -1a
  doc/
  .git
  gpl.txt
  install2home
  INSTALL.txt
  LICENSE.txt
  manual_pydabu.pdf
  PKG-INFO
  tests/
  README.md
  setup.py
  src/

Or storing big data it could look like::

  $ cd foo && ls -1
  glow_XIMAS1848000_001.zip
  glow_XIMAS1848000_2020-08-05_00003_140552145659648.img
  glow_XIMAS1848000.log
  graphics/
  info.txt
  overview_XOMAS1848000_001.zip
  overview_XOMAS1848000_2020-08-05_00004_140603729520384.img
  overview_XOMAS1848000.log
  pytwanrc_doc.pdf
  result.pdf
  result.rst
  signals.pdf
  twanrc_rf_trigger_AK06FZRP.log

Now let us create some description with :option:`pydabu create_data_bubble`::

  pydabu create_data_bubble -dir .

Two files ".dabu.json" and ".dabu.schema" are created as a draft for you.
In ".dabu.schema" the json schema describes the structured data stored
in the json instance ".dabu.json".

The schema describes not only the type of some data, but also required
metadata. You can yourself adapt it to your needs. Or you supervisor can
describe his requirement there.

The instance describes your data and holds some simple format check results.
You have to fill this draft with additional information and you should
check it.

With every text editor you can look at the generated files.
We will use a viewer::

  firefox .dabu.json

checking and fixing a data bubble
---------------------------------

You can check if your json instance is valid regarding the schema
(e. g. for "pydabu" (from above) you will not get any output)::

  jsonschema -i .dabu.json .dabu.schema
  pydabu check_data_bubble -dir .

At the moment the command :option:`pydabu check_data_bubble` gives
an overview of errors/warnings. Mainly you will see missing properties,
which are required.

For example for the data in the directory "foo" (from above), you will get::

  $ jsonschema -i .dabu.json .dabu.schema
  u'data integrity control' is a required property

Since, at this point we did not edit ".dabu.json" manually it is easy to fix.
Use [pfu]_ to create some checksums (if you have a few GB or more, this could
take a while) and recreate the data bubble::

  $ pfu.py create_checksum -dir . -store single
  $ rm .dabu.json .dabu.schema
  $ pydabu create_data_bubble -dir .
  $ jsonschema -i .dabu.json .dabu.schema
  ...
  u'license' is a required property

Instead of pfu you can also use your preferred checksumming tool.

Now you have to add a license, e. g. write a file "LICENSE.txt"::

  $ rm .checksum.sha512 .dabu.json .dabu.schema
  $ vim LICENSE.txt
  $ pfu.py create_checksum -directory . -store single
  $ pydabu create_data_bubble -dir .
  $ jsonschema -i .dabu.json .dabu.schema

And all necessary (depends on ".dabu.schema") metadata is collected in
".dabu.json".

.. only:: html

  References:
  ___________

.. [pfu] pfu -- Python File Utilities, https://gitlab.dlr.de/pfu/pfu
