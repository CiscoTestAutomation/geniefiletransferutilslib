""" File utils base class for NXOS devices. """

# Parent inheritance
from .. import FileUtils as FileUtilsDeviceBase

# filemode_to_mode
from ats.utils.fileutils.plugins.linux.ftp.fileutils import filemode_to_mode

# Dir parser
try:
    from parser.nxos.show_platform import Dir
except ImportError:
    try:
        from genie_parser.nxos.show_platform import Dir
    except ImportError:
        # For apidoc building only
        from unittest.mock import Mock; Dir=Mock()


class FileUtils(FileUtilsDeviceBase):

    def copyfile(self, from_file_url, to_file_url, timeout_seconds=300,
                 vrf=None, local=False, *args, **kwargs):
        """ Copy a file to/from NXOS device

        Copy any file to/from a device to any location supported on the
        device and on the running-configuration.

        Parameters
        ----------
            from_file_url: `str`
                Full path to the copy 'from' location
            to_file_url: `str`
                Full path to the copy 'to' location
            timeout_seconds: `str`
                The number of seconds to wait before aborting the operation
            vrf: `str`
                Vrf to be used during copy operation
            local: bool
                Flag to determine if copy destination is local to the device
                Example (bootflash/running-config/startup-config etc.)

        Returns
        -------
            `None`

        Raises
        ------
            Exception
                When a device object is not present or device execution
                encountered an unexpected behavior.

        Examples
        --------
            # FileUtils
            >>> from ats.utils.fileutils import FileUtils

            # Instantiate a filetransferutils instance for NXOS device
            >>> from ats.utils.fileutils import FileUtils
            >>> fu_device = FileUtils.from_device(device)

            # copy file from device to server
            >>> fu_device.copyfile(
            ...     from_file_url='flash:/memleak.tcl',
            ...     to_file_url='ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl',
            ...     timeout_seconds='300', device=device)

            # copy file from server to device
            >>> fu_device.copyfile(
            ...     from_file_url='ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl',
            ...     to_file_url='flash:/new_file.tcl',
            ...     timeout_seconds='300', device=device)

            # copy file from server to device running configuration
            >>> fu_device.copyfile(
            ...     from_file_url='ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl',
            ...     to_file_url='running-config',
            ...     timeout_seconds='300', device=device)

            # copy running-configuration to device memory
            >>> fu_device.copyfile(
            ...     from_file_url='running-configuration',
            ...     to_file_url='bootflash:filename',
            ...     timeout_seconds='300', device=device)

            # copy startup-configuration running-configuration
            >>> fu_device.copyfile(
            ...     from_file_url='startup-configuration',
            ...     to_file_url='running-configuration',
            ...     timeout_seconds='300', device=device)w
        """

        if local:
            # Server is not involved
            used_server = None

            # Build copy command
            # Example - copy running-configuration bootflash:tempfile1
            cmd = 'copy {f} {t}'.format(f=from_file_url, t=to_file_url)

        else:
            # Extract the server address to be used later for authentication
            used_server = self.get_server(from_file_url, to_file_url)

            # copy flash:/memleak.tcl ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl vrf management
            cmd = 'copy {f} {t} vrf {vrf}'.format(f=from_file_url, t=to_file_url,
                vrf=vrf)

        super().copyfile(from_file_url=from_file_url, to_file_url=to_file_url,
            timeout_seconds=timeout_seconds, cmd=cmd, used_server=used_server,
            *args, **kwargs)

    def dir(self, from_directory_url, timeout_seconds=300, *args, **kwargs):
        """ Retrieve filenames contained in a directory.

        Do not recurse into subdirectories, only list files at the top level
        of the given directory.

        Parameters
        ----------
            file_url : `str`
                The URL of the file whose details are to be retrieved.

            timeout_seconds : `int`
                The number of seconds to wait before aborting the operation.

        Returns
        -------
            `dict` : Dict of filename URLs and the corresponding info (ex:size)

        Raises
        ------
            AttributeError
                device object not passed in the function call

            Exception
                Parser encountered an issue

        Examples
        --------
            # FileUtils
            >>> from ats.utils.fileutils import FileUtils

            # Instanciate a filetransferutils instance for NXOS device
            >>> fu_device = FileUtils.from_device(device)

            # list all files on the device directory 'bootflash:'
            >>> directory_output = fu_device.dir(from_directory_url='bootflash:',
            ...     timeout_seconds=300, device=device)

            >>> directory_output

            ['bootflash:/virt_strg_pool_bf_vdc_1/',
             'bootflash:/platform-sdk.cmd', 'bootflash:/.swtam/',
             'bootflash:/virtual-instance/', 'bootflash:/nxos.7.0.3.I7.1.bin',
             'bootflash:/virtual-instance.conf', 'bootflash:/scripts/',
             'bootflash:/memleak.tcl', 'bootflash:/acfg_base_running_cfg_vdc1',
             'bootflash:/.rpmstore/']

        """

        dir_output = super().parsed_dir(from_directory_url, timeout_seconds,
            Dir, *args, **kwargs)

        # Extract the files location requested
        output = self.parse_url(from_directory_url)

        # Construct the directory name
        directory = output.scheme + ":/"

        # Create a new list to return
        new_list = []

        for key in dir_output['files']:
            new_list.append(directory+key)

        return new_list

    def stat(self, file_url, timeout_seconds=300, *args, **kwargs):
        """ Retrieve file details such as length and permissions.

        Parameters
        ----------
            file_url : `str`
                The URL of the file whose details are to be retrieved.

            timeout_seconds : `int`
                The number of seconds to wait before aborting the operation.

        Returns
        -------
            `file_details` : File details including size, permissions, index
                and last modified date.

        Raises
        ------
            AttributeError
                device object not passed in the function call

            Exception
                Parser encountered an issue

        Examples
        --------
            # FileUtils
            >>> from ats.utils.fileutils import FileUtils

            # Instanciate a filetransferutils instance for NXOS device
            >>> fu_device = FileUtils.from_device(device)

            # list the file details on the device 'flash:' directory
            >>> directory_output = fu_device.stat(file_url='flash:memleak.tcl',
            ...     timeout_seconds=300, device=device)

            >>> directory_output['size']
            >>> directory_output['permissions']

            EX:
            ---
                (Pdb) directory_output
                {'last_modified_date': 'Mar 20 2018 10:26:01 +00:00',
                 'size': '104260', 'permissions': '-rw-', 'index': '69705'}

        """

        files = super().stat(file_url, timeout_seconds, Dir, *args, **kwargs)

        # Extract the file name requested
        output = self.parse_url(file_url)
        file_details = files['files'][output.path]

        return file_details

    def deletefile(self, file_url, timeout_seconds=300, *args, **kwargs):
        """ Delete a file

        Parameters
        ----------
            file_url : `str`
                The URL of the file whose details are to be retrieved.

            timeout_seconds : `int`
                The number of seconds to wait before aborting the operation.

        Returns
        -------
            None

        Raises
        ------
            Exception
                When a device object is not present or device execution
                encountered an unexpected behavior.

        Examples
        --------
            # FileUtils
            >>> from ats.utils.fileutils import FileUtils

            # Instanciate a filetransferutils instance for NXOS device
            >>> fu_device = FileUtils.from_device(device)

            # delete a specific file on device directory 'flash:'
            >>> directory_output = fu_device.deletefile(
            ...     file_url='flash:memleak_bckp.tcl',
            ...     timeout_seconds=300, device=device)

        """

        super().deletefile(file_url, timeout_seconds, *args, **kwargs)

    def renamefile(self, from_file_url, to_file_url, timeout_seconds=300, *args,
        **kwargs):
        """ Rename a file

        Parameters
        ----------
            from_file_url : `str`
                The URL of the file to be renamed.

            to_file_url : `str`
                The URL of the new file name.

            timeout_seconds : `int`
                Maximum allowed amount of time for the operation.

        Returns
        -------
            None

        Raises
        ------
            Exception
                When a device object is not present or device execution
                encountered an unexpected behavior.

        Examples
        --------
            # FileUtils
            >>> from ats.utils.fileutils import FileUtils

            # Instanciate a filetransferutils instance for NXOS device
            >>> fu_device = FileUtils.from_device(device)

            # rename the file on the device 'bootflash:' directory
            >>> fu_device.renamefile(file_url='bootflash:memleak.tcl',
            ...     to_file_url='memleak_backup.tcl'
            ...     timeout_seconds=300, device=device)

        """
        # move bootflash:memleak.tcl memleak_j.tcl
        cmd = 'move {f} {u}'.format(f=from_file_url, u=to_file_url)

        super().renamefile(from_file_url, to_file_url, timeout_seconds, cmd, 
            *args, **kwargs)

    def chmod(self, file_url, mode, timeout_seconds=300, *args, **kwargs):
        """ Change file permissions

        Parameters
        ----------
            file_url : `str`
                The URL of the file whose permissions are to be changed.

            mode : `int`
                Same format as `os.chmod`.

            timeout_seconds : `int`
                Maximum allowed amount of time for the operation.

        Returns
        -------
            `None` if operation succeeded.

        """

        raise NotImplementedError("The fileutils module {} "
            "does not implement chmod.".format(self.__module__))

    def validateserver(self, to_directory_url, timeout_seconds=300,
        vrf='management', *args, **kwargs):
        ''' Make sure that the given server information is valid


        Function that verifies if the server information given is valid, and if
        the device can connect to it. It does this by saving `show clock`
        output to a particular file using transfer protocol. Then deletes the
        file.

        Parameters
        ----------
            cmd (`str`):  Command to be executed on the device 
            to_directory_url (`str`):  File path including the protocol,
                server and file location.
            timeout_seconds (`str`):
                The number of seconds to wait before aborting the operation.
            vrf (`str`):
                Vrf value to be used during execution. Default is `management`

        Returns
        -------
            `None`

        Raises
        ------
            Exception: If the command from the device to server is unreachable
                or the protocol used doesn't support remote checks.

        Examples
        --------
            # FileUtils
            >>> from ats.utils.fileutils import FileUtils

            # Instanciate a filetransferutils instance for NXOS device
            >>> fu_device = FileUtils.from_device(device)

            # Validate server connectivity
            >>> fu_device.validateserver(
            ...     to_directory_url='ftp://10.1.7.250//auto/tftp-ssr/show_clock',
            ...     timeout_seconds=300, device=device)
        '''

        # Patch up the command together
        # show clock > tftp://10.1.0.213//auto/ftp-ssr/show_clock vrf management
        cli = "show clock > {e} vrf {vrf}".format(e=to_directory_url, vrf=vrf)

        super().validateserver(cli, timeout_seconds, to_directory_url, *args,
            **kwargs)