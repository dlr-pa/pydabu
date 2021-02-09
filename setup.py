"""
:Author: Daniel Mohr
:Email: daniel.mohr@dlr.de
:Date: 2021-02-09
:License: GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007.
"""

from distutils.core import setup, Command


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
                    'distutils',
                    'json',
                    'jsonschema',
                    'os',
                    'os.path',
                    'pkgutil',
                    're',
                    'subprocess',
                    'sys',
                    'tempfile',
                    'time',
                    'unittest']
# optional modules
required_modules += ['cfchecker.cfchecks', 'netCDF4']
# modules to build doc
required_modules += ['sphinx', 'sphinxarg', 'recommonmark']

setup(
    name='pydabu',
    version='2021-02-09',
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
    provides=['dabu']
)
