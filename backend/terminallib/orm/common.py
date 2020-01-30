"""Common ORM models."""

from ipaddress import IPv4Address

from peewee import BigIntegerField

from peeweeplus import JSONModel, MySQLDatabase

from terminallib.config import CONFIG


__all__ = ['DATABASE', 'BaseModel', 'LegacyIPv4AddressField']


DATABASE = MySQLDatabase.from_config(CONFIG['Database'])


class BaseModel(JSONModel):
    """Terminal manager basic Model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database


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
