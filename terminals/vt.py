"""Virtual terminal library"""

from .abc import TerminalAware
from .db import ConsoleHistory
from .remotectrl import RemoteController

__all__ = ['VirtualTerminal']


class VirtualTerminal(TerminalAware):
    """Provides a virtual TTY for terminals"""

    def __init__(self, terminal):
        """Initializes remote controller"""
        super().__init__(terminal)
        self._remote = RemoteController(terminal)

    def execute(self, cmd):
        """Executes a command"""
        hist_entry = ConsoleHistory()
        hist_entry.command = cmd
        pr = self._remote.execute(cmd)
        hist_entry.stdout = pr.stdout
        hist_entry.stderr = pr.stderr
        hist_entry.exit_code = pr.exit_code
        hist_entry.isave()
        return pr
