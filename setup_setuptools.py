"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-03-05
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

#from distutils.core import setup, Command
from setuptools import setup, Command


class TestWithUnittest(Command):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-04
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    running automatic tests with unittest
    """
    description = "running automatic tests with unittest"
    user_options = [
        ("src=",
         None,
         'Choose what should be tested; installed: ' +
         'test installed package and scripts (default); ' +
         'local: test package direct from sources ' +
         '(installing is not necessary). ' +
         'The command line scripts are not testes for local. ' +
         'default: installed')]

    def initialize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        self.src = 'installed'

    def finalize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        pass

    def run(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        import sys
        import os.path
        if self.src == 'installed':
            pass
        elif self.src == 'local':
            sys.path.insert(0, os.path.abspath('src'))
        else:
            raise distutils.core.DistutilsArgError(
                "error in command line: " +
                "value for option 'src' is not 'installed' or 'local'")
        sys.path.append(os.path.abspath('.'))
        import unittest
        suite = unittest.TestSuite()
        import pydabu_unittests
        pydabu_unittests.module(suite)
        if self.src == 'installed':
            pydabu_unittests.scripts(suite)
        unittest.TextTestRunner(verbosity=2).run(suite)


class CheckModules(Command):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@gmx.de
    :Date: 2017-01-08
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    checking for modules need to run the software
    """
    description = "checking for modules need to run the software"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import importlib
        summary = ""
        i = 0
        print("checking for modules need to run the software (scripts and")
        print("modules/packages) of this package:\n")
        print("checking for the modules mentioned in the 'setup.py':")
        for module in self.distribution.metadata.get_requires():
            if self.verbose:
                print("try to load %s" % module)
            try:
                importlib.import_module(module)
                if self.verbose:
                    print("  loaded.")
            except ImportError:
                i += 1
                summary += "module '%s' is not available\n" % module
                print("module '%s' is not available <---WARNING---" % module)
        print(
            "\nSummary\n%d modules are not available (not unique)\n%s\n" % (
                i, summary))


class CheckModulesModulefinder(Command):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@gmx.de
    :Date: 2017-01-08
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    checking for modules need to run the scripts (modulefinder)
    """
    description = "checking for modules need to run the scripts (modulefinder)"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import modulefinder
        for script in self.distribution.scripts:
            print("\nchecking for modules used in '%s':" % script)
            finder = modulefinder.ModuleFinder()
            finder.run_script(script)
            finder.report()


# necessary modules
required_modules = ['argparse',
                    'base64',
                    'datetime',
                    'distutils',
                    'hashlib',
                    'json',
                    'jsonschema',
                    'logging',
                    'os',
                    'os.path',
                    'pkgutil',
                    're',
                    'subprocess',
                    'sys',
                    'tempfile',
                    'time',
                    'warnings']
install_requires = ['argparse>=1.1',
                    # 'base64', # not available by pypi.org
                    'datetime',
                    # 'distutils', # not available by pypi.org
                    # 'hashlib', # version from pypi.org does not work
                    # 'json', # not available by pypi.org
                    'jsonschema',
                    # 'logging', # version from pypi.org does not work
                    # 'os', # not available by pypi.org
                    # 'pkgutil', # not available by pypi.org
                    # 're', # not available by pypi.org
                    # 'subprocess', # version from pypi.org does not work
                    # 'sys', # version from pypi.org does not work
                    # 'tempfile', # version from pypi.org does not work
                    # 'time', # not available by pypi.org
                    ]
# optional modules
required_modules += ['cfchecker.cfchecks', 'netCDF4']
install_requires += ['cfchecker', 'netCDF4']
# optional modules to return version from module read from package metadata
required_modules += ['pkg_resources']
install_requires += ['pkg_resources']
# optional modules for python3 setup.py check_modules
required_modules += ['importlib']
#install_requires += ['importlib'] # version from pypi.org does not work
# optional modules for python3 setup.py check_modules_modulefinder
required_modules += ['modulefinder']
# install_requires += ['modulefinder'] # version from pypi.org does not work
# optional modules for json_schema_from_schema_org.py
required_modules += ['bz2', 'gzip', 'lzma', 'ssl', 'urllib.request']
# not available by pypi.org: bz2, gzip, lzma
# version from pypi.org does not work: ssl, urllib
# modules to build doc
required_modules += ['sphinx', 'sphinxarg', 'recommonmark']
# not available by pypi.org: sphinxarg
install_requires += ['sphinx', 'recommonmark']
# modules to run tests with unittest
required_modules += ['unittest']
# install_requires += ['unittest'] # not available by pypi.org
# modules to run tests with pytest
required_modules += ['pytest']
install_requires += ['pytest']
# optional modules to run tests with pytest in parallel
required_modules += ['xdist']
# install_requires += ['xdist'] # not available by pypi.org
# optional modules to run tests with pytest and create coverage report
required_modules += ['pytest_cov']
install_requires += ['pytest_cov']

setup(
    name='pydabu',
    version='2021-03-05',
    cmdclass={
        'check_modules': CheckModules,
        'check_modules_modulefinder': CheckModulesModulefinder,
        'run_unittests': TestWithUnittest},
    description='software to check a data bubble.',
    long_description='',
    keywords='data managment',
    author='Daniel Mohr',
    author_email='daniel.mohr@dlr.de',
    maintainer='Daniel Mohr',
    maintainer_email='daniel.mohr@dlr.de',
    url='',
    download_url='',
    package_dir={'': 'src'},
    packages=[
        'dabu',
        'dabu.analyse_data_structure',
        'dabu.check_nasa_ames_format',
        'dabu.check_netcdf_file',
        'dabu.analyse_file_format',
        'dabu.scripts'],
    scripts=[
        'src/scripts/pydabu.py'],
    package_data={'dabu': ['schemas/check_data_structure_output.schema',
                           'schemas/dabu.schema',
                           'schemas/dabu_requires.schema']},
    license='GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: BSD :: OpenBSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3'],
    # cat $(find | grep "py$") | egrep -i "^[ \t]*import .*$" | egrep -i --only-matching "import .*$" | sort -u
    requires=required_modules,
    install_requires=install_requires,  # this does not work:
    # using python, this does not use pip!
    # using python, these packages are installed even if it is already
    #               installed (e. g. system wide)
    # using pip, these packages are installed even if it is already
    #            installed (e. g. system wide)
    provides=['dabu']
)
