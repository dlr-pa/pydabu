"""
:mod:`dabu.schema_org_data`
===========================
.. moduleauthor:: Daniel Mohr
.. contents::

functions
---------
.. currentmodule:: dabu.schema_org_data
.. autofunction:: get_schema_org_data
.. autofunction:: json_schema_from_schema_org

copyright + license
===================
Author: Daniel Mohr

Date: 2021-03-19 (last change).

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

from .json_schema_from_schema_org import json_schema_from_schema_org
from .get_schema_org_data import get_schema_org_data
from .add_property import combine
