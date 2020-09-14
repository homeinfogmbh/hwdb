"""Terminal deployments."""

from peewee import BooleanField
from peewee import CharField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField

from mdb import Customer, Address
from peeweeplus import EnumField

from hwdb.enumerations import Connection, Type
from hwdb.orm.common import BaseModel


__all__ = ['Deployment']


class Deployment(BaseModel):
    """A customer-specific deployment of a terminal."""

    customer = ForeignKeyField(Customer, column_name='customer')
    type = EnumField(Type)
    connection = EnumField(Connection)
    address = ForeignKeyField(Address, column_name='address')
    lpt_address = ForeignKeyField(  # Address for local public transport.
        Address, null=True, column_name='lpt_address')
    scheduled = DateField(null=True)
    annotation = CharField(255, null=True)
    testing = BooleanField(default=False)
    timestamp = DateTimeField(null=True)

    def __str__(self):
        """Returns a human readable string."""
        string = f'{self.type.value} of {self.customer.id} at {self.address}'

        if self.annotation is None:
            return string

        return f'{string} ({self.annotation})'

    def checkdupes(self):
        """Returns duplicates of this deployment in the database."""
        cls = type(self)
        condition = cls.customer == self.customer
        condition &= cls.type == self.type
        condition &= cls.connection == self.connection
        condition &= cls.address == self.address

        if self.annotation is None:
            condition &= cls.annotation >> None
        else:
            condition &= cls.annotation == self.annotation

        condition &= cls.testing == self.testing

        if self.id is not None:
            condition &= cls.id != self.id

        return cls.select().where(condition)

    def to_json(self, systems=False, **kwargs):
        """Returns a JSON-ish dict."""
        json = super().to_json(**kwargs)

        if systems:
            json['systems'] = [system.id for system in self.systems]

        return json
