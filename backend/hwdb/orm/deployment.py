"""Terminal deployments."""

from datetime import datetime
from xml.etree.ElementTree import Element, SubElement

from peewee import JOIN
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import Select
from peewee import TextField

import urllib.parse

from mdb import Address, Company, Customer
from peeweeplus import EnumField, HTMLTextField


from hwdb.enumerations import Connection, DeploymentType
from hwdb.orm.common import BaseModel
from deployments.functions import password_encrypt
from configlib import load_config

__all__ = ["Deployment", "DeploymentTemp"]


HTML_HEADERS = ("ID", "Customer", "Type", "Address")


class Deployment(BaseModel):
    """A customer-specific deployment of a terminal."""

    customer = ForeignKeyField(
        Customer, column_name="customer", on_delete="CASCADE", lazy_load=False
    )
    type = EnumField(DeploymentType)
    connection = EnumField(Connection)
    address = ForeignKeyField(Address, column_name="address", lazy_load=False)
    lpt_address = ForeignKeyField(  # Address for local public transport.
        Address, null=True, column_name="lpt_address", lazy_load=False
    )
    annotation = CharField(255, null=True)
    testing = BooleanField(default=False)
    processing = BooleanField(default=False)
    created = DateTimeField(default=datetime.now, null=True)
    url = TextField(default=None)
    # Checklist
    construction_site_preparation_feedback = DateTimeField(null=True)
    internet_connection = DateTimeField(null=True)
    technician_annotation = HTMLTextField(null=True)

    def __str__(self):
        """Returns a human-readable string."""
        string = f"{self.type.value} of {self.customer_id} at {self.address}"

        if self.annotation is None:
            return string

        return f"{string} ({self.annotation})"

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects deployments."""
        if not cascade:
            return super().select(*args)

        lpt_address = Address.alias()
        system = cls.systems.rel_model
        return (
            super()
            .select(cls, Customer, Company, Address, lpt_address, *args)
            .join(Customer)
            .join(Company)
            .join_from(cls, Address, on=cls.address == Address.id)
            .join_from(
                cls,
                lpt_address,
                on=cls.lpt_address == lpt_address.id,
                join_type=JOIN.LEFT_OUTER,
            )
            .join_from(
                cls, system, on=system.deployment == cls.id, join_type=JOIN.LEFT_OUTER
            )
            .distinct()
        )

    @property
    def prepared(self) -> bool:
        """Returns True iff the deployment is considered prepared for usage."""
        return (
            self.construction_site_preparation_feedback is not None
            and self.internet_connection is not None
        )

    def checkdupes(self) -> Select:
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
        table = Element("table", attrib={"border": "1" if border else "0"})
        header_row = SubElement(table, "tr")

        for header in HTML_HEADERS:
            header_col = SubElement(header_row, "th")
            header_col.text = header

        value_row = SubElement(table, "tr")
        id_col = SubElement(value_row, "td")
        id_col.text = str(self.id)
        customer_col = SubElement(value_row, "td")
        customer_col.text = str(self.customer)
        type_col = SubElement(value_row, "td")
        type_col.text = self.type.value
        address_col = SubElement(value_row, "td")
        address_col.text = str(self.address)
        return table

    def to_json(
        self,
        *,
        address: bool = False,
        customer: bool = False,
        systems: bool = False,
        **kwargs,
    ) -> dict:
        """Returns a JSON-ish dict."""
        json = super().to_json(**kwargs)

        if address:
            json["address"] = self.address.to_json()

            if self.lpt_address is not None:
                json["lptAddress"] = self.lpt_address.to_json()

        if customer:
            json["customer"] = self.customer.to_json()

        if systems:
            json["systems"] = [system.id for system in self.systems]

        return json


class DeploymentTemp(Deployment):
    """Temporary deployment table for newly added deployments that need confirmation"""

    def to_json(
        self,
        *,
        address: bool = False,
        customer: bool = False,
        systems: bool = False,
        **kwargs,
    ) -> dict:
        """Returns a JSON-ish dict."""
        json = super().to_json(
            address=address, customer=customer, systems=systems, **kwargs
        )
        password = load_config("sysmon.conf").get("mailing", "encryptionpassword")
        message = str(self.id)
        encrypted_id = password_encrypt(message.encode(), password)
        json["confirm"] = (
            "https://backend.homeinfo.de/deployments/confirm/"
            + urllib.parse.quote_plus(encrypted_id)
        )
        return json
