"""Terminal library database models"""

from itertools import chain
from datetime import datetime
from ipaddress import IPv4Address, AddressValueError
from hashlib import sha256

from peewee import Model, MySQLDatabase, ForeignKeyField, IntegerField,\
    CharField, BigIntegerField, DoesNotExist, DateTimeField, BlobField,\
    BooleanField, create, PrimaryKeyField

from homeinfo.lib.misc import classproperty
from homeinfo.crm import Customer, Address, Company, Employee
from homeinfo.lib.system import run

from .config import terminals_config
from .lib import Rotation

__all__ = ['Domain', 'Class', 'Terminal', 'Screenshot', 'ConsoleHistory',
           'Administrator', 'SetupOperator', 'NagiosAdmins']


class TerminalModel(Model):
    """Terminal manager base Model"""

    class Meta:
        database = MySQLDatabase(
            terminals_config.db['db'],
            host=terminals_config.db['host'],
            user=terminals_config.db['user'],
            passwd=terminals_config.db['passwd'])
        schema = database.database

    id = PrimaryKeyField()


@create
class Class(TerminalModel):
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
class Domain(TerminalModel):
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
            raise ValueError('Not a FQDN: {0}'.format(fqdn))

    @property
    def name(self):
        """Returns the domain name without trailing '.'"""
        return self._fqdn[:-1]


@create
class Weather(TerminalModel):
    """Weather data records"""

    name = CharField(16)  # The location name
    # The absolute path to the respective XML file
    xml_file = CharField(128)


@create
class Terminal(TerminalModel):
    """A physical terminal out in the field"""

    _CHK_CMD = '/bin/ping -c 1 -W 1 {0}'

    customer = ForeignKeyField(
        Customer, db_column='customer', related_name='terminals')
    tid = IntegerField()    # Customer-unique terminal identifier
    class_ = ForeignKeyField(
        Class, db_column='class', related_name='terminals')
    domain = ForeignKeyField(
        Domain, db_column='domain', related_name='terminals')
    _ipv4addr = BigIntegerField(db_column='ipv4addr', null=True)
    virtual_display = IntegerField(null=True)
    location = ForeignKeyField(Address, null=True, db_column='location')
    deleted = DateTimeField(null=True, default=None)
    weather = ForeignKeyField(
        Weather, null=True, db_column='weather', related_name='terminals')
    _rotation = IntegerField(db_column='rotation')
    last_sync = DateTimeField(null=True, default=None)

    def __str__(self):
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
            yield '{0}\t{1}'.format(terminal.ipv4addr, terminal.hostname)

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
            net_base = terminals_config.net['IPV4NET']
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
                raise ValueError('Not and IPv4 address: {0}'.format(
                    desired)) from None
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
        return '{0}.{1}.{2}'.format(self.tid, self.cid, self.domain.name)

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
            street_houseno = '{0} {1}'.format(
                location.street, location.house_number)
        except (TypeError, ValueError):
            return None
        else:
            try:
                zip_city = '{0} {1}'.format(location.zip_code, location.city)
            except (TypeError, ValueError):
                return None
            else:
                return '{0}, {1}'.format(street_houseno, zip_city)

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

    @property
    def online(self):
        """Determines whether the terminal is online"""
        ping = 'ping -q -c 3 -t 1 {0} > /dev/null 2> /dev/null'.format(
            self.hostname)
        return run(ping, shell=True)

    @property
    def status(self):
        """Determines the status of the terminal"""
        chk_cmd = self._CHK_CMD.format(self.hostname)
        if run(chk_cmd, shell=True):
            return True
        else:
            return False

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
        knr = 'knr={0}'.format(self.customer.id)
        tracking_id = self.customer.piwik_tracking_id
        tracking_id = 'trackingid={0}'.format(
            tracking_id if tracking_id is not None else '42')
        mouse_visible = 'mouse_visible={0}'.format(mouse_visible).lower()
        checkdate = 'checkdate={0}'.format(checkdate).lower()
        rotation = 'rotation={0}'.format(rotation).lower()
        rotation_degrees = 'rotationDegrees={0}'.format(rotation_degrees)
        return '\n'.join([knr, tracking_id, mouse_visible, checkdate, rotation,
                          rotation_degrees])


@create
class Screenshot(TerminalModel):
    """Terminal screenshots"""

    terminal = ForeignKeyField(
        Terminal, db_column='terminal', related_name='screenshots')
    screenshot = BlobField()
    thumbnail = BlobField()
    date = DateTimeField(default=None)


@create
class ConsoleHistory(TerminalModel):
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
class _User(TerminalModel):
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
                    if user.passwd == sha256(passwd.encode()).hexdigest():
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
class SetupOperatorTerminals(TerminalModel):
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
class AdministratorTerminals(TerminalModel):
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


@create
class NagiosAdmins(TerminalModel):
    """Many-to-many mapping in-between
    Employees and terminal classes
    """

    class Meta:
        db_table = 'nagios_admins'

    _name = CharField(16, db_column='name', null=True, default=None)
    employee = ForeignKeyField(Employee, db_column='employee')
    class_ = ForeignKeyField(
        Class, null=True, db_column='class', related_name='members')
    service_period = CharField(16, default='24x7')
    host_period = CharField(16, default='24x7')
    service_options = CharField(16, default='w,u,c,r')
    host_options = CharField(16, default='d,r')
    host_command = CharField(64, default='notify-terminal-by-email-with-id')

    @property
    def admin(self):
        """Determines whether the Nagios
        admin is a global terminal admin
        """
        return self.class_ is None

    @property
    def name(self):
        """Returns a short name"""
        if self._name is None:
            return self.employee.surname
        else:
            return self._name
