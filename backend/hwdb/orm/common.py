"""Common ORM models."""

from peeweeplus import JSONModel, MySQLDatabase

from hwdb.config import CONFIG


__all__ = ['DATABASE', 'BaseModel']


DATABASE = MySQLDatabase.from_config(CONFIG['Database'])


class BaseModel(JSONModel):     # pylint: disable=R0903
    """Terminal manager basic Model."""

    class Meta:     # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database
