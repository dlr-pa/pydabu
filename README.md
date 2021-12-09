# README: pydabu -- Python Data Bubble

## intro

'pydabu' is an acronym for Python Data Bubble.

Your data is nothing more than a data bubble, until it is:

* described
* shared
* published

pydabu can help you to describe your data.

You can find more information on the web:

* [source code of pydabu](https://gitlab.com/dlr-pa/pydabu)
* documentation of pydabu is linked there

## install

See [INSTALL.txt](doc/source/INSTALL.txt) or
[INSTALL: pydabu (web)](https://dlr-pa.github.io/pydabu/INSTALL.html) for full
install manual. You can find a very short overview in the next lines.

pydabu needs some Python modules and you can also ask the installation
routine/script for the required Python modules:

    env python3 setup.py --help
    env python3 setup.py --requires

To install this software global to / the following step is to perform:

    env python3 setup.py install --record installed_files.txt

To install this software to your $HOME the following steps are to perform:

    env python3 setup.py install --home=~ --record installed_files.txt

You can also use pip to install:

    pip3 install .

For older versions of pip you need to choose explicit a home install:

    pip3 install --user .

## copyright + license

Author: Daniel Mohr.

Date: 2021-06-24 (last change).

License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007

Copyright (C) 2021 Daniel Mohr and
Deutsches Zentrum fuer Luft- und Raumfahrt e. V., D-51170 Koeln

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License as
 published by the Free Software Foundation; either version 3 of
 the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 General Public License for more details.

 You should have received a copy (see [LICENSE.txt](LICENSE.txt)) of the
 GNU General Public License along with this program.
 If not, see <http://www.gnu.org/licenses/>.

### Contact Informations

* Daniel Mohr, daniel.mohr@dlr.de

### Territory

This license applies to all components/files of the software.
