'''
Tftp implmentation

'''
import re
import os
import time
import getpass
import logging
import datetime

#import filehelper
from ..filehelper import FileHelper

# Unicon
from unicon.eal.dialogs import Statement, Dialog

# Initialize the logger
logger = logging.getLogger(__name__)


class Utils(object):
    ''' Utilities class for Tftp

    Class is containing utility functions for a tftp server. The same instance
    can be used by multiples devices, as each device is an argument passed in
    all the methods.

    Args:
        ip (`str`): Tftp IP address
        server (`str`): Tftp server name
        directory (`str`): tftp directory

    Examples:

        >>> tftp = TFTPUtils(scp=<scp object>,
        ...                  directory = '/tftpboot')
    '''

    def __init__(self, scp, directory, *args, **kwargs):
        self.scp = scp
        self.directory = directory

    def copy_file_to_device(self, device, filename, location, invalid,
                            vrf='management', cmd=None, delay=1, tries=1,
                            **kwargs):
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

        # First copy the file to the tftpdir location
        # Generate a new name
        # Get file + datetime
        if 'temp_filename' not in kwargs:
            name = os.path.basename(filename)
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H_%M_%S')
            temp_name = '{n}-{d}'.format(n=name, d=timestamp)
            temp_filename  = os.path.join(self.directory, temp_name)
        else:
            temp_filename = kwargs['temp_filename']

        # Give a few attempts
        excep = None
        for _ in range(5):
            try:
                # Now ready to do the copy
                self.scp.scp.put(filename, temp_filename)
            except Exception as e:
                # Keep first exception seen
                if excep is None:
                    excep = e
                continue
            else:
                break
        else:
            # No break, hence exception
            logger.error(str(excep))
            raise Exception("Issue scp'ing '{f}' "
                            "to '{s}'".format(f=filename,
                                              s=self.scp.ip))

        # This is assuming we still have access to the file from that location
        # If no, we need to use ssh to verify if it is.
        remote = False
        if not FileHelper.check_file(file=temp_filename, tries=tries, delay=delay):
            remote = True
            if not FileHelper.check_file(file=temp_filename, tries=tries, delay=delay,
                                         ssh=self.scp):
                raise Exception("File does not exists at location '{f}' "
                                "on server '{s}'".format(f=temp_filename,
                                                         s=self.scp.ip))

        # Build up the command
        if cmd is None:
            if vrf:
                cmd = "copy tftp://{ip}/{file} {location} vrf {vrf}"\
                       .format(ip=self.scp.ip, location=location, file=temp_filename,
                               vrf=vrf)
            else:
                cmd = "copy tftp://{ip}/{file} {location}"\
                       .format(ip=self.scp.ip, location=location, file=temp_filename)
        else:
            cmd = cmd.format(ip=self.scp.ip, location=location,
                             file=temp_filename, vrf=vrf)

        # Send it to the device
        # If it error out,  let it be; Script need to handle it
        if device.os == 'iosxr':
            self._configure_cli_on_device(device=device, cli=cmd,
                                          invalid=invalid)
        else:
            self._send_cli_to_device(device=device, cli=cmd, invalid=invalid)

        # Delete the temp file
        if remote:
            self.scp.sftp.remove(temp_filename)
        else:
            os.remove(temp_filename)
        return os.path.basename(temp_filename)

    def save_output(self, device, filename, cli, vrf='management', tries=1,
                    delay=1, cmd=None):
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

        # Could be passed via inherited abstract
        file = os.path.join(self.directory, filename)
        if cmd is None:
            if vrf:
                cmd = "{cli} > tftp://{ip}/{file} vrf {vrf}"\
                       .format(cli=cli, ip=self.scp.ip, file=file, vrf=vrf)
            else:
                cmd = "{cli} > tftp://{ip}/{file}"\
                       .format(cli=cli, ip=self.scp.ip, file=file)

        # Send it to the device
        # If it error out,  let it be; Script need to handle it
        self._send_cli_to_device(device=device, cli=cmd)

        # TODO : Need to find nice way to send tries/delay
        if FileHelper.check_file(file=file, tries=tries, delay=delay):
            logger.info('Configuration of the device has been saved to file '
                        '{filename}'.format(filename=filename))
        else:
            # try via ssh 
            if FileHelper.check_file(file=file, tries=tries, delay=delay,
                                     ssh=self.scp):
                logger.info('Configuration of the device has been saved to file'
                            ' {filename}'.format(filename=filename))
            else:
                raise FileNotFoundError('Configuration of the device has not '
                                        'saved to {filename}'\
                                        .format(filename=filename))

    def save_core(self, device, location, core, vrf=None, tries=1, delay=1,
                  cmd=None, timeout=None, invalid=None, **kwargs):
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
        if not invalid:
            invalid=[]

        # Could be passed via inherited abstract
        if 'file' not in kwargs:
            file = os.path.join(self.directory, core)
        else:
            file = kwargs['file']

        if not cmd:
            cmd = 'copy {location}/{core} ' \
                  'tftp://{ip}/{file}'.\
                  format(location=location, core=core, ip=self.scp.ip,
                         file=file)
            if vrf:
                cmd += ' vrf {}'.format(vrf)

        # Send it to the device
        # If it error out,  let it be; Script need to handle it
        try:
            self._send_cli_to_device(device=device, cli=cmd, invalid=invalid,
                timeout=timeout, **kwargs)
        except Exception as e:
            raise Exception(e)

    def basic_check(self, device, vrf='management', **kwargs):
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
        logger.info('Verifying if TFTP can be reached and if a temp file can '
                    'be created')

        # prepare the temp file name
        if 'file' not in kwargs:
            filename = '.'.join([device.name, time.strftime("%Y-%m-%d.%H.%M.%S",
                                                           time.localtime())])
            # Add base + newly generated file name
            file = os.path.join(self.directory, filename)
        else:
            file = kwargs['file']            

        # Patch up the command together
        if 'cli' not in kwargs:
            cli = "show clock > tftp://{ip}/{file} vrf {vrf}"\
                    .format(ip=self.scp.ip, file=file, vrf=vrf)
        else:
            cli = kwargs['cli']

        # Send the command
        try:
            self._send_cli_to_device(device=device, cli=cli)
        except Exception as e:
            # oops, it failed
            # Re-raise and add our message
            raise type(e)('TFTP server is unreachable') from e

        # Let's verify the file is there
        # TODO Nice way to pass tries + delay
        if not FileHelper.check_file(file=file):
            raise FileNotFoundError('Even though the cli was send correctly '
                                     'to the device, {file} was not '
                                     'created'.format(file=file))

        # In the future, might need to use a ssh method to delete it
        # But most likely no need
        os.remove(file)

        # Great success!
        logger.info("Tftp is ready to be used")

    def _send_cli_to_device(self, device, cli, invalid=None, timeout=300, **kwargs):
        ''' Send command to a particular device and deal with its result '''

        if 'username' in kwargs and 'password' in kwargs:
            username=kwargs['username']
            password=kwargs['password']
        else:
            username = None
            password = None

        # Create unicon dialog
        dialog = Dialog([
            Statement(pattern=r'Address or name of remote host.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination filename.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'\[confirm\]',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination username:.*',
                      action='sendline({username})'.format(username=username),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination password:.*',
                      action='sendline({password})'.format(password=password),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Destination filename.*',
                      action='sendline()',
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Enter username:',
                      action='sendline({username})'.format(username=username),
                      loop_continue=True,
                      continue_timer=False),
            Statement(pattern=r'Password:',
                      action='sendline({password})'.format(password=password),
                      loop_continue=True,
                      continue_timer=False),
            ])

        try:
            output = device.execute(cli, timeout=timeout, reply=dialog)
            # Todo: better way to filter out the errors
            # Might need dynamic, so this can be controlled via that common cfg file
            fail_msg = ['failed to copy', 'Unable to find', 'Error opening',\
                'Error', 'operation failed']
            if invalid:
                fail_msg.extend(invalid)
            for word in fail_msg:
                if word in output:
                    raise ValueError('Tftp operation failed with the following '
                                     'reason: {line}'.format(line=word))
        except Exception as e:
            raise type(e)('{}'.format(e))
