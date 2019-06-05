"""Command line interface utilities."""

from enum import Enum

from blessings import Terminal


__all__ = [
    'justify',
    'to_string',
    'DeploymentField',
    'SystemField',
    'FieldFormatter']


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


class DeploymentField(Enum):
    """Terminal field names."""

    ADDRESS = 'address'
    ANNOTATION = 'annotation'
    CONNECTION = 'connection'
    CUSTOMER = 'customer'
    ID = 'id'
    LPT_ADDRESS = 'lpt_address'
    SCHEDULED = 'scheduled'
    TESTING = 'testing'
    TYPE = 'type'
    TIMESTAMP = 'timestamp'
    WEATHER = 'weather'


class SystemField(Enum):
    """Terminal field names."""

    CONFIGURED = 'configured'
    CREATED = 'created'
    DEPLOYMENT = 'deployment'
    ID = 'id'
    MANUFACTURER = 'manufacturer'
    MODEL = 'model'
    MONITOR = 'monitor'
    ONLINE = 'online'
    OPENVPN = 'openvpn'
    OS = 'os'
    SN = 'sn'
    WIREGUARD = 'wireguard'


class FieldFormatter:
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
