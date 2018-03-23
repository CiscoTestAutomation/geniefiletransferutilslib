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
    device = Device(testbed=tb, name='aDevice', os='iosxr')

    # Instantiate a filetransferutils instance for IOSXE device
    fu_device = FileUtils.from_device(device)

    # Add testbed servers for authentication
    device.testbed.servers = AttrDict(
        server_name = dict(
            username="myuser", password="mypw", address='1.1.1.1'),
    )

    dir_output = {'dir':
        {'total_free_bytes': '938376 kbytes', 'dir_name': '/misc/scratch', 'total_bytes': '1012660 kbytes'}}


    # Mock device output
    raw1 = {'execute.return_value': '''
        copy flash:/memleak.tcl ftp://1.1.1.1//auto/tftp-ssr/memleak.tcl
        Address or name of remote host [1.1.1.1]? 
        Destination filename [/auto/tftp-ssr/memleak.tcl]? 
        !!
        104260 bytes copied in 0.396 secs (263283 bytes/sec)
    '''}

    raw2 = '''
        dir

        Directory of /misc/scratch
           32 -rw-rw-rw- 1   824 Mar  7 06:29 cvac.log
           43 -rwxr--r-- 1     0 Mar 22 08:58 fake_config_2.tcl
           41 -rw-r--r-- 1  1985 Mar 12 14:35 status_file
           13 -rw-r--r-- 1  1438 Mar  7 14:26 envoke_log
           16 -rw-r--r-- 1    98 Mar  7 06:34 oor_aware_process
         8178 drwxr-xr-x 2  4096 Mar  7 14:27 kim
         8177 drwx---r-x 2  4096 Mar  7 14:27 clihistory
           15 lrwxrwxrwx 1    12 Mar  7 14:26 config -> /misc/config
           12 drwxr-xr-x 2  4096 Mar  7 14:26 core
           14 -rw-r--r-- 1 10429 Mar  7 14:26 pnet_cfg.log
           11 drwx------ 2 16384 Mar  7 14:26 lost+found
         8179 drwxr-xr-x 8  4096 Mar  7 07:01 ztp
           42 -rw------- 1     0 Mar 20 11:08 .python-history
        16354 drwxr-xr-x 2  4096 Mar  7 07:22 nvgen_traces
        16353 drwxrwxrwx 3  4096 Mar  7 14:29 cvac

        1012660 kbytes total (938376 kbytes free)
    '''

    raw3 = {'execute.return_value': '''
        delete disk0:fake_config_2.tcl
        Delete disk0:fake_config_2.tcl[confirm]
    '''}

    raw4 = {'execute.return_value': '''
        show clock | redirect ftp://1.1.1.1//auto/tftp-ssr/show_clock
        Writing /auto/tftp-ssr/show_clock 
    '''}

    raw5 = 'INFO:ats.utils.fileutils.plugins.linux.fileutils:Retrieving details for file ftp://10.1.7.250//auto/tftp-ssr/show_clock ...'

    raw6 = 'INFO:ats.utils.fileutils.plugins.linux.fileutils:Deleting file ftp://10.1.7.250//auto/tftp-ssr/show_clock ...'

    outputs = {}
    outputs['copy disk0:/fake_config_2.tcl ftp://1.1.1.1//auto/tftp-ssr/fake_config_2.tcl'] = raw1
    outputs['dir'] = raw2
    outputs['delete disk0:fake_config.tcl'] = raw3
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
        self.fu_device.copyfile(from_file_url='disk0:/fake_config_2.tcl',
            to_file_url='ftp://1.1.1.1//auto/tftp-ssr/fake_config_2.tcl',
            timeout_seconds='300', device=self.device)

        # Delete the temp file created
        os.remove('/auto/tftp-ssr/memleak.tcl')

    def test_dir(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        directory_output = self.fu_device.dir(from_directory_url='disk0:',
            timeout_seconds=300, device=self.device)

        # Dir IOSXR parser need to bbe updated and then self.dir_output will
        # be updated as well
        self.assertEqual(directory_output, self.dir_output)

    def test_stat(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        file_details = self.fu_device.stat(file_url='disk0:memleak.tcl',
          timeout_seconds=300, device=self.device)

        # Dir IOSXR parser need to bbe updated and then below assert check will
        # be updated as well
        self.assertEqual(file_details, self.dir_output)

    def test_deletefile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.deletefile(file_url='disk0:fake_config.tcl',
          timeout_seconds=300, device=self.device)

    def test_renamefile(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        with self.assertRaisesRegex(NotImplementedError,
                "The fileutils module filetransferutils.plugins.iosxr.fileutils does not implement renamefile."):
            self.fu_device.renamefile(from_file_url='disk0:fake_config.tcl',
              to_file_url='memleak.tcl',
                timeout_seconds=300, device=self.device)

    # TODO: Finalize after fixing the patch calls
    @patch('filetransferutils.plugins.FileUtils.validateserver.futlinux.check_file', return_value=raw6)
    # @patch('filetransferutils.plugins.fileutils.FileUtils.validateserver.futlinux.deletefile', return_value=raw7)
    def test_validateserver(self):

        self.device.execute = Mock()
        self.device.execute.side_effect = self.mapper

        self.fu_device.validateserver(
            file_path='ftp://1.1.1.1//auto/tftp-ssr/show_clock',
            timeout_seconds=300, device=self.device)


if __name__ == '__main__':
    unittest.main()

# vim: ft=python et sw=4