"""Terminal deployments."""

from xml.etree.ElementTree import Element, SubElement

from peewee import JOIN
from peewee import BooleanField
from peewee import CharField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import ModelSelect

from mdb import Address, Company, Customer
from peeweeplus import EnumField

from hwdb.enumerations import Connection, DeploymentType
from hwdb.orm.common import BaseModel


__all__ = ['Deployment']


HTML_HEADERS = ('ID', 'Customer', 'Type', 'Address')


class Deployment(BaseModel):
    """A customer-specific deployment of a terminal."""

    customer = ForeignKeyField(
        Customer, column_name='customer', lazy_load=False)
    type = EnumField(DeploymentType)
    connection = EnumField(Connection)
    address = ForeignKeyField(Address, column_name='address', lazy_load=False)
    lpt_address = ForeignKeyField(  # Address for local public transport.
        Address, null=True, column_name='lpt_address', lazy_load=False)
    scheduled = DateField(null=True)
    annotation = CharField(255, null=True)
    testing = BooleanField(default=False)
    timestamp = DateTimeField(null=True)

    def __str__(self):
        """Returns a human readable string."""
        string = f'{self.type.value} of {self.customer_id} at {self.address}'

        if self.annotation is None:
            return string

        return f'{string} ({self.annotation})'

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects deployments."""
        if not cascade:
            return super().select(*args, **kwargs)

        lpt_address = Address.alias()
        args = {cls, Customer, Company, Address, lpt_address, *args}
        return super().select(*args, **kwargs).join(
            Customer).join(Company).join_from(
            cls, Address, on=cls.address == Address.id).join_from(
            cls, lpt_address, on=cls.lpt_address == lpt_address.id,
            join_type=JOIN.LEFT_OUTER)

    def checkdupes(self) -> ModelSelect:
        """Returns duplicates of this deployment in the database."""
        cls = type(self)
        condition = cls.customer == self.customer
        condition &= cls.type == self.type
        condition &= cls.connection == self.connection
        condition &= cls.address == self.address
        condition &= cls.testing == self.testing

        if self.annotation is None:
            condition &= cls.annotation >> None
        else:
            condition &= cls.annotation == self.annotation

        if self.id is not None:
            condition &= cls.id != self.id

        return cls.select().where(condition)

    def to_html(self, border: bool = True) -> Element:
        """Returns an HTML table."""
        table = Element('table', attrib={'border': '1' if border else '0'})
        header_row = SubElement(table, 'tr')

        for header in HTML_HEADERS:
            header_col = SubElement(header_row, 'th')
            header_col.text = header

        value_row = SubElement(table, 'tr')
        id_col = SubElement(value_row, 'td')
        id_col.text = str(self.id)
        customer_col = SubElement(value_row, 'td')
        customer_col.text = str(self.customer)
        type_col = SubElement(value_row, 'td')
        type_col.text = self.type.value
        address_col = SubElement(value_row, 'td')
        address_col.text = str(self.address)
        return table

    def to_json(self, address: bool = False, customer: bool = False,
                systems: bool = False, **kwargs) -> dict:
        """Returns a JSON-ish dict."""
        json = super().to_json(**kwargs)

        if address:
            json['address'] = self.address.to_json()

            if self.lpt_address is not None:
                json['lptAddress'] = self.lpt_address.to_json()

        if customer:
            json['customer'] = self.customer.to_json()

        if systems:
            json['systems'] = [system.id for system in self.systems]

        return json
