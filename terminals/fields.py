"""Command line interface utilities."""

from strflib import Shell
from homeinfo.terminals.orm import AddressUnconfiguredError

__all__ = [
    'get_annotation',
    'get_address',
    'stringify',
    'justify',
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


def stringify(value):
    """Returns the string representation of the value."""

    if value is None:
        return '–'
    elif value is True:
        return '✓'
    elif value is False:
        return '✗'

    return str(value)


def justify(string, size, leftbound=False):
    """Justifies the string."""

    if leftbound:
        return string[0:size].ljust(size)

    return string[0:size].rjust(size)


class TerminalField():
    """Wrapper to access terminal properties."""

    def __init__(self, getter, caption, size=0, leftbound=False):
        """Sets the field's name"""
        self.getter = getter
        self.caption = caption
        self._size = size
        self.leftbound = leftbound

    def __str__(self):
        """Returns the formatted caption."""
        return Shell.bold(repr(self))

    def __repr__(self):
        """Returns the justified caption."""
        return justify(self.caption, self.spacing, leftbound=self.leftbound)

    def __call__(self, terminal):
        """Handles the given value."""
        value = self.getter(terminal)
        string = stringify(value)
        return justify(string, self.spacing, leftbound=self.leftbound)

    @property
    def size(self):
        """Returns the required spacing."""
        return max(self._size, len(self.caption))
