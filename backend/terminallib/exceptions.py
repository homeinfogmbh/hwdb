"""Common exceptions."""


__all__ = [
    'TerminalError',
    'TerminalConfigError',
    'NoConnection',
    'AmbiguousSystems']


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

    def __init__(self, systems):
        """Sets the respective systems."""
        super().__init__()
        self.systems = systems

    def __iter__(self):
        """Yields the systems."""
        yield from self.systems
