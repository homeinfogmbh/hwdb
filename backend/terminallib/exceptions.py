"""Common exceptions."""


__all__ = [
    'TerminalError',
    'TerminalConfigError',
    'NoConnection',
    'AmbiguityError',
    'SystemOffline']


class TerminalError(Exception):
    """Basic exception for terminals handling."""


class TerminalConfigError(TerminalError):
    """Exception that indicated errors in the terminal configuration."""


class NoConnection(TerminalConfigError):
    """Indicated that no VPN configuration has
    been assigned to the respective terminal.
    """


class AmbiguityError(TerminalError):
    """Indicates that a query for a single
    terminal yielded ambiguous terminals.
    """

    def __init__(self, object, ambiguous):
        """Sets the respective systems."""
        super().__init__()
        self.object = object
        self.ambiguous = ambiguous

    def __iter__(self):
        """Yields the systems."""
        yield self.object
        yield from self.ambiguous


class SystemOffline(TerminalError):
    """Indicates that the respective system is offline."""
