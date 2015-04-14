"""Library for terminal SSH remote control"""

from .config import ssh
from homeinfolib.system import run

__date__ = "14.04.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['termexec']


def termexec(terminal, cmd, user=None):
    """Run command on terminal via ssh"""
    ssh_bin = '/usr/bin/ssh'
    identity_file = ssh['PRIVATE_KEY_TERMGR']
    user = user or 'heed'
    host = '@'.join([user, str(terminal.ipv4addr)])
    ssh_cmd = [ssh_bin, '-i', identity_file, host]
    return run(ssh_cmd + cmd)


def termget(terminal, src, dst, user=None):
    """Run command on terminal via ssh"""
    rsync_bin = '/usr/bin/rsync'
    identity_file = ssh['PRIVATE_KEY_TERMGR']
    user = user or 'heed'
    host = '@'.join([user, str(terminal.ipv4addr)])
    resource = ':'.join(host, src)
    rsync_cmd = [rsync_bin, '-e "ssh -i ' + identity_file + '"', host]
    return run(rsync_cmd + [resource] + [dst])
