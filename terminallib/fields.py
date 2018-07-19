"""Command line interface utilities."""

from blessings import Terminal

from terminallib.orm import AddressUnconfiguredError

__all__ = [
    'get_annotation',
    'get_address',
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


def justify(string, size, leftbound=False):
    """Justifies the string."""

    if leftbound:
        return string[0:size].ljust(size)

    return string[0:size].rjust(size)


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

    def __call__(self, terminal):
        """Handles the given value."""
        return justify(
            self.string_for_terminal(terminal), self.max,
            leftbound=self.leftbound)

    @property
    def max(self):
        """Returns the maximum size."""
        return max(self.size, len(self.caption))

    @property
    def header(self):
        """Returns the appropriate header text."""
        return justify(self.caption, self.max, leftbound=self.leftbound)

    def string_for_terminal(self, terminal):
        """Returns the appropriate string value
        for the respective terminal record.
        """
        value = self.getter(terminal)

        if value is None:
            return '-'

        if value is True:
            return '✓'

        if value is False:
            return '✗'

        return str(value)
