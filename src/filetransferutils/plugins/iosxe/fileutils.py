""" File utils base class for XE devices. """

from ... import FileUtils as FileUtilsDeviceBase

class FileUtils(FileUtilsDeviceBase):

    def copyfile(self, from_file_url, to_file_url,
            timeout_seconds, *args, **kwargs):
        """ Copy a single file.

        Copy a single file either from local to remote, or remote to local.
        Remote to remote transfers are not supported.  Users are expected
        to make two calls to this API to do this.

        Raises
        ------
        Exception
            When a remote to remote transfer is requested.

        """
        super().copyfile(*args, **kwargs)

    def dir(self, from_directory_url, timeout_seconds, *args, **kwargs):
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
            `list` : List of filename URLs.  Directory names are ignored.

        """
        raise NotImplementedError("The fileutils module {} "
            "does not implement dir.".format(self.__module__))


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
            `os.stat_result` : Filename details including size.

        Raises
        ------
        Exception
            timeout exceeded

        Exception
            File was not found

        """

        raise NotImplementedError("The fileutils module {} "
            "does not implement stat.".format(self.__module__))


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

        raise NotImplementedError("The fileutils module {} "
            "does not implement chmod.".format(self.__module__))


    def deletefile(self, file_url, timeout_seconds, *args, **kwargs):
        """ Delete a file

        Parameters
        ----------
            file_url : `str`
                The URL of the file to be deleted.

            timeout_seconds : `int`
                Maximum allowed amount of time for the operation.

        """

        raise NotImplementedError("The fileutils module {} "
            "does not implement deletefile.".format(self.__module__))


    def renamefile(self, from_file_url, to_file_url,
            timeout_seconds, *args, **kwargs):
        """ Rename a file

        Parameters
        ----------
            from_file_url : `str`
                The URL of the file to be renamed.

            to_file_url : `str`
                The URL of the new file name.

            timeout_seconds : `int`
                Maximum allowed amount of time for the operation.

        """

        raise NotImplementedError("The fileutils module {} "
            "does not implement renamefile.".format(self.__module__))

