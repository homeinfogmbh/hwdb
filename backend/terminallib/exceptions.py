"""Common exceptions."""


__all__ = [
    'TerminalError',
    'TerminalConfigError',
    'NoConnection',
    'AmbiguousSystems',
    'SystemOffline']


class TerminalError(Exception):
    """Basic exception for terminals handling."""


class TerminalConfigError(TerminalError):
    """Exception that indicated errors in the terminal configuration."""


class NoConnection(TerminalConfigError):
    """Indicated that no VPN configuration has
    been assigned to the respective terminal.
    """


class AmbiguousSystems(TerminalError):
    """Indicates that a query for a single
    terminal yielded ambiguous terminals.
    """

    def __init__(self, system, ambiguous):
        """Sets the respective systems."""
        super().__init__()
        self.system = system
        self.ambiguous = ambiguous

    def __iter__(self):
        """Yields the systems."""
        yield self.system
        yield from self.ambiguous


class SystemOffline(TerminalError):
    """Indicates that the respective system is offline."""
