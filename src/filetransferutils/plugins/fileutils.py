""" File utils common base class """
# Logging
import logging

# Parent inheritance
from .. import FileUtils as FileUtilsCommonDeviceBase

# Server FileUtils core implementation
from ats.utils.fileutils import FileUtils as server

# filemode_to_mode
from ats.utils.fileutils.plugins.linux.ftp.fileutils import filemode_to_mode

# Dir parser
from parser.nxos.show_platform import Dir

# Initialize the logger
logger = logging.getLogger(__name__)


class FileUtils(FileUtilsCommonDeviceBase):

    def copyfile(self, from_file_url, to_file_url, timeout_seconds, cmd, *args,
        **kwargs):
        """ Copy a file to/from NXOS device

        Copy any file to/from a device to any location supported on the
        device and on the running-configuration.

        Args:
        -----
            from_file_url: `str`
                Full path to the copy 'from' location
            to_file_url: `str`
                Full path to the copy 'to' location
            timeout_seconds: `str`
                The number of seconds to wait before aborting the operation.

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

            # Instantiate a filetransferutils instance for NXOS device
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

        try:
            self.send_cli_to_device(cli=cmd, timeout_seconds=timeout_seconds,
                **kwargs)
        except Exception as e:
            raise type(e)('{}'.format(e))

    def dir(self, from_directory_url, timeout_seconds, dir_output, *args,
        **kwargs):
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

            # Instantiate a filetransferutils instance for NXOS device
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

        # Extract device from the keyword arguments, if not passed raise an
        # AttributeError
        if 'device' in kwargs:
            device = kwargs['device']
        else:
            raise AttributeError("Devisce object is missing, can't proceed with"
                             " execution")

        # Call the parser
        try:
            obj = dir_output(device=device)
            parsed_output = obj.parse()
        except Exception as e:
            raise type(e)('{}'.format(e))

        return parsed_output

    def stat(self, file_url, timeout_seconds, *args, **kwargs):
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

            # Instantiate a filetransferutils instance for NXOS device
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

        # Extract device from the keyword arguments, if not passed raise an
        # AttributeError
        if 'device' in kwargs:
            device = kwargs['device']
        else:
            raise AttributeError("Devisce object is missing, can't proceed with"
                             " execution")

        parsed_output = self.dir(from_directory_url=file_url,
            timeout_seconds=timeout_seconds, device=device)

        return parsed_output

    def deletefile(self, file_url, timeout_seconds, *args, **kwargs):
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

            # Instantiate a filetransferutils instance for NXOS device
            >>> fu_device = FileUtils.from_device(device)

            # delete a specific file on device directory 'flash:'
            >>> directory_output = fu_device.deletefile(
            ...     file_url='flash:memleak_bckp.tcl',
            ...     timeout_seconds=300, device=device)

        """

        # delete flash:memleak.tcl
        cmd = 'delete {f}'.format(f=file_url)

        try:
            self.send_cli_to_device(cli=cmd, timeout_seconds=timeout_seconds,
                **kwargs)
        except Exception as e:
            raise type(e)('{}'.format(e))

    def renamefile(self, from_file_url, to_file_url, timeout_seconds, cmd,
        *args, **kwargs):
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

            # Instantiate a filetransferutils instance for NXOS device
            >>> fu_device = FileUtils.from_device(device)

            # rename the file on the device 'flash:' directory
            >>> fu_device.renamefile(file_url='flash:memleak.tcl',
            ...     to_file_url='memleak_backup.tcl'
            ...     timeout_seconds=300, device=device)

        """

        try:
            self.send_cli_to_device(cli=cmd, timeout_seconds=timeout_seconds,
                **kwargs)
        except Exception as e:
            raise type(e)('{}'.format(e))


    def chmod(self, file_url, mode, timeout_seconds, *args, **kwargs):
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

        # To be used when implemented
        # import stat as libstat
        # stat.filemode(output.st_mode)
        # libstat.filemode(mode)

        raise NotImplementedError("The fileutils module {} "
            "does not implement chmod.".format(self.__module__))

    def validateserver(self, cmd, timeout_seconds, file_path, *args, **kwargs):
        ''' Make sure that the given server information is valid


        Function that verifies if the server information given is valid, and if
        the device can connect to it. It does this by saving `show clock`
        output to a particular file using transfer protocol. Then deletes the
        file.

        Args:
            cmd (`str`):  Command to be executed on the device 
            file_path (`str`):  File path including the protocol, server and 
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

            # Instantiate a filetransferutils instance for NXOS device
            >>> fu_device = FileUtils.from_device(device)

            # Validate server connectivity
            >>> fu_device.validateserver(
            ...     file_path='ftp://10.1.7.250//auto/tftp-ssr/show_clock',
            ...     timeout_seconds=300, device=device)
        '''

        logger.info('Verifying if server can be reached and if a temp file can '
                    'be created')

        # Send the command
        try:
            self.send_cli_to_device(cli=cmd, timeout_seconds=timeout_seconds,
                **kwargs)
        except Exception as e:
            raise type(e)('TFTP/FTP server is unreachable') from e

        # Instantiate a server
        futlinux = server(testbed=self.testbed)

        # Check server created file
        try:
            futlinux.check_file(file_path)
        except Exception as e:
            raise type(e)("Server created file can't be checked") from e

        # Delete server created file
        try:
            futlinux.deletefile(file_path)
        except Exception as e:
            raise type(e)("Server created file can't be deleted") from e

        # Great success!
        logger.info("Server is ready to be used")
