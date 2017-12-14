"""Terminal library ORM models."""

from datetime import datetime
from ipaddress import IPv4Network, IPv4Address, AddressValueError

from peewee import Model, ForeignKeyField, IntegerField, CharField, \
    BigIntegerField, DoesNotExist, DateTimeField, BooleanField, PrimaryKeyField

from peeweeplus import MySQLDatabase
from syslib import run
from fancylog import Logger

from homeinfo.misc import classproperty
from homeinfo.crm import Customer, Address, Employee

from .config import CONFIG

__all__ = [
    'TerminalError',
    'TerminalConfigError',
    'VPNUnconfiguredError',
    'AddressUnconfiguredError',
    'Class',
    'Domain',
    'OS',
    'VPN',
    'Terminal',
    'Synchronization',
    'Admin',
    'Statistics',
    'LatestStats']


class TerminalError(Exception):
    """Basic exception for terminals handling."""

    pass


class TerminalConfigError(TerminalError):
    """Exception that indicated errors in the terminal configuration."""

    pass


class VPNUnconfiguredError(TerminalConfigError):
    """Indicated that no VPN configuration has
    been assigned to the respective terminal.
    """

    pass


class AddressUnconfiguredError(TerminalConfigError):
    """Indicated that no address has been configured for the terminal."""

    pass


class TerminalModel(Model):
    """Terminal manager basic Model."""

    id = PrimaryKeyField()

    class Meta:
        database = MySQLDatabase(
            CONFIG['terminals']['database'],
            host=CONFIG['terminals']['host'],
            user=CONFIG['terminals']['user'],
            passwd=CONFIG['terminals']['passwd'],
            closing=True)
        schema = database.database


class Class(TerminalModel):
    """Terminal classes."""

    name = CharField(32)
    full_name = CharField(32)
    # Touch display flag
    touch = BooleanField()

    @classmethod
    def _add(cls, name, full_name=None, touch=False):
        """Forcibly adds a new class."""
        class_ = cls()
        class_.name = name

        if full_name is None:
            class_.full_name = name
        else:
            class_.full_name = full_name

        class_.touch = True if touch else False
        class_.save()
        return class_

    @classmethod
    def add(cls, name, full_name=None, touch=False):
        """Adds a terminal class."""
        try:
            return cls.get(
                (cls.name == name) &
                (cls.touch == touch))
        except DoesNotExist:
            return cls._add(name, full_name=full_name, touch=False)

    def to_dict(self):
        """Returns a JSON-like dictionary."""
        return {
            'token': self.name,
            'name': self.full_name,
            'touch': self.touch}


class Domain(TerminalModel):
    """Terminal domains."""

    # The domain's fully qualified domain name
    _fqdn = CharField(32, db_column='fqdn')

    @classmethod
    def add(cls, fqdn):
        """Adds a domain with a certain FQDN."""
        try:
            return cls.get(cls._fqdn == fqdn)
        except DoesNotExist:
            domain = cls()
            domain.fqdn = fqdn
            domain.save()
            return domain

    @property
    def fqdn(self):
        """Returns the FQDN."""
        return self._fqdn

    @fqdn.setter
    def fqdn(self, fqdn):
        """Sets the FQDN."""
        if fqdn.endswith('.') and not fqdn.startswith('.'):
            self._fqdn = fqdn
        else:
            raise ValueError('Not a FQDN: "{}".'.format(fqdn))

    @property
    def name(self):
        """Returns the domain name without trailing dot."""
        return self._fqdn[:-1]

    def to_dict(self):
        """Returns a JSON-like dictionary."""
        return self.fqdn


class OS(TerminalModel):
    """Operating systems."""

    family = CharField(8)
    name = CharField(16)
    version = CharField(16, null=True, default=None)

    def __str__(self):
        """Returns the family name."""
        return self.family

    def __repr__(self):
        """Returns the OS name and version."""
        return '{} {}'.format(self.name, self.version)

    @classmethod
    def search(cls, string):
        """Fuzzily searches an operating system by the given string."""
        try:
            return cls.get(cls.id == int(string))
        except ValueError:
            return cls.get(
                (cls.family == string)
                | (cls.name == string)
                | (cls.version == string))

    def to_dict(self):
        """Returns a JSON-like dictionary."""
        return {
            'family': self.family,
            'name': self.name,
            'version': self.version}


class VPN(TerminalModel):
    """OpenVPN settings."""

    NETWORK = IPv4Network('{}/{}'.format(
        CONFIG['net']['IPV4NET'],
        CONFIG['net']['IPV4MASK']))

    _ipv4addr = BigIntegerField(db_column='ipv4addr')
    key = CharField(36, null=True, default=None)
    mtu = IntegerField(null=True, default=None)

    @classmethod
    def add(cls, ipv4addr=None, key=None, mtu=None):
        """Adds a record for the terminal."""
        openvpn = cls()
        openvpn.ipv4addr = cls._gen_addr(desired=ipv4addr)
        openvpn.key = key
        openvpn.mtu = mtu
        openvpn.save()
        return openvpn

    @classproperty
    @classmethod
    def used_ipv4addrs(cls):
        """Yields used IPv4 addresses."""
        for openvpn in cls:
            yield openvpn.ipv4addr

    @classproperty
    @classmethod
    def free_ipv4addrs(cls):
        """Yields availiable IPv4 addresses."""
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
        """Generates a unique IPv4 address."""
        if desired is not None:
            try:
                ipv4addr = IPv4Address(desired)
            except AddressValueError:
                raise ValueError('Not an IPv4 address: {}.'.format(ipv4addr))
            else:
                if ipv4addr in cls.free_ipv4addrs:
                    return ipv4addr
                else:
                    raise ValueError(
                        'IPv4 address {} is already in use.'.format(ipv4addr))
        else:
            for ipv4addr in cls.free_ipv4addrs:
                return ipv4addr
            raise TerminalConfigError('Network exhausted!')

    @property
    def ipv4addr(self):
        """Returns an IPv4 Address."""
        return IPv4Address(self._ipv4addr)

    @ipv4addr.setter
    def ipv4addr(self, ipv4addr):
        """Sets the IPv4 address."""
        self._ipv4addr = int(ipv4addr)

    def to_dict(self):
        """Returns a JSON-like dictionary."""
        return {'ipv4addr': str(self.ipv4addr), 'key': self.key}


class Connection(TerminalModel):
    """Internet connection information."""

    name = CharField(4)
    timeout = IntegerField()

    def __str__(self):
        return '{} ({})'.format(self.name, self.timeout)

    def to_dict(self):
        """Returns a JSON-like dictionary."""
        return {'name': self.name, 'timeout': self.timeout}


class Location(TerminalModel):
    """Location of a terminal."""

    address = ForeignKeyField(Address, null=False, db_column='address')
    annotation = CharField(255, null=True, default=None)

    def __iter__(self):
        """Yields location items."""
        yield self.address.street
        yield self.address.house_number
        yield self.address.zip_code
        yield self.address.city

        if self.annotation:
            yield self.annotation

    def __str__(self):
        """Returns location string."""
        return '\n'.join((str(item) for item in self))

    def __repr__(self):
        """Returns a unique on-liner."""
        result = '{} {}, {} {}'.format(
            self.address.street, self.address.house_number,
            self.address.zip_code, self.address.city)

        if self.annotation:
            result += ' ({})'.format(self.annotation)

        return result

    @classmethod
    def _add(cls, address, annotation=None):
        """Forcibly adds a location record."""
        location = cls()
        location.address = address
        location.annotation = annotation
        location.save()
        return location

    @classmethod
    def add(cls, address, annotation=None):
        """Adds a unique location."""
        if annotation is None:
            annotation_selector = cls.annotation >> None
        else:
            annotation_selector = cls.annotation == annotation

        try:
            return cls.get((cls.address == address) & annotation_selector)
        except DoesNotExist:
            return cls._add(address, annotation=annotation)

    @property
    def shortinfo(self):
        """Returns a short information e.g. for Nagios."""
        result = ' '.join((self.address.street, self.address.house_number))

        if self.annotation:
            result = ' - '.join((result, self.annotation))

        return result

    def to_dict(self):
        """Returns a JSON-like dictionary."""
        return {
            'address': self.address.to_dict(),
            'annotation': self.annotation}


class Terminal(TerminalModel):
    """A physical terminal out in the field."""

    # Ping once
    _CHK_CMD = '/bin/ping -c 1 -W {timeout} {host}'
    logger = Logger('Terminal')

    tid = IntegerField()    # Customer-unique terminal identifier
    customer = ForeignKeyField(
        Customer, db_column='customer', on_update='CASCADE')
    class_ = ForeignKeyField(Class, db_column='class')
    os = ForeignKeyField(OS, db_column='os')
    connection = ForeignKeyField(Connection, db_column='connection', null=True)
    vpn = ForeignKeyField(VPN, null=True, db_column='vpn')
    domain = ForeignKeyField(Domain, db_column='domain')
    location = ForeignKeyField(Location, null=True, db_column='location')
    vid = IntegerField(null=True, default=None)
    weather = CharField(16, null=True)
    scheduled = DateTimeField(null=True, default=None)
    deployed = DateTimeField(null=True, default=None)
    deleted = DateTimeField(null=True, default=None)
    testing = BooleanField(default=False)
    replacement = BooleanField(default=False)
    tainted = BooleanField(default=False)
    monitor = BooleanField(null=True, default=None)
    annotation = CharField(255, null=True, default=None)
    serial_number = CharField(255, null=True, default=None)

    def __str__(self):
        """Converts the terminal to a unique string."""
        return '.'.join([str(ident) for ident in self.idents])

    @classproperty
    @classmethod
    def hosts(cls):
        """Yields entries for /etc/hosts."""
        for terminal in cls.select().where(True):
            yield '{}\t{}'.format(terminal.ipv4addr, terminal.hostname)

    @classmethod
    def by_cid(cls, cid):
        """Yields terminals of a customer that
        run the specified virtual terminal.
        """
        return cls.select().where(cls.customer == cid).order_by(Terminal.tid)

    @classmethod
    def by_ids(cls, cid, tid, deleted=False):
        """Get a terminal by customer id and terminal id."""
        if deleted:
            return cls.get((cls.customer == cid) & (cls.tid == tid))

        return cls.get(
            (cls.customer == cid) & (cls.tid == tid) & (cls.deleted >> None))

    @classmethod
    def by_virt(cls, cid, vid):
        """Yields terminals of a customer that
        run the specified virtual terminal.
        """
        return cls.select().where(
            (cls.customer == cid) &
            (cls.vid == vid)).order_by(
            Terminal.tid)

    @classmethod
    def tids(cls, cid):
        """Yields used terminal IDs for a certain customer."""
        for terminal in cls.by_cid(cid):
            yield terminal.tid

    @classmethod
    def gen_tid(cls, cid, desired=None):
        """Gets a unique terminal ID for the customer."""
        used_tids = cls.tids(cid)

        if desired is None:
            tid = 1

            while tid in used_tids:
                tid += 1

            return tid

        if desired in used_tids:
            return cls.gen_tid(cid, desired=None)

        return desired

    @classmethod
    def min_tid(cls, customer):
        """Gets the lowest TID for the respective customer."""
        result = None

        for terminal in cls.select().where(cls.customer == customer):
            if result is None:
                result = terminal.tid
            else:
                result = min(result, terminal.tid)

        return result

    @classmethod
    def max_tid(cls, customer):
        """Gets the highest TID for the respective customer."""
        result = 0

        for terminal in cls.select().where(cls.customer == customer):
            result = max(result, terminal.tid)

        return result

    @classmethod
    def min_vid(cls, customer):
        """Gets the highest VID for the respective customer."""
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
        """Gets the highest TID for the respective customer."""
        result = 0

        for terminal in cls.select().where(cls.customer == customer):
            if terminal.vid is not None:
                result = max(result, terminal.vid)

        return result

    @classmethod
    def add(cls, cid, class_, os, connection, vpn, domain,
            location=None, weather=None, scheduled=None,
            annotation=None, serial_number=None, tid=None):
        """Adds a new terminal."""
        terminal = cls()
        terminal.tid = cls.gen_tid(cid, desired=tid)
        terminal.customer = cid
        terminal.class_ = class_
        terminal.os = os
        terminal.connection = connection
        terminal.vpn = vpn
        terminal.domain = domain
        terminal.location = location
        terminal.vid = None
        terminal.weather = weather
        terminal.scheduled = scheduled
        terminal.deployed = None
        terminal.deleted = None
        terminal.testing = False
        terminal.replacement = False
        terminal.annotation = annotation
        terminal.serial_number = serial_number
        terminal.save()
        return terminal

    @property
    def cid(self):
        """Returns the customer identifier."""
        return self.customer.id

    @property
    def idents(self):
        """Returns the terminals identifiers."""
        return (self.tid, self.cid)

    @property
    def hostname(self):
        """Generates and returns the terminal's host name."""
        return '{}.{}.{}'.format(self.tid, self.cid, self.domain.name)

    @property
    def ipv4addr(self):
        """Returns an IPv4 Address."""
        if self.vpn is not None:
            return self.vpn.ipv4addr
        else:
            raise VPNUnconfiguredError()

    @property
    def address(self):
        """Returns the terminal's address."""
        location = self.location

        if location is not None:
            address = location.address

            try:
                street_houseno = '{} {}'.format(
                    address.street, address.house_number)
            except (TypeError, ValueError):
                return None
            else:
                try:
                    zip_city = '{} {}'.format(address.zip_code, address.city)
                except (TypeError, ValueError):
                    return None
                else:
                    return '{}, {}'.format(street_houseno, zip_city)
        else:
            raise AddressUnconfiguredError()

    @property
    def online(self):
        """Determines whether the terminal is online.
        This may take some time, so use it carefully.
        """
        if self.connection:
            chk_cmd = self._CHK_CMD.format(
                timeout=self.connection.timeout,
                host=self.hostname)

            if run(chk_cmd, shell=True):
                return True

        return False

    @property
    def syncable(self):
        """Determines whether the terminal
        can be synchronized by HIPSTER.
        """
        return self.os.family == 'Linux'

    @property
    def status(self):
        """Determines the status of the terminal."""
        return False if self.tainted else self.online

    @property
    def due(self):
        """Determines whether the terminal is due for deployment."""
        return self.scheduled is not None and self.scheduled <= datetime.now()

    @property
    def isdeployed(self):
        """Determines whether the terminal is deployed."""
        return self.deployed is not None and self.deployed <= datetime.now()

    @property
    def productive(self):
        """Returns whether the system has been deployed and is non-testing."""
        return self.isdeployed and not self.testing

    def deploy(self, date_time=None, force=False):
        """Sets terminals to deployed."""
        if self.deployed is None or force:
            deployed = datetime.now() if date_time is None else date_time
            self.logger.success('Deploying {} on {}.'.format(self, deployed))
            self.deployed = deployed
            self.save()
            return True

        self.logger.warning('{} has already been deployed on {}.'.format(
            self, self.deployed))
        return False

    def undeploy(self, force=False):
        """Sets terminals to NOT deployed."""
        if self.deployed is not None or force:
            self.logger.info('Undeploying {} from {}.'.format(
                self, self.deployed))
            self.deployed = None
            self.save()
            return True

        self.logger.warning('{} is not deployed.'.format(self))
        return False

    def to_dict(self, short=False):
        """Returns a JSON-like dictionary."""
        dictionary = {'tid': self.tid}

        if short:
            dictionary['customer'] = self.customer.id
        else:
            dictionary['customer'] = self.customer.to_dict()

        if self.location is not None:
            dictionary['location'] = self.location.to_dict()

        if self.scheduled is not None:
            dictionary['scheduled'] = self.scheduled.isoformat()

        if self.deployed is not None:
            dictionary['deployed'] = self.deployed.isoformat()

        if not short:
            dictionary['class'] = self.class_.to_dict()
            dictionary['os'] = self.os.to_dict()
            dictionary['domain'] = self.domain.to_dict()

            if self.connection is not None:
                dictionary['connection'] = self.connection.to_dict()

            if self.vpn is not None:
                dictionary['vpn'] = self.vpn.to_dict()

            if self.vid is not None:
                dictionary['vid'] = self.vid

            if self.weather is not None:
                dictionary['weather'] = self.weather

            if self.deleted is not None:
                dictionary['deleted'] = self.deleted.isoformat()

            if self.testing is not None:
                dictionary['testing'] = self.testing

            if self.replacement is not None:
                dictionary['replacement'] = self.replacement

            if self.tainted is not None:
                dictionary['tainted'] = self.tainted

            if self.annotation is not None:
                dictionary['annotation'] = self.annotation

            if self.serial_number is not None:
                dictionary['serial_number'] = self.serial_number

        return dictionary


class Synchronization(TerminalModel):
    """Synchronization log.

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
    def start(cls, terminal, result=None):
        """Start a synchronization for this terminal."""
        sync = cls()
        sync.terminal = terminal
        sync.started = datetime.now()
        sync.result = result
        return sync

    def stop(self, force=False):
        """Stops the synchronization."""
        if force or self.result is not None:
            self.finished = datetime.now()
            self.save()
            return True

    def to_dict(self):
        """Returns a JSON-like dictionary."""
        dictionary = {
            'terminal': self.terminal.id,
            'started': str(self.started)}

        if self.finished is not None:
            dictionary['finished'] = str(self.finished)

        if self.reload is not None:
            dictionary['reload'] = self.reload

        if self.force is not None:
            dictionary['force'] = self.force

        if self.nocheck is not None:
            dictionary['nocheck'] = self.nocheck

        if self.result is not None:
            dictionary['result'] = self.result

        if self.annotation is not None:
            dictionary['annotation'] = self.annotation

        return dictionary


class Admin(TerminalModel):
    """Many-to-many mapping in-between
    Employees and terminal classes.
    """

    class Meta:
        db_table = 'admin'

    _name = CharField(16, db_column='name', null=True, default=None)
    employee = ForeignKeyField(
        Employee, db_column='employee', on_update='CASCADE',
        on_delete='CASCADE')
    _email = CharField(255, db_column='email', null=True, default=None)
    root = BooleanField(default=False)

    @property
    def name(self):
        """Returns a short name."""
        if self._name is None:
            return self.employee.surname

        return self._name

    @property
    def email(self):
        """Returns the admin's email."""
        if self._email is None:
            return self.employee.email

        return self._email

    def to_dict(self):
        """Returns a JSON-like dictionary."""
        return {
            'name': self.name,
            'email': self.email,
            'root': self.root}


class Statistics(Model):
    """Stores application access statistics."""

    class Meta:
        database = MySQLDatabase(
            CONFIG['statistics']['database'],
            host=CONFIG['statistics']['host'],
            user=CONFIG['statistics']['user'],
            passwd=CONFIG['statistics']['passwd'],
            closing=True)
        schema = database.database

    id = PrimaryKeyField()
    customer = IntegerField()
    tid = IntegerField(null=True, default=None)
    vid = IntegerField()
    document = CharField(255)
    timestamp = DateTimeField()

    @classmethod
    def latest(cls, terminal):
        """Returns the latest statistics
        record for the respective terminal.
        """
        for statistics in cls.select().limit(1).where(
                (cls.customer == terminal.cid) &
                (cls.tid == terminal.tid)).order_by(
                cls.timestamp.desc()):
            return statistics


class LatestStats(TerminalModel):
    """Stores the last statistics of the respective terminal."""

    class Meta:
        db_table = 'latest_stats'

    terminal = ForeignKeyField(Terminal, db_column='terminal')
    statistics = ForeignKeyField(Statistics, db_column='statistics', null=True)

    @classmethod
    def refresh(cls, terminal=None):
        """Refreshes the stats for the respective terminal."""
        if terminal is None:
            for terminal in Terminal:
                cls.refresh(terminal=terminal)
        else:
            try:
                current = cls.get(cls.terminal == terminal)
            except DoesNotExist:
                current = cls()
                current.terminal = terminal

            current.statistics = Statistics.latest(terminal)
            current.save()
