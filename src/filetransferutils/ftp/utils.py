import re
import os
import time
import getpass
import logging
import datetime

#import subprocess
import collections

from ..filehelper import FileHelper

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Initialize the logger
logger = logging.getLogger('ats.aetest')

# TODO Change ip str to ip IP object

class Utils(object):
    ''' Utilities class for Ftp

    Class is containing utility functions for a ftp server. The same instance
    can be used by multiples devices, as each device is an argument passed in
    all the methods.

    Args:
        ip (`str`): Ftp IP address
        server (`str`): Ftp server name
        directory (`str`): Ftp directory

    Examples:

        >>> ftp = Utils(scp=<scp object>,
        ...             directory = '/tftpboot')
    '''

    def __init__(self, scp, directory, *args, **kwargs):
        pass

    def copy_file_to_device(self, device, filename, location, invalid,
                            vrf='management', cmd=None, delay=1, tries=1):
        pass

    def save_output(self, device, filename, cli, vrf='management', tries=1,
                    delay=1, cmd=None):
        pass

    def save_core(self, device, location, core, server, destination, port=None,
                  vrf=None, tries=1, delay=1, cmd=None,
                  timeout=None, invalid=None, **kwargs):
        pass

    def basic_check(self, device, vrf='management'):
        pass

    def _send_cli_to_device(self, device, cli, invalid=None, timeout=300, **kwargs):
        pass