"""Stakeholders on certain terminals."""

from peewee import ForeignKeyField

from mdb import Customer
from peeweeplus import EnumField

from terminallib.enumerations import Type
from terminallib.orm.common import BaseModel


__all__ = ['TypeStakeholder']


class TypeStakeholder(BaseModel):
    """Mappings of customers that have access
    to terminals of certain types.
    """

    class Meta:     # pylint: disable=C0111,R0903
        table_name = 'type_stakeholder'

    type = EnumField(Type)
    stakeholder = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE',
        on_update='CASCADE')
