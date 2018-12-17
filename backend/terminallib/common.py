"""Abstract base classes for the terminal management."""

from logging import getLogger


__all__ = ['TerminalAware']


class TerminalAware:
    """Manages terminals."""

    def __init__(self, terminal, logger=None):
        """Sets user name and password."""
        self.terminal = terminal

        if logger is None:
            self.logger = getLogger(type(self).__name__)
        else:
            self.logger = logger.getChild(type(self).__name__)

    @property
    def idstr(self):
        """Returns the identifiers string."""
        return str(self.terminal)
