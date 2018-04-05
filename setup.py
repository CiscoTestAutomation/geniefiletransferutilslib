#! /bin/env python

"""Setup file for filetransferutils package

See:
    https://packaging.python.org/en/latest/distributing.html
"""

import os
import re
import sys
import shlex
import unittest
import subprocess

from setuptools import setup, find_packages, Command
from setuptools.command.test import test

from ats.utils.fileutils import ENTRYPOINT_GROUP

pkg_name = 'filetransferutils'

class CleanCommand(Command):
    '''Custom clean command

    cleanup current directory:
        - removes build/
        - removes src/*.egg-info
        - removes *.pyc and __pycache__ recursively

    Example
    -------
        python setup.py clean

    '''

    user_options = []
    description = 'CISCO SHARED : Clean all build artifacts'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('rm -vrf ./build ./dist ./src/*.egg-info')
        os.system('find . -type f -name "*.pyc" | xargs rm -vrf')
        os.system('find . -type d -name "__pycache__" | xargs rm -vrf')

class TestCommand(Command):
    user_options = []
    description = 'CISCO SHARED : Run unit tests against this package'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # where the tests are (relative to here)
        tests = os.path.join('src', pkg_name, 'tests')

        # call unittests
        sys.exit(unittest.main(
            module = None,
           argv = ['python -m unittest', 'discover', tests],
           failfast = True))


class BuildAndPreviewDocsCommand(Command):
    user_options = []
    description = 'CISCO SHARED : Build and privately distribute ' \
        'Sphinx documentation for this package'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        user = os.environ['USER']
        sphinx_build_cmd = "sphinx-build -b html -c ./docs " \
            "-d ./__build__/documentation/doctrees docs/ ./__build__/documentation/html"
        target_dir = "/users/{user}/WWW/cisco_shared/{pkg_name}".\
            format(user = user, pkg_name = pkg_name)
        mkdir_cmd = "mkdir -p {target_dir}".format(target_dir=target_dir)
        rsync_cmd = "rsync -rvc ./__build__/documentation/ {target_dir}".\
            format(target_dir=target_dir)
        try:
            ret_code = subprocess.call(shlex.split(mkdir_cmd))
            if not ret_code:
                ret_code = subprocess.call(shlex.split(sphinx_build_cmd))
                if not ret_code:
                    ret_code = subprocess.call(shlex.split(rsync_cmd))
                    print("\nYou may preview the documentation at the following URL:")
                    print("http://wwwin-home.cisco.com/~{user}/cisco_shared/{pkg_name}/html".\
                        format(user=user, pkg_name=pkg_name))
                    sys.exit(0)
            sys.exit(1)
        except Exception as e:
            print("Failed to build documentation : {}".format(str(e)))
            sys.exit(1)


def read(*paths):
    '''read and return txt content of file'''
    with open(os.path.join(os.path.dirname(__file__), *paths)) as fp:
        return fp.read()


def find_version(*paths):
    '''reads a file and returns the defined __version__ value'''
    version_match = re.search(r"^__version__ ?= ?['\"]([^'\"]*)['\"]",
                              read(*paths), re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

core_ver = '3.0.0'
version_range = '>= %s.0.0, < %s.0.0' % (core_ver[0], int(core_ver[0]) + 1)

# launch setup
setup(
    name = pkg_name,
    version = find_version('src', pkg_name, '__init__.py'),

    # descriptions
    description =  'containing utility functions for a tftp server',
    long_description = read('DESCRIPTION.rst'),

    # the package's documentation page.
    url = 'http://wwwin-pyats.cisco.com/cisco-shared/html/{}/docs/index.html'.\
        format(pkg_name),

    # author details
    author = 'Wei Chen',
    author_email = 'weiche3@cisco.com',
    maintainer_email =  'weiche3@cisco.com',

    # project licensing
    license = 'Cisco Systems, Inc. Cisco Confidential',

    platforms =  ['CEL',],

    # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry'
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Testing',
    ],

    # project keywords
    keywords = 'genie cisco-shared filetransferutils',

    # project packages
    packages = find_packages(where = 'src'),

    # project directory
    package_dir = {
        '': 'src',
    },

    # additional package data files that goes into the package itself
    package_data = {'':['README.rst']},

    # Standalone scripts
    scripts = [
    ],

    # console entry point
    entry_points = {
        ENTRYPOINT_GROUP : [
            'iosxe = filetransferutils.plugins.iosxe',
            'nxos = filetransferutils.plugins.nxos',
            'iosxr = filetransferutils.plugins.iosxr',
        ],
    },

    # package dependencies
    install_requires =  ['ats.utils >= 4.1.0'],

    # any additional groups of dependencies.
    # install using: $ pip install -e .[dev]
    extras_require = {
        'dev': ['coverage',
                'restview',
                'Sphinx',
                'sphinxcontrib-napoleon',
                'sphinxcontrib-mockautodoc',
                'sphinx-rtd-theme'],
    },

    # any data files placed outside this package.
    # See: http://docs.python.org/3.4/distutils/setupscript.html
    # format:
    #   [('target', ['list', 'of', 'files'])]
    # where target is sys.prefix/<target>
    data_files = [],

    # custom commands for setup.py
    cmdclass = {
        'clean': CleanCommand,
        'test': TestCommand,
        'docs': BuildAndPreviewDocsCommand,
    },

    # non zip-safe (never tested it)
    zip_safe = False,
)
