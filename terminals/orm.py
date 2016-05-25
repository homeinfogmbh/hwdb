"""Terminal library ORM models"""

from itertools import chain
from datetime import datetime
from ipaddress import IPv4Network, IPv4Address, AddressValueError
from logging import getLogger

from peewee import Model, ForeignKeyField, IntegerField, CharField,\
    BigIntegerField, DoesNotExist, DateTimeField, BooleanField, PrimaryKeyField

from homeinfo.lib.misc import classproperty
from homeinfo.lib.system import run
from homeinfo.peewee import MySQLDatabase
from homeinfo.crm import Customer, Address, Company, Employee

from .config import terminals_config

__all__ = [
    'TerminalError',
    'TerminalConfigError',
    'VPNUnconfiguredError',
    'AddressUnconfiguredError',
    'Class',
    'Domain',
    'Weather',
    'OS',
    'VPN',
    'Terminal',
    'Synchronization',
    'NagiosAdmins',
    'AccessStats']


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
                (cls.touch == touch))
        except DoesNotExist:
            new_class = cls()
            new_class.name = name
            new_class.full_name = full_name
            new_class.touch = True if touch else False
            new_class.save()
        finally:
            return new_class


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


class Weather(TerminalModel):
    """Weather data records"""

    name = CharField(16)  # The location name
    # The absolute path to the respective XML file
    xml_file = CharField(128)


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


class Connection(TerminalModel):
    """Connection data"""

    name = CharField(4)
    timeout = IntegerField()

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.timeout)


class Location(TerminalModel):
    """Location of a terminal"""

    address = ForeignKeyField(Address, null=False, db_column='address')
    annotation = CharField(255, null=True, default=None)

    def __iter__(self):
        """Yields location items"""
        yield self.address.street
        yield self.address.house_number
        yield self.address.zip_code
        yield self.address.city

        if self.annotation:
            yield self.annotation

    def __str__(self):
        """Returns location string"""
        return '\n'.join((str(item) for item in self))

    def __repr__(self):
        """Returns a unique on-liner"""
        result = '{street}, {house_number}, {zip_code} {city}'.format(
            street=self.address.street,
            house_number=self.address.house_number,
            zip_code=self.address.zip_code,
            city=self.address.city)

        if self.annotation:
            result += ' ({})'.format(self.annotation)

        return result

    @classmethod
    def add(cls, address, annotation=None):
        """Adds a unique location"""
        if annotation is None:
            try:
                location = cls.get(cls.address == address)
            except DoesNotExist:
                location = cls()
                location.address = address
                location.save()

            return location
        else:
            try:
                location = cls.get(
                    (cls.address == address) &
                    (cls.annotation == annotation))
            except DoesNotExist:
                location = cls()
                location.address = address
                location.annotation = annotation
                location.save()

            return location


class Terminal(TerminalModel):
    """A physical terminal out in the field"""

    # Ping once
    _CHK_CMD = '/bin/ping -c 1 -W {timeout} {host}'
    logger = getLogger('Terminal')

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
    location = ForeignKeyField(Location, null=True, db_column='location')
    vid = IntegerField(null=True)
    weather = ForeignKeyField(
        Weather, null=True, db_column='weather', related_name='terminals')
    deployed = DateTimeField(null=True, default=None)
    deleted = DateTimeField(null=True, default=None)
    testing = BooleanField(default=False)
    replacement = BooleanField(default=False)
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
    def by_cid(cls, cid):
        """Yields terminals of a customer that
        run the specified virtual terminal
        """
        return cls.select().where(cls.customer == cid).order_by(Terminal.tid)

    @classmethod
    def by_ids(cls, cid, tid, deleted=False):
        """Get a terminal by customer id and terminal id"""
        if deleted:
            return cls.get((cls.customer == cid) & (cls.tid == tid))
        else:
            return cls.get(
                (cls.customer == cid) &
                (cls.tid == tid) &
                (cls.deleted >> None))

    @classmethod
    def by_virt(cls, cid, vid):
        """Yields terminals of a customer that
        run the specified virtual terminal
        """
        return cls.select().where(
            (cls.customer == cid) &
            (cls.vid == vid)).order_by(
                Terminal.tid)

    @classmethod
    def tids(cls, cid):
        """Yields used terminal IDs for a certain customer"""
        for terminal in cls.by_cid(cid):
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
    def min_tid(cls, customer):
        """Gets the highest TID for the respective customer"""
        result = None
        for terminal in cls.select().where(cls.customer == customer):
            if result is None:
                result = terminal.cid
            else:
                result = min(result, terminal.cid)
        return result

    @classmethod
    def max_tid(cls, customer):
        """Gets the highest TID for the respective customer"""
        result = 0
        for terminal in cls.select().where(cls.customer == customer):
            result = max(result, terminal.cid)
        return result

    @classmethod
    def min_vid(cls, customer):
        """Gets the highest VID for the respective customer"""
        result = None
        for terminal in cls.select().where(cls.customer == customer):
            if terminal.vid is not None:
                if result is None:
                    result = terminal.vid
                else:
                    result = min(result, terminal.vid)
        return result

    @classmethod
    def max_vid(cls, customer):
        """Gets the highest TID for the respective customer"""
        result = 0
        for terminal in cls.select().where(cls.customer == customer):
            if terminal.vid is not None:
                result = max(result, terminal.vid)
        return result

    @classmethod
    def add(cls, cid, class_, os, connection, vpn, domain,
            location=None, annotation=None, tid=None):
        """Adds a new terminal"""

        tid = cls.gen_tid(cid, desired=tid)

        terminal = cls()
        terminal.tid = tid
        terminal.customer = cid
        terminal.class_ = class_
        terminal.os = os
        terminal.connection = connection
        terminal.vpn = vpn
        terminal.domain = domain
        terminal.location = location
        terminal.vid = None
        terminal.deployed = None
        terminal.deleted = None
        terminal.testing = False
        terminal.replacement = False
        terminal.annotation = annotation

        if terminal.save():
            return terminal
        else:
            return False

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
            address = location.address

            try:
                street_houseno = '{0} {1}'.format(
                    address.street, address.house_number)
            except (TypeError, ValueError):
                return None
            else:
                try:
                    zip_city = '{0} {1}'.format(
                        address.zip_code, address.city)
                except (TypeError, ValueError):
                    return None
                else:
                    return '{0}, {1}'.format(street_houseno, zip_city)
        else:
            raise AddressUnconfiguredError()

    @property
    def operators(self):
        """Yields the operators, which are
        allowed to set the terminal up
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

    def deploy(self, date_time=None, force=False):
        """Sets terminals to deployed"""
        if self.deployed is None or force:
            deployed = datetime.now() if date_time is None else date_time
            self.logger.info(
                'Deploying terminal {0} on {1}'.format(self, deployed))
            self.deployed = deployed
            self.save()
            return True
        else:
            self.logger.warning(
                'Terminal {0} has already been deployed on {1}'.format(
                    self, self.deployed))
            return False

    def undeploy(self, force=False):
        """Sets terminals to NOT deployed"""
        if self.deployed is not None or force:
            self.logger.info('Undeploying terminal {0} from {1}'.format(
                self, self.deployed))
            self.deployed = None
            self.save()
            return True
        else:
            self.logger.warning('Terminal {0} is not deployed'.format(self))
            return False


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
    _email = CharField(255, db_column='email', null=True, default=None)
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

    @property
    def email(self):
        """Returns the admin's email"""
        if self._email is None:
            return self.employee.email
        else:
            return self._email


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
