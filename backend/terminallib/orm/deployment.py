"""Terminal deployments."""

from peewee import BooleanField
from peewee import CharField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField

from mdb import Customer, Address
from peeweeplus import EnumField

from terminallib.enumerations import Connection, Type
from terminallib.orm.common import BaseModel


__all__ = ['Deployment']


class Deployment(BaseModel):
    """A customer-specific deployment of a terminal."""

    customer = ForeignKeyField(Customer, column_name='customer')
    type = EnumField(Type)
    connection = EnumField(Connection)
    address = ForeignKeyField(Address, column_name='address')
    lpt_address = ForeignKeyField(  # Address for local public transport.
        Address, null=True, column_name='lpt_address')
    weather = CharField(16, null=True)
    scheduled = DateField(null=True)
    annotation = CharField(255, null=True)
    testing = BooleanField(default=False)
    timestamp = DateTimeField(null=True)

    def __str__(self):
        """Returns a human readable string."""
        return '{} of {} at {}'.format(
            self.type, self.customer.id, self.address)

    def to_json(self, cascade=True, **kwargs):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_json(**kwargs)

        if cascade:
            dictionary['customer'] = self.customer.to_json(company=True)
            dictionary['address'] = self.address.to_json()
        else:
            dictionary['customer'] = self.customer_id
            dictionary['address'] = self.address_id

        if self.lpt_address is not None:
            if cascade:
                dictionary['lpt_address'] = self.lpt_address.to_json()
            else:
                dictionary['lpt_address'] = self.lpt_address_id

        return dictionary
