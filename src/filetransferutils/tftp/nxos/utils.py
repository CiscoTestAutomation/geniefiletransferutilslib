'''
NXOS Implementation for TFTPUtils class
'''

# Python
import re
import os
import time
import logging

# Super
from ..utils import Utils as tftputils

# Initialize the logger
logger = logging.getLogger(__name__)


class Utils(tftputils):

    def save_core(self, *args, **kwargs):
        '''Save a core to a tftp location

        Args:
            Device (`device object`): Device
            filename (`str`): Relative path to file where the output will be
                               saved
            core (`str`): Core to save
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

            >>> tftp.save_core(device = <device object>,
            ...                core = '//1//10616',
                               filename = 'mycore')
        '''

        file = os.path.join(self.directory, kwargs['destination'])

        return super().save_core(file=file, *args, **kwargs)

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

        # prepare the temp file name
        if 'filename' not in kwargs:
            filename = '.'.join([device.name, time.strftime("%Y-%m-%d.%H.%M.%S",
                time.localtime())])
        else:
            filename = kwargs['filename']

        file = os.path.join(self.directory, filename)

        return super().basic_check(device=device, file=file, **kwargs)
