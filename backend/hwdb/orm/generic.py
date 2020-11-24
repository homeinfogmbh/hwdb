"""Table for generic hardware."""

from peewee import CharField, DecimalField, ForeignKeyField, TextField

from mdb import Customer
from peeweeplus import EnumField

from hwdb.enumerations import HardwareType
from hwdb.orm.common import BaseModel


__all__ = ['GenericHardware']


class GenericHardware(BaseModel):   # pylint: disable=R0903
    """Generic hardware table."""

    customer = ForeignKeyField(Customer, column_name='customer')
    type = EnumField(HardwareType)
    serial_number = CharField(null=True)
    dim_x = DecimalField(null=True)
    dim_y = DecimalField(null=True)
    dim_z = DecimalField(null=True)
    description = TextField(null=True)
