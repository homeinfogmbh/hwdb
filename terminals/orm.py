"""Terminal library database models"""

from itertools import chain
from datetime import datetime
from ipaddress import IPv4Network, IPv4Address, AddressValueError
from hashlib import sha256
from uuid import uuid4

from peewee import Model, ForeignKeyField, IntegerField, CharField,\
    BigIntegerField, DoesNotExist, DateTimeField, BooleanField, PrimaryKeyField

from homeinfo.lib.misc import classproperty
from homeinfo.lib.system import run
from homeinfo.peewee import MySQLDatabase, create
from homeinfo.crm import Customer, Address, Company, Employee

from .config import terminals_config

__all__ = ['Class', 'Domain', 'Weather', 'OS', 'VPN', 'Terminal',
           'Synchronization', 'Administrator', 'SetupOperator',
           'NagiosAdmins', 'AccessStats']


class TerminalError(Exception):
    """Basic exception for terminals handling"""

    pass


class TerminalConfigError(TerminalError):
    """Exception that indicated errors in the terminal configuration"""

    pass


class VPNUnconfiguredError(TerminalConfigError):
    """Indicated that no VPN configuration has
    been assigned to the respective terminal
    """

    pass


class AddressUnconfiguredError(TerminalConfigError):
    """Indicated that no address has been configured for the terminal"""

    pass


class TerminalModel(Model):
    """Terminal manager basic Model"""

    id = PrimaryKeyField()

    class Meta:
        database = MySQLDatabase(
            terminals_config.db['db'],
            host=terminals_config.db['host'],
            user=terminals_config.db['user'],
            passwd=terminals_config.db['passwd'],
            closing=True)
        schema = database.database


class _User(TerminalModel):
    """A generic abstract user"""

    name = CharField(64)
    pwhash = CharField(64)
    salt = CharField(36)
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
                if user.passwd and passwd:
                    pwstr = passwd + user.salt
                    pwhash = sha256(pwstr.encode()).hexdigest()
                    if user.pwhash == pwhash:
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

    @property
    def passwd(self):
        """Returns the password hash"""
        return self.pwhash

    @passwd.setter
    def passwd(self, passwd):
        """Creates a new password hash"""
        salt = str(uuid4())
        pwstr = passwd + salt
        pwhash = sha256(pwstr.encode()).hexdigest()
        self.salt = salt
        self.pwhash = pwhash
        self.save()


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
            new_class = cls.get(
                (cls.name == name) &
                (cls.touch == touch)
            )
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

    # The domain's fully qualified domain name
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
            self._fqdn = fqdn
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
class OS(TerminalModel):
    """Operating systems"""

    family = CharField(8)
    name = CharField(16)
    version = CharField(16, null=True, default=None)

    def __str__(self):
        """Returns the family name"""
        return self.family

    def __repr__(self):
        """Returns the OS name and version"""
        return '{0} {1}'.format(self.name, self.version)


@create
class VPN(TerminalModel):
    """OpenVPN settings"""

    NETWORK = IPv4Network('10.8.0.0/16')

    _ipv4addr = BigIntegerField(db_column='ipv4addr')
    key = CharField(36, null=True, default=None)

    @classmethod
    def add(cls, key=None, ipv4addr=None):
        """Adds a record for the terminal"""
        openvpn = cls()
        openvpn.key = key
        openvpn.ipv4addr = cls._gen_addr(desired=ipv4addr)
        openvpn.save()
        return openvpn

    @classproperty
    @classmethod
    def used_ipv4addrs(cls):
        """Yields used IPv4 addresses"""
        for openvpn in cls:
            yield openvpn.ipv4addr

    @classproperty
    @classmethod
    def free_ipv4addrs(cls):
        """Yields availiable IPv4 addresses"""
        used_ipv4addrs = [a for a in cls.used_ipv4addrs]
        lowest = None
        for ipv4addr in cls.NETWORK:
            if lowest is None:
                lowest = ipv4addr + 10
            elif ipv4addr >= lowest:
                if ipv4addr not in used_ipv4addrs:
                    yield ipv4addr

    @classmethod
    def _gen_addr(cls, desired=None):
        """Generates a unique IPv4 address"""
        if desired is not None:
            try:
                ipv4addr = IPv4Address(desired)
            except AddressValueError:
                raise ValueError('Not an IPv4 address: {0}'.format(ipv4addr))
            else:
                if ipv4addr in cls.free_ipv4addrs:
                    return ipv4addr
                else:
                    raise ValueError(
                        'IPv4 address {0} is already in use'.format(ipv4addr))
        else:
            for ipv4addr in cls.free_ipv4addrs:
                return ipv4addr
            raise TerminalConfigError('Network exhausted!')

    @property
    def ipv4addr(self):
        """Returns an IPv4 Address"""
        return IPv4Address(self._ipv4addr)

    @ipv4addr.setter
    def ipv4addr(self, ipv4addr):
        """Sets the IPv4 address"""
        self._ipv4addr = int(ipv4addr)


@create
class Connection(TerminalModel):
    """Connection data"""

    name = CharField(4)
    timeout = IntegerField()


@create
class Terminal(TerminalModel):
    """A physical terminal out in the field"""

    # Ping once and wait two seconds max.
    _CHK_CMD = '/bin/ping -c 1 -W {timeout} {host}'

    tid = IntegerField()    # Customer-unique terminal identifier
    customer = ForeignKeyField(
        Customer, db_column='customer', related_name='terminals')
    class_ = ForeignKeyField(
        Class, db_column='class', related_name='terminals')
    os = ForeignKeyField(OS, db_column='os', related_name='terminals')
    connection = ForeignKeyField(
        Connection, db_column='connection', null=True, default=None)
    vpn = ForeignKeyField(
        VPN, null=True, db_column='vpn',
        related_name='terminals', default=None)
    domain = ForeignKeyField(
        Domain, db_column='domain', related_name='terminals')
    location = ForeignKeyField(Address, null=True, db_column='location')
    vid = IntegerField(null=True)
    weather = ForeignKeyField(
        Weather, null=True, db_column='weather', related_name='terminals')
    deployed = DateTimeField(null=True, default=None)
    deleted = DateTimeField(null=True, default=None)
    testing = BooleanField(default=False)
    annotation = CharField(255, null=True, default=None)

    def __str__(self):
        """Converts the terminal to a unique string"""
        return '.'.join([str(ident) for ident in self.idents])

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
                term = cls.get(
                    (cls.customer == cid) & (cls.tid == tid) &
                    (cls.deleted >> None))
            except DoesNotExist:
                term = None
        return term

    @classmethod
    def tids(cls, cid):
        """Yields used terminal IDs for a certain customer"""
        for terminal in cls.select().where(cls.customer == cid):
            yield terminal.tid

    @classmethod
    def gen_tid(cls, cid, desired=None):
        """Gets a unique terminal ID for the customer"""
        if desired is None:
            tid = 1
            while tid in cls.tids(cid):
                tid += 1
            return tid
        else:
            if tid in cls.tids(cid):
                return cls.gen_tid(cid, desired=None)
            else:
                return tid

    @classmethod
    def by_virt(cls, cid, vid):
        """Yields terminals of a customer that
        run the specified virtual terminal
        """
        return cls.select().where((cls.customer == cid) & (cls.vid == vid))

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
        if self.vpn is not None:
            return self.vpn.ipv4addr
        else:
            raise VPNUnconfiguredError()

    @property
    def address(self):
        location = self.location
        if location is not None:
            try:
                street_houseno = '{0} {1}'.format(
                    location.street, location.house_number)
            except (TypeError, ValueError):
                return None
            else:
                try:
                    zip_city = '{0} {1}'.format(
                        location.zip_code, location.city)
                except (TypeError, ValueError):
                    return None
                else:
                    return '{0}, {1}'.format(street_houseno, zip_city)
        else:
            raise AddressUnconfiguredError()

    @property
    def operators(self):
        """Yields the operators, which are
        allowed to setup the terminal
        """
        return OperatorTerminals.operators(self)

    @property
    def administrators(self):
        """Yields the administrators, which are
        allowed to administer the terminal
        """
        return chain(AdministratorTerminals.operators(self),
                     Administrator.root)

    @property
    def status(self):
        """Determines the status of the terminal

        This may take some time, so use it carefully
        """
        if self.connection:
            chk_cmd = self._CHK_CMD.format(
                timeout=self.connection.timeout, host=self.hostname)
            if run(chk_cmd, shell=True):
                return True
            else:
                return False
        else:
            return False

    @property
    def productive(self):
        """Returns whether the system has been deployed and is non-testing"""
        return True if self.deployed and not self.testing else False


@create
class Synchronization(TerminalModel):
    """Synchronization log

    Recommended usage:
        with Synchronization.start(terminal) as sync:
            <do_sync_stuff>
            if sync_succeded:
                sync.status = True
            else:
                sync.status = False
    """

    terminal = ForeignKeyField(
        Terminal, db_column='terminal', related_name='_synchronizations')
    started = DateTimeField()
    finished = DateTimeField(null=True, default=None)
    reload = BooleanField(null=True, default=None)
    force = BooleanField(null=True, default=None)
    nocheck = BooleanField(null=True, default=None)
    result = BooleanField(null=True, default=None)
    annotation = CharField(255, null=True, default=None)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.stop()

    @classmethod
    def start(cls, terminal):
        """Start a synchronization for this terminal"""
        sync = cls()
        sync.terminal = terminal
        sync.started = datetime.now()
        return sync

    def stop(self):
        """Stops the synchronization"""
        self.finished = datetime.now()
        return self.save()


@create
class Administrator(_User):
    """A user that is allowed to create,
    modify and delete all terminals
    """
    pass


@create
class Operator(_User):
    """A user that is allowed to setup systems by HOMEINFO"""

    class Meta:
        db_table = 'operator'

    company = ForeignKeyField(
        Company, db_column='company', related_name='setup_operators')

    @property
    def terminals(self):
        """Yields the terminals, the operator is allowed to use"""
        return OperatorTerminals.terminals(self)

    def authorize(self, terminal):
        """Checks whether the setup operator is
        allowed to setup a certain terminal
        """
        return self.root or terminal in self.terminals


@create
class OperatorTerminals(TerminalModel):
    """Many-to-many mapping in-between setup operators and terminals"""

    class Meta:
        db_table = 'terminal_operators'

    operator = ForeignKeyField(Operator, db_column='operator')
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
class AdministratorTerminals(TerminalModel):
    """Many-to-many mapping in-between administrators and terminals"""

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


@create
class AccessStats(TerminalModel):
    """Stores application access statistics"""

    class Meta:
        db_table = 'access_stats'

    customer = ForeignKeyField(Customer, db_column='customer')
    tid = IntegerField(null=True, default=None)
    vid = IntegerField()
    document = CharField(255)
    timestamp = DateTimeField()

    @classmethod
    def add(cls, cid, vid, document, tid=None):
        """Creates a new record"""
        record = cls()
        record.customer = cid
        record.tid = tid
        record.vid = vid
        record.document = document
        record.timestamp = datetime.now()
        if record.save():
            return True
        else:
            return False
