""" File utils base class for filetransferutils package. """
# Urlparse
from urllib.parse import urlparse

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# FileUtils Core
from ats.utils.fileutils import FileUtils as FileUtilsBase


class FileUtils(FileUtilsBase):

    def send_cli_to_device(self, cli, used_server=None, invalid=None,
      timeout_seconds=300, **kwargs):
        """ Send command to a particular device and deal with its result

        Args:
        -----
            cli: `str`
              Full command to be executed on the device
            invalid: `str`
              Any invalid patterns need to be caught during execution
            timeout_seconds: `str`
              The number of seconds to wait before aborting the operation.
            used_server: `str`
              Server address/name

        Returns:
        --------
            `None`

        Raises
        ------
        Exception
            When a device object is not present or device execution encountered
            an unexpected behavior.

        ValueError
            When a device execution output shows one of the invalid patterns.

        Examples:
        ---------
      # FileUtils
      >>> from ..fileutils import FileUtils

          # copy flash:/memleak.tcl ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl
          >>> cmd = 'copy {f} {t}'.format(f=from_file_url, t=to_file_url)

          >>> FileUtils.send_cli_to_device(cli=cmd,
          ...   timeout_seconds=timeout_seconds, **kwargs)
        """

        # Extract device from the keyword arguments, if not passed raise an
        # AttributeError
        if 'device' in kwargs:
            device = kwargs['device']
        else:
            raise AttributeError("Device object is missing, can't proceed with"
                             " execution")

        # Extracting username and password to be used during device calls
        if used_server:
            username, password = self.get_auth(used_server)
        else:
            username = None
            password = None

        # Checking if user passed any extra invalid patterns
        if 'invalid' in kwargs:
            invalid = kwargs['invalid']

        # Create unicon dialog
        dialog = Dialog([
            Statement(pattern=r'Address or name of remote host.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination filename.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'\[confirm\]',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination username:.*',
                      action='sendline({username})'.format(username=username),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination password:.*',
                      action='sendline({password})'.format(password=password),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination filename.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Enter username:',
                      action='sendline({username})'.format(username=username),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Password:',
                      action='sendline({password})'.format(password=password),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Do you want to delete.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            ])

        try:
            output = device.execute(cli, timeout=timeout_seconds, reply=dialog)

            # Error patterns to be caught when executing cli on device
            fail_msg = ['failed to copy', 'Unable to find', 'Error opening',\
                'Error', 'operation failed']

            # Check if user passed extra error/fail patterns to be caught
            if invalid:
                fail_msg.extend(invalid)

            # Checking for the error/fail patterns, raise an exception if found
            for word in fail_msg:
                if word in output:
                    raise ValueError('Operation failed with the following '
                                     'reason: {line}'.format(line=word))
        except Exception as e:
            raise type(e)('{}'.format(e))

        return output

    def parse_url(self, url):
        """ Parse the given url

        Args:
        -----
            url: `str`
              Full url to be parsed

        Returns:
        --------
            ParseResult class with the following keyword arguments
            (scheme='', netloc='', path='', params='', query='', fragment='')

        Raises
        ------
          None

        Examples:
        ---------
        # FileUtils
        >>> from ..fileutils import FileUtils

        # Extract the file name and location
          >>> output = FileUtils.parse_url(file_url)
                  ParseResult(scheme='flash', netloc='', path='memleak.tcl',
                  params='', query='', fragment='')

          >>> output.scheme
          ...   'flash'

          >>> output.path
          ...   'memleak.tcl'

        """
        parsed_url = urlparse(url)
        return parsed_url

    def get_server(self, from_file_url, to_file_url):
        """ Get the server address from the provided URLs

        Args:
        -----
            from_file_url: `str`
              URL path of the from location
            to_file_url: `str`
              URL path of the to location


        Returns:
        --------
            used_server: `str`
              String of the used server

        Raises
        ------
          None

        Examples:
        ---------
        # FileUtils
        >>> from ..fileutils import FileUtils

        # Extract the file name and location
          >>> output = FileUtils.get_server(from_file_url, to_file_url)

          >>> output
          ...   '10.1.7.250'

        """
        # Extract the server address to be used later for authentication
        new_list = [from_file_url, to_file_url]
        for item in new_list:
            parsed = self.parse_url(item)
            if parsed.netloc:
                used_server = parsed.netloc
                break
            else:
                continue

        return used_server