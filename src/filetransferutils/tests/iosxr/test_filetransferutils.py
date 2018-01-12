#!/usr/bin/env python

# import python
import os
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device

# abstract
from abstract import Lookup

# filetransferutils
import filetransferutils
from filetransferutils.ssh import Ssh


class test_filetransferutils(unittest.TestCase):
	device = Device(name='aDevice', os='iosxr')

	# Establish server connection
	scp = Ssh(ip='10.1.7.250')
	scp.setup_scp()

	# Mock device output
	raw1 = {'execute.return_value': '''
		[OK]
	'''}

	# Mock device output
	raw2 = {'execute.return_value': '''
		Destination filename [/auto/tftp-ssr/corefile.core.gz]?
		Writing tftp://10.1.7.250/auto/tftp-ssr/corefile.core.gz
		CCCC
		3626697 bytes copied in      3 sec (  1041854)bytes/sec
	'''}

	raw3 = '''\
		% Please answer 'yes' or 'no'.
		Would you like to proceed in configuration mode? [no]: yes
		RP/0/RSP1/CPU0:PE1(config)#load tftp://10.1.7.250//auto/tftp-ssr/new_file-2018$
		Loading.
		0 bytes parsed in 1 sec (0)bytes/sec
	'''

	outputs = {}
	outputs['show version brief | file tftp://10.1.7.250//auto/tftp-ssr/test_file_name.py'] = raw1
	outputs['copy crashinfo:/corefile.core.gz tftp://10.1.7.250//auto/tftp-ssr/corefile.core.gz'] = raw2
	outputs['show clock | file tftp://10.1.7.250//auto/tftp-ssr/aDevice'] = raw1
	outputs['load tftp://10.1.7.250//auto/tftp-ssr/new_file-2018-01-10-10_24_58'] = raw3

	def mapper(self, key, timeout=None, reply= None):
		return self.outputs[key]

	# Get the corresponding filetransferutils Utils implementation
	tftpcls = Lookup(device.os).filetransferutils.tftp.utils.Utils(
		scp, '/auto/tftp-ssr/')

	def test_copy_device_output_to_server(self):

		self.device.execute = Mock()
		self.device.execute.side_effect = self.mapper

		# Create file on the server
		f = open(os.path.join('/auto/tftp-ssr/', 'test_file_name.py'), 'w')

		self.tftpcls.copy_CLI_output(device=self.device, filename='test_file_name.py',
			cli='show version brief')

		# Delete the temp file created
		os.remove('/auto/tftp-ssr/test_file_name.py')

	def test_copy_core(self):

		self.device.execute = Mock()
		self.device.execute.side_effect = self.mapper

		# Create core on the server
		f = open(os.path.join('/auto/tftp-ssr/', 'corefile.core.gz'), 'w')

		self.tftpcls.copy_core(device=self.device,
			location='crashinfo:',
			core='corefile.core.gz',
			server='',
			destination='')

		# Delete the temp file created
		os.remove('/auto/tftp-ssr/corefile.core.gz')

	def test_validate_server(self):

		self.device.execute = Mock()
		self.device.execute.side_effect = self.mapper

		# Create core on the server
		f = open(os.path.join('/auto/tftp-ssr/', 'aDevice'), 'w')

		self.tftpcls.validate_server(device=self.device, vrf=None,
			filename=self.device.name)

		# validate_server method already deletes the temp created file

	def test_copy_file_to_device(self):

		self.device.configure = Mock()
		self.device.configure.side_effect = self.mapper

		# Create a temporary filename to be used later in the code
		# Needed fo rlater check with the above defined sideeffect
		temp_filename = '/auto/tftp-ssr/new_file-2018-01-10-10_24_58'

		# Create core on the server
		f = open(os.path.join('/auto/tftp-ssr/', 'new_file'), 'w')

		try:
			self.tftpcls.copy_file_to_device(device=self.device,
				filename='/auto/tftp-ssr/new_file', location='running-config',
				invalid=None, temp_filename=temp_filename)
		except Exception as e:
			# Handling the case of running unittest as unittest discovery under the package
			if e.args[0] == "Issue scp'ing '/auto/tftp-ssr/new_file' to '10.1.7.250'":
				pass
			else:
				raise Exception("{d}".format(d=e.args[0]))

		# Delete the temp file created
		os.remove('/auto/tftp-ssr/new_file')


if __name__ == '__main__':
    unittest.main()

# vim: ft=python et sw=4
