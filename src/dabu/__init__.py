"""pydabu -- python data bubble

.. contents::

description
===========
This is the description for the module dabu belonging to the project pydabu.

submodules
==========
.. automodule:: dabu.analyse_data_structure
.. automodule:: dabu.analyse_file_format
.. automodule:: dabu.check_nasa_ames_format
.. automodule:: dabu.check_netcdf_file
.. automodule:: dabu.compare_json_schemas
.. automodule:: dabu.schema_org_data
.. automodule:: dabu.scripts

copyright + license
===================
Author: Daniel Mohr

Date: 2021-03-10 (last change).

License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

Copyright (C) 2021 Daniel Mohr
 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License as
 published by the Free Software Foundation; either version 3 of
 the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, see
 http://www.gnu.org/licenses/
"""

try:
    # try to get version from package metadata
    import pkg_resources
    __version__ = pkg_resources.require('pydabu')[0].version
except Exception:
    pass
