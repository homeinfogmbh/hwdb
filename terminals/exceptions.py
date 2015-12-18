"""Exceptions"""

__all__ = ['TerminalError', 'TerminalConfigError', 'VPNUnconfiguredError']


class TerminalError(Exception):
    """Basic exception for terminals handling"""

    pass


class TerminalConfigError(TerminalError):
    """Exception that indicated errors in the terminal configuration"""

    pass


class VPNUnconfiguredError(TerminalConfigError):
    """Indicated that not VPN configuration has
    been assigned to the respective terminal
    """

    pass
