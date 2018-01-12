'''
IOSXE Implementation for TFTPUtils class
'''

# Python
import os
import time
import logging

# Super
from ..utils import Utils as tftputils

# Initialize the logger
logger = logging.getLogger(__name__)


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

        # Remove vrf on the call

        cmd = 'copy tftp://{ip}/{file} {location}'

        return super().copy_file_to_device(cmd=cmd, *args, **kwargs)

    def save_output(self, filename, cli, *args, **kwargs):
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

            >>> tftp.save_output(device = <device object>,
            ...                  filename = 'show_mod',
            ...                  cli = 'show module')
        '''

        # Remove vrf on the call
        file = os.path.join(self.directory, filename)
        cmd = "{cli} | redirect tftp://{ip}/{file}"\
               .format(cli=cli, ip=self.scp.ip, file=file)

        return super().save_output(filename=filename, cli=cli, cmd=cmd, *args,
                                   **kwargs)

    def basic_check(self, device, **kwargs):
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

            >>> tftp.basic_check(device = <device object>)
        '''

        # Remove vrf on the call
        if 'vrf' in kwargs:
            kwargs['vrf'] = None

        # prepare the temp file name
        if 'filename' not in kwargs:
            filename = '.'.join([device.name, time.strftime("%Y-%m-%d.%H.%M.%S",
                time.localtime())])
        else:
            filename = kwargs['filename']

        file = os.path.join(self.directory, filename)
        cmd = "show clock | redirect tftp://{ip}/{file}"\
               .format(ip=self.scp.ip, file=file)

        return super().basic_check(device=device, cli=cmd, file=file, **kwargs)
