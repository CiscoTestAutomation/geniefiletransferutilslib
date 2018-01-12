# Enable abstraction; This is the root package.
__import__('abstract').declare_package(__name__)

'''
Module:
    filetransferutils

Description:
    A utility package for file transfer to/from remote servers using different protocols
    (tftp/ftp/scp...etc.)

    For more detailed explanation and usages, refer to filetransferutils documentation at
    http://wwwin-pyats.cisco.com/cisco-shared/genie/latest/apidoc/filetransferutils/filetransferutils.html
'''

__version__ = '1.0.0'
__author__ = """Jean-Benoit Aubin (jeaubin@cisco.com)
                Karim Mohamed     (karmoham@cisco.com)"""
__date__ = "January 2018"
__contact__ = 'asg-genie-support@cisco.com'
__copyright__ = 'Cisco Systems, Inc. Cisco Confidential'
