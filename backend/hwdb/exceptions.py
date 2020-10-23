"""Common exceptions."""


__all__ = [
    'TerminalError',
    'TerminalConfigError',
    'NoConnection',
    'AmbiguityError',
    'RconError',
    'SystemOffline'
]


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

    def __init__(self, object, ambiguous):  # pylint: disable=W0622
        """Sets the respective systems."""
        super().__init__()
        self.object = object
        self.ambiguous = ambiguous

    def __iter__(self):
        """Yields the systems."""
        yield self.object
        yield from self.ambiguous


class RconError(TerminalError):
    """An error during remote control."""

    def __init__(self, response):
        """Sets the requests HTTP response."""
        super().__init__()
        self.response = response

    def __getattr__(self, attr):
        """Delegates to the response."""
        return getattr(self.response, attr)


class SystemOffline(TerminalError):
    """Indicates that the respective system is offline."""
