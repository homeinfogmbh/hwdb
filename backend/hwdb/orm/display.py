"""Digital signage displays."""

from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField

from mdb import Address

from hwdb.orm.common import BaseModel
from hwdb.orm.system import System


__all__ = ['Display']


class Display(BaseModel):   # pylint: disable=R0903
    """A physical display out in the field."""

    address = ForeignKeyField(
        Address, null=True, column_name='address', backref='displays',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    annotation = CharField(255, null=True)
    system = ForeignKeyField(
        System, null=True, column_name='system', backref='displays',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    installed = DateTimeField(null=True)
    make = CharField(255, null=True)   # Hardware make.
    model = CharField(255, null=True)   # Hardware model.
    serial_number = CharField(255, null=True)
