"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-07-30
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import distutils  # we need distutils for distutils.errors.DistutilsArgError
import os
import sys

from setuptools import Command, setup


class TestWithPytest(Command):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-07-30
    :License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.

    running automatic tests with pytest
    """
    description = "running automatic tests with pytest"
    user_options = [
        ('src=',
         None,
         'Choose what should be tested; installed: ' +
         'test installed package and scripts (default); ' +
         'local: test package direct from sources ' +
         '(installing is not necessary). ' +
         'The command line scripts are not tested for local. ' +
         'default: installed'),
        ('coverage', None, 'use pytest-cov to generate a coverage report'),
        ('pylint', None, 'if given, run pylint'),
        ('pytestverbose', None, 'increase verbosity of pytest'),
        ('parallel', None, 'run tests in parallel')]

    def initialize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-18
        """
        # pylint: disable=attribute-defined-outside-init
        self.src = 'installed'
        self.coverage = False
        self.pylint = False
        self.pytestverbose = False
        self.parallel = False

    def finalize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """

    def run(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-07-30
        """
        # pylint: disable=too-many-branches
        if self.src == 'installed':
            pass
        elif self.src == 'local':
            sys.path.insert(0, os.path.abspath('src'))
        else:
            raise distutils.core.DistutilsArgError(
                "error in command line: " +
                "value for option 'src' is not 'installed' or 'local'")
        sys.path.append(os.path.abspath('.'))
        # https://docs.pytest.org/en/stable/contents.html
        # https://pytest-cov.readthedocs.io/en/latest/
        # pylint: disable=bad-option-value,import-outside-toplevel
        import pytest
        pyargs = []
        if self.parallel:
            try:
                # if available, using parallel test run
                # pylint: disable=unused-variable,unused-import
                import xdist
                if os.name == 'posix':
                    # since we are only running seconds,
                    # we use the load of the last minute:
                    nthreads = int(os.cpu_count() - os.getloadavg()[0])
                    # since we have only a few tests, limit overhead:
                    nthreads = min(4, nthreads)
                    nthreads = max(2, nthreads)  # at least two threads
                else:
                    nthreads = max(2, int(0.5 * os.cpu_count()))
                pyargs += ['-n %i' % nthreads]
            except (ModuleNotFoundError, ImportError):
                pass
        if self.coverage:
            coverage_dir = 'coverage_report/'
            # first we need to clean the target directory
            if os.path.isdir(coverage_dir):
                files = os.listdir(coverage_dir)
                for filename in files:
                    os.remove(os.path.join(coverage_dir, filename))
            pyargs += ['--cov=dabu', '--no-cov-on-fail',
                       '--cov-report=html:' + coverage_dir,
                       '--cov-report=term:skip-covered']
        if self.pylint:
            pyargs += ['--pylint']
        if self.pytestverbose:
            pyargs += ['--verbose']
        if self.src == 'installed':
            pyargs += ['pydabu_unittests/main.py']
        pyargs += ['pydabu_unittests/package_data.py']
        pyargs += [
            'pydabu_unittests/dabu_scripts_pydabu_check_arg_file_not_exists.py'
        ]
        pyargs += ['pydabu_unittests/compare_json_schemas.py']
        pyargs += ['pydabu_unittests/schema_org_data.py']
        if self.src == 'installed':
            pyargs += ['pydabu_unittests/script_pydabu.py']
            pyargs += \
                ['pydabu_unittests/script_json_schema_from_schema_org.py']
        pyplugins = []
        print('call: pytest', ' '.join(pyargs))
        sys.exit(pytest.main(pyargs, pyplugins))


class TestWithUnittest(Command):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-03-05
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
         'The command line scripts are not tested for local. ' +
         'default: installed')]

    def initialize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """
        # pylint: disable=attribute-defined-outside-init
        self.src = 'installed'

    def finalize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-02-04
        """

    def run(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-06-21
        """
        if self.src == 'installed':
            pass
        elif self.src == 'local':
            sys.path.insert(0, os.path.abspath('src'))
        else:
            raise distutils.core.DistutilsArgError(
                "error in command line: " +
                "value for option 'src' is not 'installed' or 'local'")
        sys.path.append(os.path.abspath('.'))
        # pylint: disable=bad-option-value,import-outside-toplevel
        import unittest
        suite = unittest.TestSuite()
        import pydabu_unittests
        pydabu_unittests.module(suite)
        setup_self = self

        class TestRequiredModuleImport(unittest.TestCase):
            # pylint: disable=missing-docstring
            # pylint: disable=no-self-use
            def test_required_module_import(self):
                import importlib
                for module in setup_self.distribution.metadata.get_requires():
                    importlib.import_module(module)
        loader = unittest.defaultTestLoader
        suite.addTest(loader.loadTestsFromTestCase(
            TestRequiredModuleImport))
        if self.src == 'installed':
            pydabu_unittests.scripts(suite)
        if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():
            sys.exit(0)
        else:
            sys.exit(1)
        res = unittest.TextTestRunner(verbosity=2).run(suite)
        if res.wasSuccessful():
            sys.exit(0)
        else:
            sys.exit(1)


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
        """
        :Author: Daniel Mohr
        :Date: 2017-01-08
        """

    def finalize_options(self):
        """
        :Author: Daniel Mohr
        :Date: 2017-01-08
        """

    def run(self):
        """
        :Author: Daniel Mohr
        :Date: 2017-01-08
        """
        # pylint: disable=bad-option-value,import-outside-toplevel
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


# necessary modules
REQUIRED_MODULES = ['argparse',
                    'base64',
                    'datetime',
                    'distutils',
                    'getpass',
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
                    'types',
                    'warnings']
# optional modules
REQUIRED_MODULES += ['cfchecker.cfchecks', 'netCDF4']
# optional modules to return version from module read from package metadata
REQUIRED_MODULES += ['pkg_resources']
# optional modules for python3 setup.py check_modules
REQUIRED_MODULES += ['importlib']
# optional modules for json_schema_from_schema_org
# REQUIRED_MODULES += ['bz2', 'gzip', 'lzma', 'ssl', 'urllib.request']
# modules to build doc
# REQUIRED_MODULES += ['sphinx', 'sphinxarg', 'recommonmark']
# modules to run tests with unittest
# REQUIRED_MODULES += ['unittest', 'shutil']
# modules to run tests with pytest
# REQUIRED_MODULES += ['pytest']
# optional modules to run tests with pytest in parallel
# REQUIRED_MODULES += ['xdist']
# optional modules to run tests with pytest and create coverage report
# REQUIRED_MODULES += ['pytest_cov']

setup(
    name='pydabu',
    version='2021.07.29',
    cmdclass={
        'check_modules': CheckModules,
        'run_unittest': TestWithUnittest,
        'run_pytest': TestWithPytest},
    description='software to check a data bubble.',
    long_description='',
    keywords=['data managment', 'metadata', 'data management plan'],
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
        'dabu.compare_json_schemas',
        'dabu.analyse_file_format',
        'dabu.schema_org_data',
        'dabu.scripts',
        'dabu.scripts.pydabu',
        'dabu.scripts.json_schema_from_schema_org'],
    entry_points={
        'console_scripts':
            ['pydabu=dabu.scripts.pydabu.pydabu_main:pydabu_main',
             'json_schema_from_schema_org='
             'dabu.scripts.json_schema_from_schema_org.'
             'json_schema_from_schema_org_main:'
             'json_schema_from_schema_org_main'],
    },
    package_data={'dabu': ['schemas/analyse_data_structure_output.schema',
                           'schemas/dabu.schema',
                           'schemas/dabu_requires.schema']},
    license='GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: BSD :: OpenBSD',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Archiving'],
    # cat $(find | grep "py$") | egrep -i "^[ \t]*import .*$" | \
    #   egrep -i --only-matching "import .*$" | sort -u
    requires=REQUIRED_MODULES,
    provides=['dabu']
)
