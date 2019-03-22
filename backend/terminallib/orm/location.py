"""Terminal locations."""

from peewee import CharField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField

from mdb import Customer, Address
from peeweeplus import CascadingFKField
from peeweeplus import EnumField

from terminallib.enumerations import Connection, Type
from terminallib.orm.common import TerminalModel


__all__ = ['Location']


class Location(TerminalModel):
    """A location for a terminal."""

    customer = CascadingFKField(Customer, column_name='customer')
    type = EnumField(Type)
    connection = EnumField(Connection)
    address = ForeignKeyField(
        Address, column_name='address', on_delete='SET NULL',
        on_update='CASCADE')
    lpt_address = ForeignKeyField(  # Address for local public transport.
        Address, null=True, column_name='lpt_address',
        on_delete='SET NULL', on_update='CASCADE')
    weather = CharField(16, null=True)
    scheduled = DateField(null=True)
    deployed = DateTimeField(null=True)
    annotation = CharField(255, null=True)

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
