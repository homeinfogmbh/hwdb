"""Abstract base classes for the terminal management"""

from fancylog import LoggingClass

__all__ = ['TerminalAware']


class TerminalAware(LoggingClass):
    """Manages terminals"""

    def __init__(self, terminal, logger=None, debug=False):
        """Sets user name and password"""
        super().__init__(logger=logger, debug=debug)
        self.terminal = terminal

    @property
    def idstr(self):
        """Returns the identifiers string"""
        return str(self.terminal)
