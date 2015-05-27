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
