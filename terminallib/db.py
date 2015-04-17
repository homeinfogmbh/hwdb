"""Terminal data storage"""

from os.path import isfile, join
from datetime import datetime
from ipaddress import IPv4Address, AddressValueError
from peewee import ForeignKeyField, IntegerField, CharField, BigIntegerField,\
    DoesNotExist, DateTimeField, BlobField, BooleanField
from homeinfolib.db import create, connection
from homeinfolib.lib import classproperty
from homeinfolib.system import run
from homeinfo.crm.customer import Customer
from homeinfo.crm.address import Address
from .abc import TermgrModel
from .config import net, openvpn
from homeinfo.crm.company import Company
from itertools import chain

__author__ = 'Richard Neumann <r.neumann@homeinfo.de>'
__date__ = '10.03.2015'
__all__ = ['Domain', 'Class', 'Terminal', 'Screenshot', 'ConsoleHistory',
           'Administrator', 'SetupOperator']


@create
class Class(TermgrModel):
    """Terminal classes"""

    name = CharField(32)
    """The class' name"""
    touch = BooleanField()
    """Flag, whether it is a class with touch-display"""

    @classmethod
    def add(cls, class_id, class_name, touch=False):
        """Adds a terminal class"""
        try:
            new_class = cls.iget(  # @UndefinedVariable
                (cls.name == class_name) & (cls.touch == touch))
        except DoesNotExist:
            new_class = cls()
            new_class.name = class_name
            new_class.touch = True if touch else False
            new_class.isave()
        finally:
            return new_class


@create
class Domain(TermgrModel):
    """Terminal domains"""

    _fqdn = CharField(32, db_column='fqdn')

    @classmethod
    def add(cls, fqdn):
        """Adds a domain with a certain FQDN"""
        try:
            domain = cls.iget(cls._fqdn == fqdn)  # @UndefinedVariable
        except DoesNotExist:
            domain = cls()
            domain.fqdn = fqdn
            domain.isave()
        finally:
            return domain

    @property
    def fqdn(self):
        """Returns the FQDN"""
        return self._fqdn

    @fqdn.setter
    def fqdn(self, fqdn):
        """Sets the FQDN"""
        if fqdn.endswith('.') and not fqdn.startswith('.'):
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

    @classproperty
    @classmethod
    def used_ipv4addr(cls):
        """Yields used IPv4 addresses"""
        for terminal in cls.iselect(True):
            yield terminal.ipv4addr

    @classproperty
    @classmethod
    def hosts(cls):
        """Yields entries for /etc/hosts"""
        for terminal in cls.iselect(True):
            yield '\t'.join([str(terminal.ipv4addr), terminal.hostname])

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

    @classmethod
    def gen_ipv4addr(cls, desired=None):
        """Generates a unique IPv4 address for the terminal"""
        if desired is None:
            net_base = net['IPV4NET']
            ipv4addr_base = IPv4Address(net_base)
            # Skip first 10 IP Addresses
            ipv4addr = ipv4addr_base + 10
            while ipv4addr in cls.used_ipv4addr:
                ipv4addr += 1
            # TODO: Catch IP address overflow and check
            # whether IP address is within the network
            return ipv4addr
        else:
            try:
                ipv4addr = IPv4Address(desired)
            except AddressValueError:
                raise ValueError(' '.join(['Not and IPv4 address:',
                                           str(desired)])) from None
            else:
                if ipv4addr not in cls.used_ipv4addr:
                    return ipv4addr
                else:
                    return cls.gen_ip_addr(desired=None)

    @classmethod
    def gen_tid(cls, cid, desired=None):
        """Gets a unique terminal ID for the customer"""
        if desired is None:
            tid = 1
            while tid in cls.used_tids(cid):
                tid += 1
            return tid
        else:
            if tid in cls.used_tids(cid):
                return cls.gen_tid(cid, desired=None)
            else:
                return tid

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

    @property
    def operators(self):
        """Yields the operators, which are
        allowed to setup the terminal
        """
        return SetupOperatorTerminals.operators(self)

    @property
    def administrators(self):
        """Yields the administrators, which are
        allowed to administer the terminal
        """
        return chain(AdministratorTerminals.operators(self),
                     Administrator.root)

    def gen_vpn_keys(self):
        """Generates an OpenVPN key pair for the terminal"""
        build_script = openvpn['BUILD_SCRIPT']
        key_file_name = '.'.join([str(self.tid), str(self.cid)])
        rsa_dir = openvpn['EASY_RSA_DIR']
        keys_dir = join(rsa_dir, 'keys')
        key_file = join(keys_dir, key_file_name)
        if isfile(key_file):
            return False
        else:
            return run([build_script, key_file_name])


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


# XXX: Abstract
class _User(TermgrModel):
    """A generic user"""

    name = CharField(64)
    """The login name"""
    passwd = CharField(64)
    """The SHA-256 encoded password"""
    enabled = BooleanField()
    """Flags whether the account is enabled"""
    annotation = CharField(255, null=True)
    """An optional Annotation"""

    @classmethod
    def authenticate(cls, name, passwd):
        """Authenticate with name and hashed password"""
        if passwd:
            try:
                user = cls.iget(cls.name == name)
            except DoesNotExist:
                return False
            else:
                if user.passwd:
                    if user.passwd == passwd:
                        if user.enabled:
                            return user
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
        else:
            return False


@create
class Administrator(_User):
    """A user that is allowed to create,
    modify and delete all terminals
    """
    pass


@create
class SetupOperator(_User):
    """A user that is allowed to setup systems by HOMEINFO"""

    company = ForeignKeyField(Company, db_column='company',
                              related_name='setup_operators')
    """The respective company"""

    class Meta:
        db_table = 'setup_operator'

    @property
    def terminals(self):
        """Yields the terminals, the operator is allowed to use"""
        return SetupOperatorTerminals.terminals(self)

    def authorize(self, terminal):
        """Checks whether the setup operator is
        allowed to setup a certain terminal
        """
        return terminal in self.terminals


@create
class SetupOperatorTerminals(TermgrModel):
    """Many-to-many mapping in-between setup operators and terminals"""

    class Meta:
        db_table = 'terminal_operators'

    operator = ForeignKeyField(SetupOperator, db_column='operator')
    """The respective setup operator"""
    terminal = ForeignKeyField(Terminal, db_column='terminal')
    """The respective terminal"""

    @classmethod
    def terminals(cls, operator):
        """Yields terminals of the specified operator"""
        for mapping in cls.iselect(cls.operator == operator):
            yield mapping.terminal

    @classmethod
    def operators(cls, terminal):
        """Yields operators of the specified terminal"""
        for mapping in cls.iselect(cls.terminal == terminal):
            yield mapping.operator


@create
class AdministratorTerminals(TermgrModel):
    """Many-to-many mapping in-between setup operators and terminals"""

    class Meta:
        db_table = 'terminal_admins'

    administrator = ForeignKeyField(Administrator, db_column='administrator')
    """The respective setup operator"""
    terminal = ForeignKeyField(Terminal, db_column='terminal')
    """The respective terminal"""

    @classmethod
    def terminals(cls, operator):
        """Yields terminals of the specified operator"""
        for mapping in cls.iselect(cls.operator == operator):
            yield mapping.terminal

    @classmethod
    def operators(cls, terminal):
        """Yields operators of the specified terminal"""
        for mapping in cls.iselect(cls.terminal == terminal):
            yield mapping.operator
