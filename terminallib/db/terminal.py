"""Terminal data storage"""

from peewee import ForeignKeyField, IntegerField, CharField, BigIntegerField,\
    DoesNotExist
from ipaddress import IPv4Address
from homeinfolib.db import improved, create, connection
from homeinfo.crm.customer import Customer
from homeinfo.crm.address import Address
from .abc import TermgrModel

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '18.09.2014'
__all__ = ['Terminal']


@create
@improved
class Terminal(TermgrModel):
    """CRM's customer(s)"""

    customer = ForeignKeyField(Customer, db_column='customer',
                               related_name='terminals')
    """The customer this terminal belongs to"""
    tid = IntegerField()
    """The terminal ID"""
    domain = CharField(64)
    """The terminal's domain"""
    _ipv4addr = BigIntegerField(db_column='ipv4addr', null=True)
    """The terminal's clear-text htpasswd-password"""
    virtual_display = IntegerField(null=True)
    """Virtual display, running on the physical terminal"""
    _location = ForeignKeyField(Address, null=True, db_column='location')
    """The address of the terminal"""

    def __repr__(self):
        """Converts the terminal to a unique string"""
        return '.'.join([str(ident) for ident in self.idents])

    @classmethod
    def by_ids(cls, cid, tid):
        """Get a terminal by customer id and terminal id"""
        with connection(Customer):
            try:
                term = cls.iget((cls.customer == cid) & (cls.tid == tid))
            except DoesNotExist:
                term = None
        return term

    @property
    def cid(self):
        """Returns the customer's ID"""
        with connection(Customer):
            return self.customer.id

    @property
    def idents(self):
        """Returns the terminals identifiers"""
        return (self.tid, self.cid)

    @property
    def hostname(self):
        """Generates and returns the terminal's host name"""
        return '.'.join([str(self.tid), str(self.cid), self.domain])

    @property
    def ipv4addr(self):
        """Returns an IPv4 Address"""
        return IPv4Address(self._ipv4addr)

    @ipv4addr.setter
    def ipv4addr(self, ipv4addr):
        """Sets the IPv4 address"""
        self._ipv4addr = int(ipv4addr)

    @property
    def location(self):
        """Returns the location of the terminal"""
        with connection(Address):
            try:
                location = ', '.join([' '.join([self._location.street,
                                                self._location.house_number]),
                                      ' '.join([self._location.zip,
                                                self._location.city])])
            except:
                location = None
        return location
