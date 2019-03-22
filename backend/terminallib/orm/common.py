"""Common ORM models."""

from peeweeplus import JSONModel, MySQLDatabase

from terminallib.config import CONFIG


__all__ = ['DATABASE', 'TerminalModel']


DATABASE = MySQLDatabase.from_config(CONFIG['terminalsdb'])


class TerminalModel(JSONModel):
    """Terminal manager basic Model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database
