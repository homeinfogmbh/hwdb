"""IP-related fields."""

from ipaddress import IPv4Address

from peewee import BigIntegerField


__all__ = ['LegacyIPv4AddressField']


class LegacyIPv4AddressField(BigIntegerField):
    """Legacy IPv4 address field."""

    def db_value(self, value):  # pylint: disable=R0201
        """Returns the IPv4 address's interger value or None."""
        if value is None:
            return None

        return int(value)

    def python_value(self, value):  # pylint: disable=R0201
        """Returns the IPv4 address object or None."""
        if value is None:
            return None

        return IPv4Address(value)
