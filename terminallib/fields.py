"""Command line interface utilities."""

from blessings import Terminal

from terminallib.orm import AddressUnconfiguredError

__all__ = [
    'get_annotation',
    'get_address',
    'justify',
    'to_string',
    'TerminalField']


def get_annotation(terminal):
    """Returns the terminal's address annotation."""

    location = terminal.location

    if location is not None:
        return location.annotation

    return None


def get_address(terminal):
    """Returns the terminal's address."""

    try:
        return terminal.address
    except AddressUnconfiguredError:
        return 'N/A'


def justify(string, size, leftbound=False):
    """Justifies the string."""

    if leftbound:
        return string[0:size].ljust(size)

    return string[0:size].rjust(size)


def to_string(value, none='-', true='✓', false='✗'):
    """Applies builtin str() to value unless value is None, True or
    False, in which case it will return none, true respectively false
    from the keyword arguments.
    """

    if value is None:
        return none

    if value is True:
        return true

    if value is False:
        return false

    return str(value)


class TerminalField:
    """Wrapper to access terminal properties."""

    def __init__(self, getter, caption, size=0, leftbound=False):
        """Sets the field's name"""
        self.getter = getter
        self.caption = caption
        self.size = size
        self.leftbound = leftbound

    def __str__(self):
        """Returns the formatted caption."""
        return Terminal().bold(self.header)

    def format(self, terminal):
        """Formats the respective field of the given terminal record."""
        return justify(
            to_string(self.getter(terminal)), self.max,
            leftbound=self.leftbound)

    @property
    def max(self):
        """Returns the maximum size."""
        return max(self.size, len(self.caption))

    @property
    def header(self):
        """Returns the appropriate header text."""
        return justify(self.caption, self.max, leftbound=self.leftbound)
