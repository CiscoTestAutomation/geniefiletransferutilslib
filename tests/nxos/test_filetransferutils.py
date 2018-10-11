#!/usr/bin/env python

# import python
import os
import unittest
from unittest.mock import patch
from unittest.mock import Mock

# ATS
from ats.topology import Testbed
from ats.topology import Device
from ats.datastructures import AttrDict

# filetransferutils
try:
    from pyats.utils.fileutils import FileUtils
except:
    from ats.utils.fileutils import FileUtils


class test_filetransferutils(unittest.TestCase):
    # Instantiate tesbed and device objects
    tb = Testbed(name='myTestbed')
    device = Device(testbed=tb, name='aDevice', os='nxos')

    # Instantiate a filetransferutils instance for NXOS device
    fu_device = FileUtils.from_device(device)

    # Add testbed servers for authentication
    device.testbed.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw", address='1.1.1.1'),
    )

    dir_output = ['bootflash:/ISSUCleanGolden.system.gbin',
        'bootflash:/ISSUCleanGolden.cfg', 'bootflash:/platform-sdk.cmd',
        'bootflash:/virt_strg_pool_bf_vdc_1/', 'bootflash:/virtual-instance/',
        'bootflash:/virtual-instance.conf', 'bootflash:/.rpmstore/',
        'bootflash:/.swtam/', 'bootflash:/scripts/']

    # Mock device output
    raw1 = {'execute.return_value': '''
        copy bootflash:/virtual-instance.conf ftp://10.1.0.213//auto/tftp-ssr/virtual-instance.conf vrf management
        Enter username: rcpuser
        Password: 
        ***** Transfer of file Completed Successfully *****
        Copy complete.
    '''}

    raw2 = '''
        dir
               4096    Jan 25 21:00:53 2017  .rpmstore/
               4096    Jan 25 21:01:08 2017  .swtam/
                390    Jan 25 21:36:20 2017  ISSUCleanGolden.cfg
          752699904    Jan 25 21:36:26 2017  ISSUCleanGolden.system.gbin
                  0    Jan 25 21:35:55 2017  platform-sdk.cmd
               4096    Jan 25 21:01:57 2017  scripts/
               4096    Jan 25 21:02:02 2017  virt_strg_pool_bf_vdc_1/
               4096    Jan 25 21:01:21 2017  virtual-instance/
                 59    Jan 25 21:01:11 2017  virtual-instance.conf

        Usage for bootflash://
         1150812160 bytes used
         2386407424 bytes free
         3537219584 bytes total
    '''

    raw3 = {'execute.return_value': '''
        delete bootflash:new_file.tcl
        Do you want to delete "/new_file.tcl" ? (yes/no/abort)   [y] 
    '''}

    raw4 = {'execute.return_value': '''
        move bootflash:mem_leak.tcl new_file.tcl
    '''}

    raw5 = {'execute.return_value': '''
        show clock > ftp://10.1.7.250//auto/tftp-ssr/show_clock vrf management
        Enter username: rcpuser
        Password: 
        ***** Transfer of file Completed Successfully *****
    '''}

    raw6 = {'futlinux.check_file.return_value': '',
        'futlinux.deletefile.return_value': ''}

    raw7 = {'execute.return_value': '''
        copy running-config tftp://10.1.7.250//auto/tftp-ssr/test_config.py vrf management
        Trying to connect to tftp server......
        Connection to Server Established.
        [                         ]         0.50KB[#                        ]         4.50KB[##                       ]         8.50KB[###                      ]        12.50KB                                                                                    TFTP put operation was successful
        Copy complete, now saving to disk (please wait)...
        Copy complete.
    '''}

    outputs = {}
    outputs['copy bootflash:/virtual-instance.conf '
        'ftp://10.1.0.213//auto/tftp-ssr/virtual-instance.conf vrf management']\
         = raw1
    outputs['dir'] = raw2
    outputs['delete bootflash:new_file.tcl'] = raw3
    outputs['move bootflash:mem_leak.tcl new_file.tcl'] = raw4
    outputs['show clock > ftp://1.1.1.1//auto/tftp-ssr/show_clock vrf management'] = raw5
    outputs['copy running-config tftp://10.1.7.250//auto/tftp-ssr/test_config.py vrf management'] = raw7

    def mapper(self, key, timeout=None, reply= None):
        return self.outputs[key]

    def test_copyfile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        # Call copyfiles
        self.fu_device.copyfile(source='bootflash:/virtual-instance.conf',
            destination='ftp://10.1.0.213//auto/tftp-ssr/virtual-instance.conf',
            timeout_seconds='300', device=self.device)

    def test_dir(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        directory_output = self.fu_device.dir(target='bootflash:',
            timeout_seconds=300, device=self.device)

        self.assertEqual(sorted(directory_output), sorted(self.dir_output))

    def test_stat(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        file_details = self.fu_device.stat(
            target='bootflash:virtual-instance.conf',
            timeout_seconds=300, device=self.device)

        self.assertEqual(file_details['time'], '21:01:11')
        self.assertEqual(file_details['date'], 'Jan 25 2017')
        self.assertEqual(file_details['size'], '59')

    def test_deletefile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.deletefile(target='bootflash:new_file.tcl',
          timeout_seconds=300, device=self.device)

    def test_renamefile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.renamefile(source='bootflash:mem_leak.tcl',
          destination='new_file.tcl',
          timeout_seconds=300, device=self.device)

    @patch('genie.libs.filetransferutils.plugins.fileutils.FileUtils.validateserver',
        return_value=raw6)
    def test_validateserver(self, raw6):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.validateserver(
            target='ftp://1.1.1.1//auto/tftp-ssr/show_clock',
            timeout_seconds=300, device=self.device)

    def test_copyconfiguration(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.copyconfiguration(source='running-config',
          destination='tftp://10.1.7.250//auto/tftp-ssr/test_config.py',
          timeout_seconds=300, device=self.device)


if __name__ == '__main__':
    unittest.main()

# vim: ft=python et sw=4