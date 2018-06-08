Introduction
============

The ``GenieFileTransferUtilsLibs`` package is a plugin derived implementation of the
:multiprotocolutilities:`Multiprotocol File Transfer <http>` core utilities.

The package provides various device agnostic APIs for supporting file transfer
(image, core, etc.) operation using different protocols such as tftp, ftp, etc.

.. _package_installation:


Installation
============

``GenieFileTransferUtilsLibs`` is installed with pip install within a sourced pyATS virtual environment.

.. code-block:: bash

    pip install genie.libs.filetransferutils

.. note::

    Make sure to source the env.sh(bash)/env.csh(C shell) to setup the `pyATS` env.
    For more information about pyATS installation please check the
    :pyats:`pyATS <http>` documentation.

Once installed the ``GenieFileTransferUtilsLibs`` package can be imported using `import` 

.. code-block:: python

    # GenieFileTransferUtilsLibs
    from genie.libs import filetransferutils


Support
=======

Reach out to :mailto:`contact us <cisco.com>` for any questions or issues related to the
``genie.metaparser`` package.

You can also post questions to the :communityforum:`community forum <http>` - the support team patrols
these forums daily.


Example 
=======

Import the ``FileUtils`` core utilities package then instanciate the file utils
device implementation corresponding to the device OS as illustrated below. 

.. code-block:: python

    # Import FileUtils core utilities
    from ats.utils.fileutils import FileUtils

    # Instanciate a filetransferutils instance for the device corresponding
    # to the device specific OS
    fu_device = FileUtils.from_device(device)

.. note::

    Check documentation for more information about Multiprotocol_File_Transfer_Utilities_ package.

Now the API can be called for various operations such as: 

* Copy file to/from device

    .. code-block:: python

        fu_device.copyfile(source='URL to copy from',
                           destination='URL to copy to',
                           timeout_seconds='timeout in seconds',
                           device='<device object>')

        Example:
        -------
        fu_device.copyfile(source='flash:/memleak.tcl',
            destination='ftp://1.1.1.1//auto/tftp-ssr/memleak.tcl',
            timeout_seconds=300, device=self.device)

* List all the files/folders under the specified directory

    .. code-block:: python

        directory_output = fu_device.dir(target='directory name',
                                         timeout_seconds='timeout in seconds',
                                         device='<device object>')

        Example:
        -------
        directory_output = fu_device.dir(target='flash:',
            timeout_seconds=300, device=self.device)

* Retrieve file details on a device directory

    .. code-block:: python

        file_details = fu_device.stat(target='file URL path',
                                      timeout_seconds='timeout in seconds',
                                      device='<device object>')

        Example:
        -------
        # Call the stat function
        file_details = fu_device.stat(target='flash:/memleak.tcl',
            timeout_seconds=300, device=self.device)

        # Retrieve the file details
        self.assertEqual(file_details['last_modified_date'],
            'Mar 20 2018 10:26:01 +00:00')
        self.assertEqual(file_details['permissions'], '-rw-')
        self.assertEqual(file_details['index'], '69705')
        self.assertEqual(file_details['size'], '104260')


* Delete file from device directory

    .. code-block:: python

        fu_device.deletefile(target='file URL path',
                             timeout_seconds='timeout in seconds',
                             device='<device object>')

        Example:
        -------
        # Call the deletefile function
        fu_device.deletefile(target='flash:/memleak.tcl',
            timeout_seconds=300, device=self.device)

* Rename file on device directory

    .. code-block:: python

        fu_device.renamefile(source='file URL path',
                             destination='file new name',
                             timeout_seconds='timeout in seconds',
                             device='<device object>')

        Example:
        -------
        # Call the renamefile function
        fu_device.renamefile(source='flash:/memleak.tcl',
            destination='new_file.tcl',
            timeout_seconds=300, device=self.device)

* Validate connectivity to remote server

    * Method will copy the output of 'show clock' command to a remote server to ensure
      sane connectivity to the server and then deletes the temporary created file.

    .. code-block:: python

        fu_device.validateserver(target='file URL path on the remote server',
                                 timeout_seconds='timeout in seconds',
                                 device='<device object>')

        Example:
        -------
        # Call the validateserver function
        fu_device.validateserver(
            target='ftp://1.1.1.1//auto/tftp-ssr/show_clock',
            timeout_seconds=300, device=self.device)

* Copy configuration to/from device

    .. code-block:: python

        # copy file from server to device running configuration
        fu_device.copyconfiguration(source='file URL path',
                             destination='running-config',
                             timeout_seconds='timeout in seconds',
                             device='<device object>')

        # copy device running configuration to startup-configuration
        fu_device.copyconfiguration(source='running-config',
                             destination='startup-config',
                             timeout_seconds='timeout in seconds',
                             device='<device object>')

        Example:
        -------
        # copy file from server to device running configuration
        fu_device.copyconfiguration(
            source='ftp://1.1.1.1//auto/tftp-ssr/config.py',
            destination='running-config',
            timeout_seconds='300', device=device)
