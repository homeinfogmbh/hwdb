"""Virtual terminal library"""

from .abc import TerminalAware
from .db import TerminalHistory
from .remotectrl import RemoteController

__date__ = "25.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['VirtualTerminal']


class VirtualTerminal(TerminalAware):
    """Provides a virtual TTY for terminals"""

    def __init__(self, terminal):
        """Initializes remote controller"""
        super().__init__(terminal)
        self._remote = RemoteController(terminal)

    def execute(self, cmd, decode=False):
        """Executes a command"""
        hist_entry = TerminalHistory()
        hist_entry.command = cmd
        stdout, stderr, exit_code = self._remote.execute(cmd)
        hist_entry.stdout = stdout
        hist_entry.stderr = stderr
        hist_entry.exit_code = exit_code
        hist_entry.isave()
        if decode:
            try:
                stdout = stdout.decode()
            except:
                raise ValueError('Cannot decode STDOUT')
            else:
                try:
                    stderr = stderr.decode()
                except:
                    raise ValueError('Cannot decode STDERR')
        return (stdout, stderr, exit_code)
