import os
import time
import logging
import difflib

# Initialize the logger
logger = logging.getLogger(__name__)


class FileHelper(object):
    ''' Utilities class for files

    A group of statismethod function that does useful operations
    on files
    '''

    @staticmethod
    def check_no_file(file, tries=3, delay=5):
        ''' Verify if a specific file does not exists

        Loop mechanism to verify if a file does not exists

        Args:
            file (`str`) : Full path of the file to verify
            tries (`int`) : Amount of attempt to verify the file does not
                            exists (Optional, default 3)
            delay (`int`) : how long to sleep for between attempts
                            (Optional, default is 5)

        Returns:
            `bool`: `True` if the file does not exists, `False` otherwise

        Examples:

            >>> from filetransferutils.filehelper import FileHelper

            Let's verify that a file does not exists

            >>> FileHelper.check_no_file(file='/full/path/to/my/file')
            True

            Let's update tries to 5. As the file does not exists already, it
            will not do anything useful

            >>> FileHelper.check_no_file(file='/full/path/to/my/file', tries=5)
            True

        '''
        for _ in range(tries):
            if not os.path.isfile(file):
                return True
            time.sleep(delay)
        return False

    @staticmethod
    def check_file(file, tries=3, delay=5, ssh=None):
        ''' Verify if a specific file does exists

        Loop mechanism to verify if a file exists

        Args:
            file (`str`) : Full path of the file to verify
            tries (`int`) : Amount of attempt to verify the file does
                            exists (Optional, default 3)
            delay (`int`) : how long to sleep for between attempts
                            (Optional, default is 5)
            scp (`scp object`): If scp object passed, will use it to
                                to verify the file

        Returns:
            `bool`: `True` if the file does exists, `False` otherwise

        Examples:

            >>> from filetransferutils.filehelper import FileHelper

            Let's verify that a file exists. But of course, we know this file
            does not exists, hence it will loop 3 times, and sleep for 5
            seconds between each attempt

            >>> FileHelper.check_file(file='/full/path/to/my/file')
            False

            Same as previous example, but let's try 5 times!

            >>> FileHelper.check_file(file='/full/path/to/my/file', tries=5)
            False

        '''
        if ssh:
            for _ in range(tries):
                if ssh.sftp.stat(file):
                    return True
                time.sleep(delay)
            pass
        else:
            for _ in range(tries):
                if os.path.isfile(file):
                    return True
                time.sleep(delay)
        return False

    @staticmethod
    def is_same(file1, file2, ignore_list=[]):
        ''' Diff two files in a linux fashion

        Diff two files and print to screen the added and removed lines.

        All lines with a `-` in front means : This line existed in `file1` and
        does not exists in `file2`.

        All lines with a `+` in front means : This line did not exists in
        `file1` and now does exists in `file2`.

        With the `ignore_list` argument you can specify keywords. If
        any of those keywords are in any of the lines, those lines will not be
        diffed between files.

        Args:
            file1 (`str`) : Full path to the first file to diff
            file2 (`str`) : Full path to the second file to diff
            ignore_list (`list`) : List of keywords to specify which line to
                                   ignore for the diff

        Returns:
            `bool`: `True` if the file are identical, `False` otherwise

        Examples:

            >>> from filetransferutils.filehelper import FileHelper

            Let's diff two files which are identical

            >>> FileHelper.is_same(file1='/full/path/to/myfile1',
            ...                    file2='/full/path/to/myfile1')
            True

            Let's diff two files which are not identical

            >>> FileHelper.is_same(file1='/full/path/to/myfile1',
            ...                    file2='/full/path/to/myfile2')
            False

            Let's diff the same two files, but ignore datetime and one another
            dynamic value that keep changing

            >>> FileHelper.is_same(file1='/full/path/to/myfile1',
            ...                    file2='/full/path/to/myfile2',
            ...                    ignore_list=['datetime', 'clock'])
            True
        '''


        logger.info('Diff between \r\n{file1} \r\n{file2}'\
                    .format(file1=file1, file2=file2))

        # Default list
        removed_config = []
        added_config = []

        # Open both files
        with open(file1, 'r') as input1, open(file2, 'r') as input2:
            # Store files into variables
            out1 = input1.readlines()
            out2 = input2.readlines()

        # Create the diff
        diff = difflib.ndiff(out1, out2)

        # Check line by line
        # diff is a generator
        for line in diff:
            # Ignore from the ignore_list
            if any(word in line for word in ignore_list) or\
               line.startswith('  '):
                continue
            elif line.startswith('-'):
                # Removed stuff!
                removed_config.append(line.strip())
            elif line.startswith('+'):
                # Added stuff!
                added_config.append(line.strip())

        # Print stuff that was added/removed
        # we are printing both even though maybe only one list contains items
        # It removes the ambiguity of the user to know if there was
        # of the other type
        if removed_config or added_config:
            logger.warning("Added configuration: \r\n{added}"\
                    .format(added='\r\n'.join(added_config)))
            logger.warning("Removed configuration: \r\n{removed}"\
                    .format(removed='\r\n'.join(removed_config)))
            # Not the same
            return False
        # Same!
        return True