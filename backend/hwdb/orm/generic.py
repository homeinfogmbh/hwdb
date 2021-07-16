"""Table for generic hardware."""

from peewee import CharField
from peewee import DecimalField
from peewee import ForeignKeyField
from peewee import ModelSelect
from peewee import TextField

from mdb import Company, Customer
from peeweeplus import EnumField

from hwdb.enumerations import HardwareType
from hwdb.orm.common import BaseModel


__all__ = ['GenericHardware']


class GenericHardware(BaseModel):   # pylint: disable=R0903
    """Generic hardware table."""

    class Meta:     # pylint: disable=R0903,C0115
        table_name = 'generic_hardware'

    customer = ForeignKeyField(
        Customer, column_name='customer', lazy_load=False)
    type = EnumField(HardwareType)
    serial_number = CharField(null=True)
    dim_x = DecimalField(null=True)
    dim_y = DecimalField(null=True)
    dim_z = DecimalField(null=True)
    description = TextField(null=True)

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects generic hardware."""
        if not cascade:
            return super().select(*args, **kwargs)

        args = {cls, Customer, Company, *args}
        return super().select(*args, **kwargs).join(Customer).join(Company)
