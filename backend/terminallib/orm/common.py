"""Common ORM models."""

from peeweeplus import JSONModel, MySQLDatabase

from terminallib.config import CONFIG


__all__ = ['DATABASE', 'BaseModel']


DATABASE = MySQLDatabase.from_config(CONFIG['db'])


class BaseModel(JSONModel):
    """Terminal manager basic Model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database
