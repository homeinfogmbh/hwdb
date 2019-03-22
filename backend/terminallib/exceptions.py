"""Common exceptions."""


__all__ = [
    'InvalidCommand',
    'TerminalError',
    'TerminalConfigError',
    'AmbiguousConnections',
    'NoConnection',
    'AmbiguousTerminals']


class InvalidCommand(Exception):
    """Indicates that the respective command is invalid."""


class TerminalError(Exception):
    """Basic exception for terminals handling."""


class TerminalConfigError(TerminalError):
    """Exception that indicated errors in the terminal configuration."""


class AmbiguousConnections(TerminalConfigError):
    """Indicated that no VPN configuration has
    been assigned to the respective terminal.
    """


class NoConnection(TerminalConfigError):
    """Indicated that no VPN configuration has
    been assigned to the respective terminal.
    """


class AmbiguousTerminals(TerminalError):
    """Indicates that a query for a single
    terminal yielded ambiguous terminals.
    """

    def __init__(self, message, terminals):
        """Sets message and terminals."""
        super().__init__(message)
        self.terminals = terminals
