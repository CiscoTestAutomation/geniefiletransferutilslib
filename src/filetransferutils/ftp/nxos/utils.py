'''
NXOS Implementation for Utils class
'''

# Python
import re
import os
import time
import random
import logging
import collections

# Super
from ..utils import Utils as ftputils

# Initialize the logger
logger = logging.getLogger(__name__)

# TODO Exception modification
# TODO Change ip str to ip IP object


class Utils(ftputils):
	def copy_core(self, *args, **kwargs):
		pass
