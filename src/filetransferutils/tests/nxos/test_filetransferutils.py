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
from ats.utils.fileutils import FileUtils


class test_filetransferutils(unittest.TestCase):
    # Instantiate tesbed and device objects
    tb = Testbed(name='myTestbed')
    device = Device(testbed=tb, name='aDevice', os='iosxe')

    # Instantiate a filetransferutils instance for IOSXE device
    fu_device = FileUtils.from_device(device)

    # Add testbed servers for authentication
    device.testbed.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw", address='1.1.1.1'),
    )

    dir_output = {'.dbpersist': {'index': '69719',
                        'last_modified_date': 'Feb 12 2018 11:20:01 +00:00',
                        'permissions': 'drwx',
                        'size': '4096'},
         '.installer': {'index': '69698',
                        'last_modified_date': 'Mar 20 2018 10:25:11 +00:00',
                        'permissions': 'drwx',
                        'size': '4096'},
         '.prst_sync': {'index': '15489',
                        'last_modified_date': 'Mar 20 2018 10:31:08 +00:00',
                        'permissions': 'drwx',
                        'size': '4096'},
         '.rollback_timer': {'index': '30977',
                             'last_modified_date': 'May 2 2016 07:58:53 +00:00',
                             'permissions': 'drwx',
                             'size': '4096'},
         'CRDU': {'index': '69721',
                  'last_modified_date': 'Sep 25 2017 07:59:54 +00:00',
                  'permissions': 'drwx',
                  'size': '4096'},
         'ISSUCleanGolden': {'index': '69708',
                             'last_modified_date': 'Sep 27 2017 09:11:39 +00:00',
                             'permissions': '-rw-',
                             'size': '617329255'},
         'RestoreTue_Mar_20_12_13_39_2018-Mar-20-11-14-38.106-0': {'index': '69735',
                                                                   'last_modified_date': 'Mar '
                                                                                         '20 '
                                                                                         '2018 '
                                                                                         '11:14:45 '
                                                                                         '+00:00',
                                                                   'permissions': '-rw-',
                                                                   'size': '27145'},
         'RestoreTue_Mar_20_12_19_11_2018-Mar-20-11-20-09.900-0': {'index': '69736',
                                                                   'last_modified_date': 'Mar '
                                                                                         '20 '
                                                                                         '2018 '
                                                                                         '11:20:16 '
                                                                                         '+00:00',
                                                                   'permissions': '-rw-',
                                                                   'size': '27145'},
         'boothelper.log': {'index': '69699',
                            'last_modified_date': 'Mar 20 2018 10:25:46 +00:00',
                            'permissions': '-rw-',
                            'size': '76'},
         'bootloader_evt_handle.log': {'index': '69700',
                                       'last_modified_date': 'Mar 20 2018 10:25:27 '
                                                             '+00:00',
                                       'permissions': '-rw-',
                                       'size': '90761'},
         'core': {'index': '69701',
                  'last_modified_date': 'Feb 1 2018 13:44:32 +00:00',
                  'permissions': 'drwx',
                  'size': '4096'},
         'dc_profile_dir': {'index': '38722',
                            'last_modified_date': 'Mar 20 2018 10:25:43 +00:00',
                            'permissions': 'drwx',
                            'size': '4096'},
         'gs_script': {'index': '69709',
                       'last_modified_date': 'Aug 3 2016 08:07:47 +00:00',
                       'permissions': 'drwx',
                       'size': '4096'},
         'iox': {'index': '69714',
                 'last_modified_date': 'Aug 13 2016 08:55:12 +00:00',
                 'permissions': 'drwx',
                 'size': '4096'},
         'memleak.tcl': {'index': '69705',
                         'last_modified_date': 'Mar 20 2018 10:26:01 +00:00',
                         'permissions': '-rw-',
                         'size': '104260'},
         'nvram_config': {'index': '69720',
                          'last_modified_date': 'Mar 20 2018 13:09:24 +00:00',
                          'permissions': '-rw-',
                          'size': '2097152'},
         'nvram_config_bkup': {'index': '69703',
                               'last_modified_date': 'Mar 20 2018 13:09:25 +00:00',
                               'permissions': '-rw-',
                               'size': '2097152'},
         'onep': {'index': '69706',
                  'last_modified_date': 'May 2 2016 08:11:23 +00:00',
                  'permissions': 'drwx',
                  'size': '4096'},
         'stby-vlan.dat': {'index': '69729',
                           'last_modified_date': 'Feb 12 2018 12:51:01 +00:00',
                           'permissions': '-rw-',
                           'size': '3496'},
         'tech_support': {'index': '69727',
                          'last_modified_date': 'Oct 23 2017 13:40:11 +00:00',
                          'permissions': 'drwx',
                          'size': '4096'},
         'tools': {'index': '69712',
                   'last_modified_date': 'Mar 19 2017 09:26:23 +00:00',
                   'permissions': 'drwx',
                   'size': '4096'},
         'vlan.dat': {'index': '69734',
                      'last_modified_date': 'Mar 11 2018 17:40:26 +00:00',
                      'permissions': '-rw-',
                      'size': '3496'}}

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
        delete flash:memleak.tcl
        Delete filename [memleak.tcl]? 
        Delete flash:/memleak.tcl? [confirm]
    '''}

    raw4 = {'execute.return_value': '''
        rename flash:memleak.tcl new_file.tcl
        Destination filename [new_file.tcl]? 
    '''}

    raw5 = {'execute.return_value': '''
        show clock | redirect ftp://1.1.1.1//auto/tftp-ssr/show_clock
        Writing /auto/tftp-ssr/show_clock 
    '''}

    raw6 = 'INFO:ats.utils.fileutils.plugins.linux.fileutils:Retrieving details for file ftp://10.1.7.250//auto/tftp-ssr/show_clock ...'

    raw7 = 'INFO:ats.utils.fileutils.plugins.linux.fileutils:Deleting file ftp://10.1.7.250//auto/tftp-ssr/show_clock ...'

    outputs = {}
    outputs['copy bootflash:/virtual-instance.conf ftp://10.1.0.213//auto/tftp-ssr/virtual-instance.conf'] = raw1
    outputs['dir'] = raw2
    outputs['delete flash:memleak.tcl'] = raw3
    outputs['rename flash:memleak.tcl new_file.tcl'] = raw4
    outputs['show clock | redirect ftp://1.1.1.1//auto/tftp-ssr/show_clock'] = raw5

    def mapper(self, key, timeout=None, reply= None):
        return self.outputs[key]

    def test_copyfile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        # Create file on the server
        f = open(os.path.join('/auto/tftp-ssr/', 'memleak.tcl'), 'w')

        # Call copyfiles
        self.fu_device.copyfile(from_file_url='bootflash:/virtual-instance.conf',
            to_file_url='ftp://10.1.0.213//auto/tftp-ssr/virtual-instance.conf',
            timeout_seconds='300', device=self.device)

        # Delete the temp file created
        os.remove('/auto/tftp-ssr/memleak.tcl')

    def test_dir(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        directory_output = self.fu_device.dir(from_directory_url='bootflash:',
            timeout_seconds=300, device=self.device)

        self.assertEqual(directory_output, self.dir_output)

    # def test_stat(self):

    #     self.device.execute = Mock()
    #     self.device.execute.side_effect = self.mapper

    #     directory_output = self.fu_device.stat(
    #         file_url='bootflash:virtual-instance.conf',
    #         timeout_seconds=300, device=self.device)

    #     import pdb; pdb.set_trace()
    #     self.assertEqual(file_details['last_modified_date'], 'Mar 20 2018 10:26:01 +00:00')
    #     self.assertEqual(file_details['permissions'], '-rw-')
    #     self.assertEqual(file_details['index'], '69705')
    #     self.assertEqual(file_details['size'], '104260')

    # def test_deletefile(self):

    #     self.device.execute = Mock()
    #     self.device.execute.side_effect = self.mapper

    #     self.fu_device.deletefile(file_url='flash:memleak.tcl',
    #       timeout_seconds=300, device=self.device)

    # def test_renamefile(self):

    #     self.device.execute = Mock()
    #     self.device.execute.side_effect = self.mapper

    #     self.fu_device.renamefile(from_file_url='flash:memleak.tcl',
    #       to_file_url='new_file.tcl',
    #       timeout_seconds=300, device=self.device)

    # # TODO: Finalize after fixing the patch calls
    # @patch('..fileutils.FileUtils.validateserver.futlinux.check_file', return_value=raw6)
    # # @patch('filetransferutils.plugins.FileUtils.validateserver.futlinux.deletefile', return_value=raw7)
    # def test_validateserver(self):

    #     self.device.execute = Mock()
    #     self.device.execute.side_effect = self.mapper

    #     self.fu_device.validateserver(
    #         file_path='ftp://1.1.1.1//auto/tftp-ssr/show_clock',
    #         timeout_seconds=300, device=self.device)


if __name__ == '__main__':
    unittest.main()

# vim: ft=python et sw=4