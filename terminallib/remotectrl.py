"""Library for terminal remote control"""

from .config import ssh
from .abc import TerminalAware
from subprocess import Popen, PIPE

__date__ = "25.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['RemoteController']


class RemoteController(TerminalAware):
    """Controls a terminal remotely"""

    def _remote(self, cmd):
        """Makes a command remote"""
        user_host = '@'.join([ssh['USER'], str(self.terminal.ipv4addr)])
        ssh = [ssh['BINARY'], user_host]
        return ssh + cmd

    def _execute(self, cmd):
        """Actually execute a command"""
        with Popen(cmd, stdout=PIPE, sterr=PIPE) as process:
            stdout, stderr = process.communicate()
            exit_code = process.wait()
        return (stdout, stderr, exit_code)

    def execute(self, cmd):
        """Executes a certain command"""
        cmd_lst = [i.strip() for i in cmd.split() if i.strip()]
        if self._verify(cmd_lst):
            return self._execute(self._remote(cmd_lst))
        else:
            pass    # TODO: Raise error
