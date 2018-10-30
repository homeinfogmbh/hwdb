"""Common exceptions."""


__all__ = [
    'InvalidCommand',
    'TerminalError',
    'TerminalConfigError',
    'VPNUnconfiguredError',
    'AmbiguousTerminals']


class InvalidCommand(Exception):
    """Indicates that the respective command is invalid."""

    pass


class TerminalError(Exception):
    """Basic exception for terminals handling."""

    pass


class TerminalConfigError(TerminalError):
    """Exception that indicated errors in the terminal configuration."""

    pass


class VPNUnconfiguredError(TerminalConfigError):
    """Indicated that no VPN configuration has
    been assigned to the respective terminal.
    """

    pass


class AmbiguousTerminals(TerminalError):
    """Indicates that a query for a single
    terminal yielded ambiguous terminals.
    """

    def __init__(self, message, terminals):
        """Sets message and terminals."""
        super().__init__(message)
        self.terminals = terminals
