#! /bin/env python

'''Setup file for Libs

See:
    https://packaging.python.org/en/latest/distributing.html
'''

from pyats.utils.fileutils.core.plugin_manager import ENTRYPOINT_GROUP

from ciscodistutils import setup, find_packages, is_devnet_build
from ciscodistutils.tools import (read,
                                  version_info,
                                  generate_cython_modules)

from ciscodistutils.common import (AUTHOR,
                                   URL,
                                   CLASSIFIERS,
                                   PYATS_PKG,
                                   SUPPORT,
                                   LICENSE,
                                   STD_EXTRA_REQ)

# compute version range
version, version_range = version_info('src', 'genie', 'libs', 'filetransferutils', '__init__.py')

# generate package dependencies
install_requires=['unicon']

entry_points = {
    ENTRYPOINT_GROUP : [
        'ios = genie.libs.filetransferutils.plugins.ios',
        'iosxe = genie.libs.filetransferutils.plugins.iosxe',
        'nxos = genie.libs.filetransferutils.plugins.nxos',
        'iosxr = genie.libs.filetransferutils.plugins.iosxr',
        'junos = genie.libs.filetransferutils.plugins.junos',
    ],
}

# launch setup
setup(
    name = 'genie.libs.filetransferutils',
    version = version,

    # descriptions
    description = 'Genie libs FileTransferUtils: Genie FileTransferUtils Libraries',
    long_description = read('DESCRIPTION.rst'),

    # the project's main homepage.
    url = URL,

    # author details
    author = AUTHOR,
    author_email = SUPPORT,

    # project licensing
    license = LICENSE,

    # see https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers = CLASSIFIERS,

    # project keywords
    keywords = 'genie pyats test automation',

    # uses namespace package
    namespace_packages = ['genie', 'genie.libs'],

    # project packages
    packages = find_packages(where = 'src'),

    # project directory
    package_dir = {
        '': 'src',
    },

    # additional package data files that goes into the package itself
    package_data = {
    },

    # console entry point
    entry_points = entry_points,

    # package dependencies
    install_requires = install_requires,

    # any additional groups of dependencies.
    # install using: $ pip install -e .[dev]
    extras_require = {
        'dev': ['coverage',
                'restview',
                'Sphinx',
                'sphinx-rtd-theme'],
    },

    # external modules
    ext_modules = [],

    # any data files placed outside this package.
    # See: http://docs.python.org/3.4/distutils/setupscript.html
    # format:
    #   [('target', ['list', 'of', 'files'])]
    # where target is sys.prefix/<target>
    data_files = [],

    # non zip-safe (never tested it)
    zip_safe = False,
)
