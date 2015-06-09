"""Abstract base classes for the terminal management"""

__all__ = ['TerminalAware']


class TerminalAware():
    """Manages terminals"""

    def __init__(self, terminal):
        """Sets user name and password"""
        self._terminal = terminal

    @property
    def terminal(self):
        """Returns the terminal"""
        return self._terminal

    @property
    def cid(self):
        """Returns the respective terminal's customer's ID"""
        return self.terminal.cid

    @property
    def tid(self):
        """Returns the respective terminal's ID"""
        return self.terminal.tid

    @property
    def idstr(self):
        """Returns the identifiers string"""
        return '.'.join([str(self.tid), str(self.cid)])
