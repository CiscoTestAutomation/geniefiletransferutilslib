Introduction
============
 
The FileTransferUtils package (``FileTransferUtils``) provides various API for supporting file transfer (image, core, etc..) using different protocols such as tftp, ftp, etc..  

.. _package_installation:

Installation
============

``FileTransferUtils`` is installed with pip install within a sourced pyATS virtual environment.

.. code-block:: bash

    pip install filetransferutils

.. note::

    Make sure to source the env.sh to setup the `pyATS` env.

Once installed the FileTransferUtils package can be imported using `import' 

.. code-block:: python

    # FileTransferUtils
    import filetransferutils


Support 
========

pyATS Support Team is happy to help you with any question/enquiry through PieStack_ under the category of Cisco Shared Packages/FileTransferUtils. 

.. _PieStack: http://piestack.cisco.com



Example 
========

Setup the connection to remote server (in this case through SSH), instanciate the file transfer protocol object (in this example TFTP protocol). 

.. code-block:: python


    # Import FileTransferUtils pkg
    import filetransferutils

    # Import secure shell pkg 
    from filetransferutils.ssh import Ssh

    # setup the secure shell connection with the remove server 
    scp = Ssh(ip=server)
    scp.setup_scp()

    # Create an instance file transfer protocol object; in this case the TFTP 
    tftpobj = Lookup.from_device(device).filetransferutils.tftp.utils.Utils(
        scp, kwargs['destination'])

Now the API can be called for various operations such as: 

* copying file to device

    .. code-block:: python

        tftpobj.copy_file_to_device(device = '<device object>',
                                    filename = 'file full path',
                                    location = 'running-config')

* copying output of a CLI Command



    .. code-block:: python
        
        # Save a cli output to a file, which is then copied to server
        tftpobj.copy_CLI_output (device='<device object>', filename='file name on the server',
                                 cli='cli to be executed on device')

* copy_core

    .. code-block:: python

        tftpobj.copy_core(device='<device object>', location='core location on device',
                              core='core file name', vrf='vrf name (if needed)',
                              timeout='timeout for the core copy', username='username (if needed, ex: ftp)',
                              password='password (if needed, ex: ftp)')

* validate_server 

    .. code-block:: python

        tftpobj.validate_server(device='<device object>', vrf='vrf name (if needed)')
