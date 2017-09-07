"""Command line interface utilities."""

from strflib import Shell
from homeinfo.terminals.orm import AddressUnconfiguredError

__all__ = ['get_annotation', 'get_address', 'stringify', 'TerminalField']


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


class TerminalField():
    """Wrapper to access terminal properties."""

    TEMPLATE = '{{: {1}{0}.{0}}}'

    def __init__(self, getter, caption, size=0, leftbound=False):
        """Sets the field's name"""
        self.getter = getter
        self.caption = caption
        self.size = size
        self.leftbound = leftbound

    def __str__(self):
        """Returns the formatted caption."""
        return Shell.bold(self.template.format(self.caption))

    def __call__(self, terminal):
        """Handles the given value."""
        return self.template.format(stringify(self.getter(terminal)))

    @property
    def spacing(self):
        """Returns the required spacing."""
        return max(self.size, len(self.caption))

    @property
    def template(self):
        """Returns the pre-formatted template."""
        return self.TEMPLATE.format(
            self.spacing, '<' if self.leftbound else '>')
