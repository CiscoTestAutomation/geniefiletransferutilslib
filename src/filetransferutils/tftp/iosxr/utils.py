'''
IOSXR Implementation for TFTPUtils class
'''

# Python
import re
import os
import random
import logging

# FileHelper
from filetransferutils.filehelper import FileHelper

# Super
from ..utils import Utils as tftputils

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Initialize the logger
logger = logging.getLogger(__name__)

# This part of the code will be removed once Genie officially move to UNICON
from enum import Enum
from collections import OrderedDict

class ConnectionType(Enum):
    CSCCON = 1
    UNICON = 2
    NONE = 99

IMPORT_LIBS = dict()

# importing csccon
try:
    from ats import tcl as atsTcl
    from csccon import Csccon
except ImportError:
    pass
else:
    IMPORT_LIBS['csccon'] = (Csccon, ConnectionType.CSCCON)

# importing unicon
try:
    from unicon import Connection
    from unicon.eal.dialogs import Statement, Dialog
except ImportError:
    pass
else:
    IMPORT_LIBS['unicon'] = (Connection, ConnectionType.UNICON)

def get_connection(device, mapping = None):
    """get_connection api

    This is to retrieve connection from the device

    Args:
        device(`device`): device to use
        mapping(`str`): connection mapping to be used for configuration
                        Default: None, default connection will be used

    """

    if not device:
        return None

    connectionmgr = device.connectionmgr
    connections = connectionmgr.connections
    default_alias = connectionmgr.default_alias

    # determine the connection default one or from mapping
    connection_cls = connections.get(default_alias, None)
    if hasattr(device, 'mapping') and mapping:
        named = device.mapping.get(mapping, None)
        if named:
            # get named connection from pool, backup with default connection
            connection_cls = connections.get(named, connection_cls)

    return connection_cls

def get_connection_type(device, mapping = None, connection_cls = None):
    """get_connection_type api

    This is to retrieve connection type from the device conenction

    Args:
        device(`device`): device to use
        mapping(`str`): connection mapping to be used for configuration
                        Default: None, default connection will be used
        connection_cls(`BaseConnection`): device connection to be configured
                        Default: None, default connection will be used

    """

    # get device connection
    connection_cls = connection_cls or \
                              get_connection(device = device, mapping = mapping)
    if connection_cls:
        # get the connection type : either csccon or unicon
        for lib in ('csccon', 'unicon'):
            if lib in IMPORT_LIBS:
                cls, connection_type = IMPORT_LIBS.get(lib)
                if isinstance(connection_cls, cls):
                    return connection_type

    return ConnectionType.NONE
# ------------------------------------------------------------------------------

class Utils(tftputils):

    def copy_file_to_device(self, *args, **kwargs):
        ''' Copy a file to a device via tftp

        Copy any file to a device via Tftp to any location supported on the
        device.

        Args:
            Device (`device object`): Device
            filename (`str`): Relative path to file desired to be copied on the
                               device
            location (`str`): Where to store the file on the device
            vrf (`str`):  Vrf to use. (Optional, default is management)

        Returns:
            `None`

        Examples:

            Create a tftp instance

            >>> tftp = TFTPUtils(server = 'tftpServer1',
            ...                  ip = '10.10.10.10',
            ...                  location = '/tftpboot')

            Copy the file /auto/my_path/my_config to the device running-config

            >>> tftp.copy_file_to_device(device = <device object>,
            ...                          filename = '/auto/my_path/my_config',
            ...                          location = 'running-config')
        '''
        cmd = 'load tftp://{ip}/{file}'

        return super().copy_file_to_device(cmd=cmd, *args, **kwargs)

    def copy_CLI_output(self, filename, cli, *args, **kwargs):
        '''Save a cli output to a file outside of the device via tftp

        Args:
            Device (`device object`): Device
            filename (`str`): Relative path to file where the output will be
                               saved
            cli (`str`): Command to send to the device to save the output
            vrf (`str`):  Vrf to use. Use as a default `management`

        Returns:
            `None`

        Examples:

            Create a tftp instance

            >>> tftp = TFTPUtils(server = 'tftpServer2',
            ...                  ip = '10.10.10.10',
            ...                  location = '/tftpboot')

            Save the output of a particular command to the file
            /auto/my_path/show_mod

            >>> tftp.copy_CLI_output(device = <device object>,
            ...                  filename = 'show_mod',
            ...                  cli = 'show module')
        '''

        file = os.path.join(self.directory, filename)
        cmd = "{cli} | file tftp://{ip}/{file}"\
               .format(cli=cli, ip=self.scp.ip, file=file)

        return super().copy_CLI_output(filename=filename, cli=cli, cmd=cmd, *args,
                                   **kwargs)

    def validate_server(self, *args, **kwargs):
        ''' Make sure that the given tftp information is valid


        Function that verifies if the Tftp information given is valid, and if
        the device can connect to the tftp. It does this by saving
        `show clock` output to a particular file using tftp. Then deletes the
        file

        Args:
            Device (`device object`): Device
            vrf (`str`):  Vrf to use. Use as a default `management`

        Returns:
            `None`

        Raises:
            Exception: If the command from the device to tftp is
                       unreachable
            FileNotFoundError: If the command was sent correctly, but the file
                               did not create

        Examples:
            >>> tftp = TFTPUtils(server = 'tftpServer1',
            ...                  ip = '10.10.10.10',
            ...                  location = '/tftpboot')

            >>> tftp.validate_server(device = <device object>)
        '''

        logger.info('Verifying if TFTP can be reached and if a temp file can '
                    'be created')

        device = kwargs['device']
        # prepare the temp file name
        if 'filename' not in kwargs:
            filename = '.'.join([device.name, str(random.randint(0,999))])
        else:
            filename = kwargs['filename']

        # Add base + newly generated file name
        file = os.path.join(self.directory, filename)

        # Patch up the command together
        # show clock | file tftp://10.1.0.214//auto/tftp-best/lrasheed_test
        cli = "show clock | file tftp://{ip}/{file}".format(ip=self.scp.ip,
                                                            file=file)

        # Send the command
        try:
            self._send_cli_to_device(device=device, cli=cli)
        except Exception as e:
            # oops, it failed
            # Re-raise and add our message
            raise type(e)('TFTP server is unreachable') from e

        # Let's verify the file is there
        # TODO Nice way to pass tries + delay
        if not FileHelper.check_file(file=file):
            raise FileNotFoundError('Even though the cli was send correctly '
                                     'to the device, {file} was not '
                                     'created'.format(file=file))

        # In the future, might need to use a ssh method to delete it
        # But most likely no need
        os.remove(file)

        # Great success!
        logger.info("Tftp is ready to be used")

    def _configure_cli_on_device(self, device, cli, invalid=None, timeout=300, **kwargs):
        
        ''' Send command to a particular device and deal with its result '''

        if 'username' in kwargs and 'password' in kwargs:
            username=kwargs['username']
            password=kwargs['password']
        else:
            username = None
            password = None

        # Create unicon dialog
        dialog = Dialog([
            Statement(pattern=r'Would you like to proceed in configuration mode\? \[no\]:',
                      action='sendline({answer})'.format(answer='yes'),
                      loop_continue=True,
                      continue_timer=False),
            ])

        # TODO: Need to handle the copy core scenario
        if getattr(get_connection_type(device), 'name') == 'CSCCON':
            output  = device.configure(cli)
        else:
            output  = device.configure(cli, timeout=timeout, reply=dialog)

        # Todo: better way to filter out the errors
        # Might need dynamic, so this can be controlled via that common cfg file
        fail_msg = ['failed to copy', 'Unable to find', 'Error opening']
        if invalid:
            fail_msg.extend(invalid)
        for line in output.splitlines():
            if any(re.match(word, line) for word in fail_msg):
                raise ValueError('Tftp operation failed: '
                                 '{line}'.format(line=line))