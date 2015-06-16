"""Terminal library database models"""

from itertools import chain
from datetime import datetime
from ipaddress import IPv4Address, AddressValueError
from peewee import Model, MySQLDatabase, ForeignKeyField, IntegerField,\
    CharField, BigIntegerField, DoesNotExist, DateTimeField, BlobField,\
    BooleanField, create, PrimaryKeyField
from homeinfo.lib.misc import classproperty
from homeinfo.crm import Customer, Address, Company
from .config import db, net
from .lib import Rotation

__all__ = ['Domain', 'Class', 'Terminal', 'Screenshot', 'ConsoleHistory',
           'Administrator', 'SetupOperator']


class TermgrModel(Model):
    """Terminal manager base Model"""

    class Meta:
        database = MySQLDatabase(
            db.get('db'), host=db.get('host'), user=db.get('user'),
            passwd=db.get('passwd'))
        schema = database.database

    id = PrimaryKeyField()


@create
class Class(TermgrModel):
    """Terminal classes"""

    name = CharField(32)
    full_name = CharField(32)
    # Touch display flag
    touch = BooleanField()

    @classmethod
    def add(cls, name, full_name=None, touch=False):
        """Adds a terminal class"""
        try:
            new_class = cls.get((cls.name == name) &
                                (cls.touch == touch))
        except DoesNotExist:
            new_class = cls()
            new_class.name = name
            new_class.full_name = full_name
            new_class.touch = True if touch else False
            new_class.save()
        finally:
            return new_class


@create
class Domain(TermgrModel):
    """Terminal domains"""

    # The domain's fully qulaifited domain name
    _fqdn = CharField(32, db_column='fqdn')

    @classmethod
    def add(cls, fqdn):
        """Adds a domain with a certain FQDN"""
        try:
            domain = cls.get(cls._fqdn == fqdn)
        except DoesNotExist:
            domain = cls()
            domain.fqdn = fqdn
            domain.save()
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
class Weather(TermgrModel):
    """Weather data records"""

    name = CharField(16)
    """The location name"""
    xml_file = CharField(128)
    """The absolute path to the respective XML file"""


@create
class SyncTicket(TermgrModel):
    """A synchronization ticket"""

    issued = DateTimeField()


@create
class Terminal(TermgrModel):
    """A physical terminal out in the field"""

    customer = ForeignKeyField(Customer, db_column='customer',
                               related_name='terminals')
    tid = IntegerField()    # Customer-unique terminal identifier
    class_ = ForeignKeyField(Class, db_column='class',
                             related_name='terminals')
    domain = ForeignKeyField(Domain, db_column='domain',
                             related_name='terminals')
    _ipv4addr = BigIntegerField(db_column='ipv4addr', null=True)
    virtual_display = IntegerField(null=True)
    location = ForeignKeyField(Address, null=True, db_column='location')
    deleted = DateTimeField(null=True, default=None)
    weather = ForeignKeyField(Weather, null=True, db_column='weather',
                              related_name='terminals')
    _rotation = IntegerField(db_column='rotation')
    ticket = ForeignKeyField(SyncTicket, db_column='ticket',
                             null=True, default=None)

    def __repr__(self):
        """Converts the terminal to a unique string"""
        return '.'.join([str(ident) for ident in self.idents])

    @classproperty
    @classmethod
    def used_ipv4addr(cls):
        """Yields used IPv4 addresses"""
        for terminal in cls.select().where(True):
            yield terminal.ipv4addr

    @classproperty
    @classmethod
    def hosts(cls):
        """Yields entries for /etc/hosts"""
        for terminal in cls.select().where(True):
            yield '\t'.join([str(terminal.ipv4addr), terminal.hostname])

    @classmethod
    def by_ids(cls, cid, tid, deleted=False):
        """Get a terminal by customer id and terminal id"""
        if deleted:
            try:
                term = cls.get((cls.customer == cid) & (cls.tid == tid))
            except DoesNotExist:
                term = None
        else:
            try:
                term = cls.get((cls.customer == cid) & (cls.tid == tid) &
                               (cls.deleted >> None))
            except DoesNotExist:
                term = None
        return term

    @classmethod
    def used_tids(cls, cid):
        """Yields used terminal IDs for a certain customer"""
        for terminal in cls.select().where(cls.customer == cid):
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

    @classmethod
    def by_virt(cls, cid, vid):
        """Yields terminals of a customer that
        run the specified virtual terminal
        """
        return cls.select().where((cls.customer == cid) &
                                  (cls.virtual_display == vid))

    @property
    def cid(self):
        """Returns the customer identifier"""
        return self.customer.id

    @property
    def idents(self):
        """Returns the terminals identifiers"""
        return (self.tid, self.cid)

    @property
    def hostname(self):
        """Generates and returns the terminal's host name"""
        return '.'.join([str(self.tid), str(self.cid),
                         self.domain.name])

    @property
    def ipv4addr(self):
        """Returns an IPv4 Address"""
        return IPv4Address(self._ipv4addr)

    @ipv4addr.setter
    def ipv4addr(self, ipv4addr):
        """Sets the IPv4 address"""
        self._ipv4addr = int(ipv4addr)

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
    def rotation(self):
        """Returns the rotation"""
        if self._rotation is None:
            return None
        else:
            return Rotation(degrees=self._rotation)

    @rotation.setter
    def rotation(self, rotation):
        """Sets the rotation"""
        if rotation is None:
            self._rotation = None
        else:
            try:
                self._rotation = rotation.degrees
            except AttributeError:
                self._rotation = int(Rotation(degrees=rotation))

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

    def appconf(self, checkdate=False):
        """Generates the content for the config.ini, respectively
        the application.conf configuration file for the application
        """
        if self.class_.touch:
            mouse_visible = False
        else:
            mouse_visible = True
        if self.rotation is None:
            rotation = True
            rotation_degrees = 0
        else:
            rot = int(self.rotation)
            if rot == 0:
                rotation = False
                rotation_degrees = 0
            else:
                rotation = True
                rotation_degrees = rot
        knr = '='.join(['knr', str(self.customer.id)])
        tracking_id = self.customer.piwik_tracking_id
        tracking_id = '='.join(['trackingid', str(tracking_id) if
                                tracking_id is not None else '42'])
        mouse_visible = '='.join(['mouse_visible', str(mouse_visible).lower()])
        checkdate = '='.join(['checkdate', str(checkdate).lower()])
        rotation = '='.join(['rotation', str(rotation).lower()])
        rotation_degrees = '='.join(['rotationDegrees', str(rotation_degrees)])
        return '\n'.join([knr, tracking_id, mouse_visible, checkdate, rotation,
                          rotation_degrees])


@create
class Synchronization(TermgrModel):
    """A synchronization log"""

    terminal = ForeignKeyField(
        Terminal, db_column='terminal', related_name='syncs')
    started = DateTimeField()
    finished = DateTimeField(null=True, default=None)
    status = BooleanField(default=False)
    annotation = CharField(255, null=True, default=None)


@create
class Screenshot(TermgrModel):
    """Terminal screenshots"""

    terminal = ForeignKeyField(
        Terminal, db_column='terminal', related_name='screenshots')
    screenshot = BlobField()
    thumbnail = BlobField()
    date = DateTimeField(default=datetime.now())


@create
class ConsoleHistory(TermgrModel):
    """A physical terminal's virtual console's history"""

    class Meta:
        db_table = 'console_history'

    terminal = ForeignKeyField(Terminal, db_column='terminal',
                               related_name='console_log')
    timestamp = DateTimeField(default=datetime.now())
    command = CharField(255)
    stdout = BlobField()
    stderr = BlobField()
    exit_code = IntegerField()


# XXX: Abstract
class _User(TermgrModel):
    """A generic user"""

    name = CharField(64)
    passwd = CharField(64)
    enabled = BooleanField()
    annotation = CharField(255, null=True)
    root = BooleanField(default=False)

    @classmethod
    def authenticate(cls, name, passwd):
        """Authenticate with name and hashed password"""
        if passwd:
            try:
                user = cls.get(cls.name == name)
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

    company = ForeignKeyField(
        Company, db_column='company', related_name='setup_operators')

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
        return self.root or terminal in self.terminals


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
        for mapping in cls.select().where(cls.operator == operator):
            yield mapping.terminal

    @classmethod
    def operators(cls, terminal):
        """Yields operators of the specified terminal"""
        for mapping in cls.select().where(cls.terminal == terminal):
            yield mapping.operator


@create
class AdministratorTerminals(TermgrModel):
    """Many-to-many mapping in-between setup operators and terminals"""

    class Meta:
        db_table = 'terminal_admins'

    administrator = ForeignKeyField(Administrator, db_column='administrator')
    terminal = ForeignKeyField(Terminal, db_column='terminal')

    @classmethod
    def terminals(cls, operator):
        """Yields terminals of the specified operator"""
        for mapping in cls.select().where(cls.operator == operator):
            yield mapping.terminal

    @classmethod
    def operators(cls, terminal):
        """Yields operators of the specified terminal"""
        for mapping in cls.select().where(cls.terminal == terminal):
            yield mapping.operator
