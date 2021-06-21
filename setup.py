"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-06-21
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

import os

from distutils.core import setup, Command


class TestWithPytest(Command):
    """
    :Author: Daniel Mohr
    :Email: daniel.mohr@dlr.de
    :Date: 2021-02-19
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
        pass

    def run(self):
        """
        :Author: Daniel Mohr
        :Date: 2021-06-21
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
        # https://docs.pytest.org/en/stable/contents.html
        # https://pytest-cov.readthedocs.io/en/latest/
        import pytest
        pyargs = []
        if self.parallel:
            try:
                # if available, using parallel test run
                import xdist
                import sys
                if os.name == 'posix':
                    # since we are only running seconds,
                    # we use the load of the last minute:
                    nthreads = int(os.cpu_count() - os.getloadavg()[0])
                    # since we have only a few tests, limit overhead:
                    nthreads = min(4, nthreads)
                    nthreads = max(1, nthreads)  # at least one thread
                else:
                    nthreads = max(1, int(0.5 * os.cpu_count()))
                pyargs += ['-n %i' % nthreads]
            except:
                pass
        if self.coverage:
            coverage_dir = 'coverage_report/'
            # first we need to clean the target directory
            if os.path.isdir(coverage_dir):
                files = os.listdir(coverage_dir)
                for f in files:
                    os.remove(os.path.join(coverage_dir, f))
            pyargs += ['--cov=dabu', '--no-cov-on-fail',
                       '--cov-report=html:' + coverage_dir,
                       '--cov-report=term:skip-covered']
        if self.pylint:
            pyargs += ['--pylint']
        if self.pytestverbose:
            pyargs += ['--verbose']
        pyargs += ['pydabu_unittests/main.py']
        pyargs += ['pydabu_unittests/package_data.py']
        pyargs += [
            'pydabu_unittests/dabu_scripts_pydabu_check_arg_file_not_exists.py'
        ]
        pyargs += ['pydabu_unittests/compare_json_schemas.py']
        pyargs += ['pydabu_unittests/schema_org_data.py']
        if self.src == 'installed':
            pyargs += ['pydabu_unittests/script_pydabu.py']
            pyargs += ['pydabu_unittests/script_json_schema_from_schema_org.py']
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
        :Date: 2021-06-21
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
        setup_self = self

        class test_required_module_import(unittest.TestCase):
            def test_required_module_import(self):
                import importlib
                for module in setup_self.distribution.metadata.get_requires():
                    importlib.import_module(module)
        loader = unittest.defaultTestLoader
        suite.addTest(loader.loadTestsFromTestCase(
            test_required_module_import))
        if self.src == 'installed':
            pydabu_unittests.scripts(suite)
        if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful():
            sys.exit(0)
        else:
            sys.exit(1)
        a = unittest.TextTestRunner(verbosity=2).run(suite)
        print('\n########\n')
        print(type(a))
        print(a)
        if a.wasSuccessful():
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
                    'pwd',
                    're',
                    'subprocess',
                    'sys',
                    'tempfile',
                    'time',
                    'warnings']
# optional modules
required_modules += ['cfchecker.cfchecks', 'netCDF4']
# optional modules to return version from module read from package metadata
required_modules += ['pkg_resources']
# optional modules for python3 setup.py check_modules
required_modules += ['importlib']
# optional modules for python3 setup.py check_modules_modulefinder
required_modules += ['modulefinder']
# optional modules for json_schema_from_schema_org.py
required_modules += ['bz2', 'gzip', 'lzma', 'ssl', 'urllib.request']
# modules to build doc
required_modules += ['sphinx', 'sphinxarg', 'recommonmark']
# modules to run tests with unittest
required_modules += ['unittest', 'shutil']
# modules to run tests with pytest
required_modules += ['pytest']
# optional modules to run tests with pytest in parallel
required_modules += ['xdist']
# optional modules to run tests with pytest and create coverage report
required_modules += ['pytest_cov']

setup(
    name='pydabu',
    version='2021-06-21',
    cmdclass={
        'check_modules': CheckModules,
        'check_modules_modulefinder': CheckModulesModulefinder,
        'run_unittest': TestWithUnittest,
        'run_pytest': TestWithPytest},
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
        'dabu.compare_json_schemas',
        'dabu.analyse_file_format',
        'dabu.schema_org_data',
        'dabu.scripts',
        'dabu.scripts.pydabu',
        'dabu.scripts.json_schema_from_schema_org'],
    scripts=[
        'src/scripts/pydabu.py',
        'src/scripts/json_schema_from_schema_org.py'],
    package_data={'dabu': ['schemas/analyse_data_structure_output.schema',
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
    provides=['dabu']
)
