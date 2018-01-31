# SSh class implementation
import time
import paramiko
import getpass
import logging
from scp import SCPClient

# Initialize the logger
logger = logging.getLogger(__name__)


class Ssh(object):
    '''Utils class to setup ssh and scp'''

    instances = {}

    def __init__(self, ip):
        self.ip = ip

    def setup_scp(self):

        # Check if that specific server has been connected to before or not
        if self.ip in self.instances.values():
            return

        # Create ssh connection to the server
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.ip, 22, username=getpass.getuser())
            self.scp = SCPClient(self.ssh.get_transport())
            self.sftp = self.ssh.open_sftp()
            # Sleep for connection stability
            time.sleep(1.5)
        except Exception as e:
            # As failed doesnt have from e
            logger.error(str(e))
            raise Exception("Couldn't connect to "\
                            "'{s}'".format(s=self.ip))

        self.instances[self] = self.ip
