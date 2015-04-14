"""Terminal data storage"""

from datetime import datetime
from ipaddress import IPv4Address
from peewee import ForeignKeyField, IntegerField, CharField, BigIntegerField,\
    DoesNotExist, DateTimeField, BlobField, BooleanField
from homeinfolib.db import create, connection
from homeinfolib.lib import classproperty
from homeinfo.crm.customer import Customer
from homeinfo.crm.address import Address
from .abc import TermgrModel

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '10.03.2015'
__all__ = ['Domain', 'Class', 'Terminal', 'Screenshot', 'ConsoleHistory']


@create
class Class(TermgrModel):
    """Terminal classes"""

    name = CharField(32)
    """The class' name"""
    touch = BooleanField()
    """Flag, whether it is a touch-display class"""


@create
class Domain(TermgrModel):
    """Terminal domains"""

    _fqdn = CharField(32, db_column='fqdn')

    @property
    def fqdn(self):
        """Returns the FQDN"""
        return self._fqdn

    @fqdn.setter
    def fqdn(self, fqdn):
        """Sets the FQDN"""
        if fqdn.endswith('.'):
            self.fqdn = fqdn
        else:
            raise ValueError(' '.join(['Not a FQDN:', fqdn]))

    @property
    def name(self):
        """Returns the domain name without trailing '.'"""
        return self._fqdn[:-1]


@create
class Terminal(TermgrModel):
    """A physical terminal out in the field"""

    customer = ForeignKeyField(Customer, db_column='customer',
                               related_name='terminals')
    """The customer this terminal belongs to"""
    tid = IntegerField()
    """The terminal ID"""
    _cls = ForeignKeyField(Class, db_column='cls', related_name='terminals')
    """The terminal's class"""
    _domain = ForeignKeyField(Domain, db_column='domain',
                              related_name='terminals')
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

    @classmethod
    def used_tids(cls, cid):
        """Yields used terminal IDs for a certain customer"""
        with connection(Customer):
            for terminal in cls.iselect(cls.customer == cid):
                yield terminal.tid

    @classproperty
    @classmethod
    def used_ipv4addr(cls):
        """Yields used IPv4 addresses"""
        for terminal in cls.iselect(True):
            yield terminal.ipv4addr

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
        return '.'.join([str(self.tid), str(self.cid), self.domain.name])

    @property
    def ipv4addr(self):
        """Returns an IPv4 Address"""
        return IPv4Address(self._ipv4addr)

    @ipv4addr.setter
    def ipv4addr(self, ipv4addr):
        """Sets the IPv4 address"""
        self._ipv4addr = int(ipv4addr)

    @property
    def cls(self):
        """Returns the terminal's class"""
        with connection(Domain):
            return self._cls

    @property
    def domain(self):
        """Returns the domain"""
        with connection(Domain):
            return self._domain

    @property
    def location(self):
        """Returns the location of the terminal"""
        with connection(Address):
            location = self._location
        return location

    @property
    def address(self):
        location = self.location
        try:
            street_houseno = ' '.join([location.street, location.house_number])
        except (TypeError, ValueError):
            return None
        else:
            try:
                zip_city = ' '.join([location.zip_code, location.city])
            except (TypeError, ValueError):
                return None
            else:
                return ', '.join([street_houseno, zip_city])


@create
class Screenshot(TermgrModel):
    """Terminal screenshots"""

    terminal = ForeignKeyField(Terminal, db_column='terminal',
                               related_name='screenshots')
    """The terminal, the screenshot has been taken from"""
    screenshot = BlobField()
    """The actual screenshot data"""
    thumbnail = BlobField()
    """A smaller preview of the screenshot"""
    date = DateTimeField(default=datetime.now())
    """The date and time when the screenshot has been taken"""


@create
class ConsoleHistory(TermgrModel):
    """A physical terminal's virtual console's history"""

    class Meta:
        db_table = 'console_history'

    terminal = ForeignKeyField(Terminal, db_column='terminal',
                               related_name='console_log')
    """The terminal this history belongs to"""
    timestamp = DateTimeField(default=datetime.now())
    """A time stamp when the command was executed"""
    command = CharField(255)
    """The command, that was issued"""
    stdout = BlobField()
    """The STDOUT result of the command"""
    stderr = BlobField()
    """The STDERR result of the command"""
    exit_code = IntegerField()
    """The exit code of the command"""
