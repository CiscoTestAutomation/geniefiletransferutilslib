import os
import time
import logging
import collections

# Unicon
from unicon.eal.dialogs import Statement, Dialog

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
