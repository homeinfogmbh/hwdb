"""Stakeholders on certain terminals."""

from mdb import Customer
from peeweeplus import CascadingFKField, EnumField

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
    customer = CascadingFKField(Customer, column_name='customer')
