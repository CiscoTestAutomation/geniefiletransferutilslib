Table of Contents
=================

    1. :ref:`introduction`
    2. :ref:`package_installation`
    3. :ref:`support_Mailers`
    4. :ref:`how_to`

The documentation is organized into following sections:

.. _introduction:

Introduction
============

This package covers different file transfer protocols. It
contains a utility functions for file transfer to/from remote servers. User can 
use the package to copy files, save crashreports and cores on a remote server 
for later use.

The same instance can be used by multiples devices, as each device is an
argument passed in all the methods.

.. _package_installation:

Package Installation
====================

User needs to create an empty directory and inside that new directory
the installation script can be called.

.. code-block:: text

    /auto/pyats/bin/pyats-install

.. note::

    ``--help`` can be used to check installation options

For more information about pyATS
`installation <http://wwwin-pyats.cisco.com/documentation/html/install/install.html>`_
please check the documentation.

``FileTransferUtils`` can be installed using the `pip` command. Assuming that you
have already sourced your virtualenv, run the following commands on the shell:

    pip install filetransferutils

.. _support_Mailers:

Support Mailers
===============

The `pyATS Support Team`_ is available to help you with any issues
related to the ``FileTransferUtils`` package.

Please consider creating a question under `PieStack`_.

You may also consider making use of one of the following mailers :
`pyATS Users`_.

.. _pyATS Support Team: pyats-support@cisco.com
.. _pyATS Users: pyats-users@cisco.com
.. _PieStack: http://piestack.cisco.com


.. _how_to:

How to use ``FileTransferUtils``?
=================================

Package can be imported anywhere under the pyats environment and be used as
illustrated below.

Supported utility functions with examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

First, user needs to setup server connection.

Setup server connection
```````````````````````

Before using ``FileTransferUtils``, we need to setup secure shell ``SSH``
connection with the remote server.

.. code-block:: python


    # FileTransferUtils
    import filetransferutils

    # Ssh
    from filetransferutils.ssh import Ssh

    # Got a file transfer prortocol, set it up
    # Get the information needed
    scp = Ssh(ip=server)
    scp.setup_scp()

    # Get the corresponding abstracted filetransfetrutils protocol implementation
    # Example using tftp:
    tftpcls = Lookup.from_device(device).filetransferutils.tftp.utils.Utils(
        scp, kwargs['destination'])

Now user is able to use the above cretaed server session to perform various
actions as shown below.

Functions
`````````

copy_file_to_device
-------------------

Copy any file to a device via Tftp/Ftp/Scp/etc. to any location supported on
the device.

    .. code-block:: python

        tftpcls.copy_file_to_device(device = '<device object>',
                                    filename = 'file full path',
                                    location = 'running-config')

save_output
-----------

Save a cli output to a file outside of the device via tftp.

    .. code-block:: python

        tftpcls.save_output(device='<device object>', filename='file name on the server',
                              cli='cli to be executed on device')

save_core
---------

Save a device generated core on the remote server.

    .. code-block:: python

        tftpcls.save_core(device='<device object>', location='core location on device',
                              core='core file name', vrf='vrf name (if needed)',
                              timeout='timeout for the core copy', username='username (if needed, ex: ftp)',
                              password='password (if needed, ex: ftp)')

basic_check
-----------

Make sure that the given tftp information is valid.

    .. code-block:: python

        tftpcls.basic_check(device='<device object>', vrf='vrf name (if needed)')
