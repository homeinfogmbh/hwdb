"""Digital signage displays."""

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField

from hwdb.orm.common import BaseModel
from hwdb.orm.deployment import Deployment
from hwdb.orm.system import System


__all__ = ['Display']


class Display(BaseModel):
    """A physical display out in the field."""

    deployment = ForeignKeyField(
        Deployment, null=True, column_name='deployment', backref='displays',
        on_delete='SET NULL', on_update='CASCADE')
    system = ForeignKeyField(
        System, null=True, column_name='system', backref='displays',
        on_delete='SET NULL', on_update='CASCADE')
    installed = DateTimeField(null=True)
    monitor = BooleanField(null=True)
    make = CharField(255, null=True)   # Hardware make.
    model = CharField(255, null=True)   # Hardware model.
    serial_number = CharField(255, null=True)
