'''
IOSXR Implementation for Utils class
'''

# Python
import re
import os
import time
import random
import logging
import collections

# FileHelper
from filetransferutils.filehelper import FileHelper

# Super
from ..utils import Utils as ftputils

# Initialize the logger
logger = logging.getLogger(__name__)

# TODO Exception modification
# TODO Change ip str to ip IP object


class Utils(ftputils):
	def copy_file_to_device(self, *args, **kwargs):
		pass

	def copy_CLI_output(self, filename, cli, *args, **kwargs):
		pass

	def validate_server(self, *args, **kwargs):
		pass

	def _configure_cli_on_device(self, device, cli, invalid=None, **kwargs):
		pass