from .. import FileUtils as FileUtilsDeviceBase

class FileUtils(FileUtilsDeviceBase):

    def copyfile(self, source, destination, timeout_seconds=300, vrf=None, *args,
                 **kwargs):
        ''' Copy a file to/from linux device '''
        # update source and destination with the valid address from testbed
        source = self.validate_and_update_url(source, device=kwargs.get('device'), vrf=vrf)
        destination = self.validate_and_update_url(destination, device=kwargs.get('device'), vrf=vrf)

        used_server = self.get_server(source, destination)
        username, _ = self.get_auth(used_server)
        ssh_protocol = {'scp', 'sftp'}

        # if protocol is scp or sftp
        # sftp only support download
        for protocol in ssh_protocol:
            if '{}:'.format(protocol) in source or '{}:'.format(protocol) in destination:
                # scp/sftp requires username in the address
                if '{}:'.format(protocol) in source:
                    source = '{username}@{url}'.format(username=username, url=source)
                elif '{}:'.format(protocol) in destination:
                    destination = '{username}@{url}'.format(username=username, url=destination)

                cmd = '{protocol} {s} {d}'.format(protocol=protocol,
                                                  s=source.replace('{}://'.format(protocol), '').replace('//', ':/'),
                                                  d=destination.replace('{}://'.format(protocol), '').replace('//', ':/'))
                break

        else:
            raise NotImplementedError('Only SFTP and SCP protocols are supported for linux')

        super().copyfile(source=source, destination=destination,
            timeout_seconds=timeout_seconds, cmd=cmd, used_server=used_server,
            *args, **kwargs)