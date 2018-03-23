""" File utils base class for filetransferutils package. """
# Urlparse
from urllib.parse import urlparse

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# FileUtils Core
from ats.utils.fileutils import FileUtils as FileUtilsBase


class FileUtils(FileUtilsBase):

    def send_cli_to_device(self, cli, invalid=None, timeout_seconds=300,
    	**kwargs):
        """ Send command to a particular device and deal with its result

        Args:
        -----
            cli: `str`
            	Full command to be executed on the device
            invalid: `str`
            	Any invalid patterns need to be caught during execution
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

        ValueError
            When a device execution output shows one of the invalid patterns.

        Examples:
        ---------
			# FileUtils
			>>> from ..fileutils import FileUtils

        	# copy flash:/memleak.tcl ftp://10.1.0.213//auto/tftp-ssr/memleak.tcl
        	>>> cmd = 'copy {f} {t}'.format(f=from_file_url, t=to_file_url)

        	>>> FileUtils.send_cli_to_device(cli=cmd,
        	... 	timeout_seconds=timeout_seconds, **kwargs)
        """

        # Extract device from the keyword arguments, if not passed raise an
        # AttributeError
        if 'device' in kwargs:
        	device = kwargs['device']
        else:
            raise AttributeError("Device object is missing, can't proceed with"
                             " execution")

        # Extracting username and password to be used during device calls
        if 'username' in kwargs and 'password' in kwargs:
            username=kwargs['username']
            password=kwargs['password']
        elif device.testbed.servers:
        	# Assuming testbed file server is the same one passed by the user
	        for server in device.testbed.servers:
	        	if 'username' in device.testbed.servers[server]:
	        		username = device.testbed.servers[server]['username']
	        	if 'password' in device.testbed.servers[server]:
	        		password = device.testbed.servers[server]['password']
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
                    raise ValueError('ftp operation failed with the following '
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
        	... 	'flash'

        	>>> output.path
        	... 	'memleak.tcl'

        """
        parsed_url = urlparse(url)
        return parsed_url