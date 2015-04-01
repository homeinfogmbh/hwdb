"""Terminal data storage"""

from datetime import datetime
from ipaddress import IPv4Address
from peewee import ForeignKeyField, IntegerField, CharField, BigIntegerField,\
    DoesNotExist, DateTimeField, BlobField
from homeinfolib.db import improved, create, connection
from homeinfo.crm.customer import Customer
from homeinfo.crm.address import Address
from .abc import TermgrModel
from .config import net

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '10.03.2015'
__all__ = ['TermgrModel']


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


@create
@improved
class TerminalHistory(TermgrModel):
    """A virtual terminal's history"""

    class Meta:
        db_table = 'vt_history'

    terminal = ForeignKeyField(Terminal, db_column='terminal',
                               related_name='vt_log')
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


class DBEntry():
    """Manages terminal database records"""

    @classmethod
    def add(cls, cid, tid, domain=None):
        """Adds a new terminal"""
        if cls.exists(cid, tid):
            return False
        else:
            terminal = Terminal()
            terminal.customer = cid
            terminal.tid = tid
            if domain is None:
                terminal.domain = net['DOMAIN']
            else:
                terminal.domain = domain
            try:
                terminal.isave()
            except:
                return False
            else:
                return terminal

    @classmethod
    def exists(cls, cid, tid):
        """Determines whether a certain terminal exists"""
        try:
            cst = Customer.iget(Customer.id == cid)  # @UndefinedVariable
        except DoesNotExist:
            return False    # TODO: Improve error handling
        else:
            try:
                terminal = Terminal.iget(   # @UndefinedVariable
                    (Terminal.customer == cst) & (Terminal.tid == tid))
            except DoesNotExist:
                return False
            else:
                return terminal

    def delete(self):
        """Deletes the terminal"""
        pass

    def lockdown(self):
        """Lockdown terminal"""
        pass

    def unlock(self):
        """Unlock terminal"""
        pass
