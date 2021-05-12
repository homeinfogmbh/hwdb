"""System groups."""

from peewee import CharField

from hwdb.orm.common import BaseModel


__all__ = ['Group']


class Group(BaseModel):     # pylint: disable=R0903
    """System group."""

    name = CharField()
