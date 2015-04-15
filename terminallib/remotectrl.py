"""Library for terminal remote control"""

from homeinfolib.system import run
from .config import ssh
from .abc import TerminalAware
from tempfile import NamedTemporaryFile

__date__ = "25.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['RemoteController']


class RemoteController(TerminalAware):
    """Controls a terminal remotely"""

    @property
    def _user_host(self):
        """Returns the respective user@host string"""
        return '@'.join([ssh['USER'], str(self.terminal.ipv4addr)])

    @property
    def _identity_file(self):
        """Returns the SSH identity file argument
        with the respective identity file's path
        """
        return ' '.join(['-i', ssh['PRIVATE_KEY_TERMGR']])

    @property
    def _remote_shell(self):
        """Returns the rsync remote shell"""
        return ' '.join(['-e', '"ssh', ''.join([self._identity_file, '"'])])

    def _remote(self, cmd):
        """Makes a command remote"""
        return [ssh['SSH_BIN'], self._identity_file, self._user_host] + cmd

    def _rsync(self, src, dst):
        """Returns a"""
        return [ssh['RSYNC_BIN'], self._remote_shell,
                ':'.join([self._user_host, src]), dst]

    def execute(self, cmd):
        """Executes a certain command on a remote terminal"""
        return run(self._remote(cmd))

    def getfile(self, file):
        """Gets a file from a remote terminal"""
        with NamedTemporaryFile('wb+') as tmp:
            rsync = self._rsync(file, tmp.name)
            pr = run(rsync)
            if pr:
                tmp.seek(0)
                return tmp.read()
            else:
                return pr
