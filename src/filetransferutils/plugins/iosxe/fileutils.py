""" File utils base class for XE devices. """

# Parent inheritance
from .. import FileUtils as FileUtilsDeviceBase

# filemode_to_mode
from ats.utils.fileutils.plugins.linux.ftp.fileutils import filemode_to_mode

# Dir parser
from parser.iosxe.show_platform import Dir


class FileUtils(FileUtilsDeviceBase):

    def copyfile(self, from_file_url, to_file_url, timeout_seconds=300,
        vrf=None, *args, **kwargs):
        """ Copy a file to/from IOSXE device

        Copy any file to/from a device to any location supported on the
        device and on the running-configuration.

        Args:
        -----
            from_file_url: `str`
                Full path to the copy 'from' location
            to_file_url: `str`
                Full path to the copy 'to' location
            timeout_seconds: `str`
                The number of seconds to wait before aborting the operation
            vrf: `str`
                Vrf to be used during copy operation

        Returns:
        --------
            `None`

        Raises
        ------
        Exception
            When a device object is not present or device execution encountered
            an unexpected behavior.

        Examples:
        ---------
            # FileUtils
            >>> from ats.utils.fileutils import FileUtils

            # Instanciate a filetransferutils instance for IOSXE device
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
        """

        # copy flash:/memleak.tcl ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl
        if vrf:
            cmd = 'copy {f} {t} vrf {vrf_value}'.format(f=from_file_url,
                t=to_file_url, vrf_value=vrf)
        else:
            cmd = 'copy {f} {t}'.format(f=from_file_url, t=to_file_url)

        # Extract the server address to be used later for authentication
        new_list = [from_file_url, to_file_url]
        for item in new_list:
            parsed = self.parse_url(item)
            if parsed.netloc:
                used_server = parsed.netloc
                break
            else:
                continue

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

        Examples:
        ---------
            # FileUtils
            >>> from ats.utils.fileutils import FileUtils

            # Instanciate a filetransferutils instance for IOSXE device
            >>> fu_device = FileUtils.from_device(device)

            # list all files on the device directory 'flash:'
            >>> directory_output = fu_device.dir(from_directory_url='flash:',
            ...     timeout_seconds=300, device=device)

            >>> directory_output['dir']['flash:/']['files']

            EX:
            ---
                (Pdb) directory_output['dir']['flash:/']['files']['boothelper.log']
                {'index': '69699', 'permissions': '-rw-', 'size': '76',
                 'last_modified_date': 'Mar 20 2018 10:25:46 +00:00'}

        """


        dir_output = super().dir(from_directory_url, timeout_seconds, Dir,
            *args, **kwargs)

        # Extract the files location requested
        output = self.parse_url(from_directory_url)

        # Construct the directory name
        directory = output.scheme + ":/"

        return dir_output['dir'][directory]['files']

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

        Examples:
        ---------
            # FileUtils
            >>> from ats.utils.fileutils import FileUtils

            # Instanciate a filetransferutils instance for IOSXE device
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

        files = super().stat(file_url, timeout_seconds, *args, **kwargs)

        # Extract the file name requested
        output = self.parse_url(file_url)
        file_details = files[output.path]

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
            When a device object is not present or device execution encountered
            an unexpected behavior.

        Examples:
        ---------
            # FileUtils
            >>> from ats.utils.fileutils import FileUtils

            # Instanciate a filetransferutils instance for IOSXE device
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
            When a device object is not present or device execution encountered
            an unexpected behavior.

        Examples:
        ---------
            # FileUtils
            >>> from ats.utils.fileutils import FileUtils

            # Instanciate a filetransferutils instance for IOSXE device
            >>> fu_device = FileUtils.from_device(device)

            # rename the file on the device 'flash:' directory
            >>> fu_device.renamefile(file_url='flash:memleak.tcl',
            ...     to_file_url='memleak_backup.tcl'
            ...     timeout_seconds=300, device=device)

        """
        # rename bootflash:memleak.tcl memleak_j.tcl
        cmd = 'rename {f} {u}'.format(f=from_file_url, u=to_file_url)

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

    def validateserver(self, to_directory_url, timeout_seconds=300, *args,
        **kwargs):
        ''' Make sure that the given server information is valid


        Function that verifies if the server information given is valid, and if
        the device can connect to it. It does this by saving `show clock`
        output to a particular file using transfer protocol. Then deletes the
        file.

        Args:
            cmd (`str`):  Command to be executed on the device 
            to_directory_url (`str`):  File path including the protocol, server and 
                file location.
            timeout_seconds: `str`
                The number of seconds to wait before aborting the operation.

        Returns:
            `None`

        Raises:
            Exception: If the command from the device to server is unreachable
                or the protocol used doesn't support remote checks.

        Examples:
            # FileUtils
            >>> from ats.utils.fileutils import FileUtils

            # Instanciate a filetransferutils instance for NXOS device
            >>> fu_device = FileUtils.from_device(device)

            # Validate server connectivity
            >>> fu_device.validateserver(
            ...     to_directory_url='ftp://10.1.6.242//auto/tftp-ssr/show_clock',
            ...     timeout_seconds=300, device=device)
        '''

        # Patch up the command together
        # show clock | redirect ftp://10.1.6.242//auto/tftp-ssr/show_clock
        cli = "show clock | redirect {e}".format(e=to_directory_url)

        import pdb; pdb.set_trace()
        self.parse_url(to_directory_url)
        super().validateserver(cli, timeout_seconds, to_directory_url, *args,
            **kwargs)
