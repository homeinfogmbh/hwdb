"""Common ORM models."""

from peeweeplus import JSONModel, MySQLDatabaseProxy


__all__ = ["DATABASE", "BaseModel"]


DATABASE = MySQLDatabaseProxy("hwdb")


class BaseModel(JSONModel):  # pylint: disable=R0903
    """Terminal manager basic Model."""

    class Meta:  # pylint: disable=C0111,R0903
        database = DATABASE
        schema = database.database
