"""Terminal library ORM models."""

from datetime import datetime, date
from ipaddress import IPv4Network, IPv4Address
from subprocess import DEVNULL, CalledProcessError, check_call

from peewee import ForeignKeyField, IntegerField, CharField, BigIntegerField, \
    DateTimeField, DateField, BooleanField

from fancylog import LogLevel, Logger
from homeinfo.crm import Customer, Address, Employee
from peeweeplus import MySQLDatabase, JSONModel, CascadingFKField

from terminallib.config import CONFIG
from terminallib.misc import get_hostname

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


DATABASE = MySQLDatabase(
    CONFIG['terminals']['database'], host=CONFIG['terminals']['host'],
    user=CONFIG['terminals']['user'], passwd=CONFIG['terminals']['passwd'],
    closing=True)
NETWORK = IPv4Network('{}/{}'.format(
    CONFIG['net']['IPV4NET'], CONFIG['net']['IPV4MASK']))
CHECK_COMMAND = ('/bin/ping', '-c', '1', '-W')


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


class TerminalModel(JSONModel):
    """Terminal manager basic Model."""

    class Meta:
        database = DATABASE
        schema = database.database


class Class(TerminalModel):
    """Terminal classes."""

    name = CharField(32)
    full_name = CharField(32)
    touch = BooleanField()  # Touch display flag.

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
            return cls.get((cls.name == name) & (cls.touch == touch))
        except cls.DoesNotExist:
            return cls._add(name, full_name=full_name, touch=False)


class Domain(TerminalModel):
    """Terminal domains."""

    # The domain's fully qualified domain name
    fqdn = CharField(32, db_column='fqdn')

    @classmethod
    def add(cls, fqdn):
        """Adds a domain with a certain FQDN."""
        try:
            return cls.get(cls.fqdn_ == fqdn)
        except cls.DoesNotExist:
            domain = cls()
            domain.fqdn = fqdn
            domain.save()
            return domain

    @property
    def name(self):
        """Returns the domain name without trailing dot."""
        return self.fqdn.strip('.')


class OS(TerminalModel):
    """Operating systems."""

    family = CharField(8)
    name = CharField(16)
    version = CharField(16, null=True)

    def __str__(self):
        """Returns the family name."""
        return self.family

    def __repr__(self):
        """Returns the OS name and version."""
        return '{} {}'.format(self.name, self.version)

    @classmethod
    def search(cls, string):
        """Fuzzily searches an operating system by the given string."""
        return cls.select().where(
            (cls.family == string) | (cls.name == string)
            | (cls.version == string))


class VPN(TerminalModel):
    """OpenVPN settings."""

    ipv4addr_ = BigIntegerField(db_column='ipv4addr')
    key = CharField(36, null=True)
    mtu = IntegerField(null=True)

    @classmethod
    def add(cls, ipv4addr=None, key=None, mtu=None):
        """Adds a record for the terminal."""
        openvpn = cls()
        openvpn.ipv4addr = cls.generate_ipv4_address(desired=ipv4addr)
        openvpn.key = key
        openvpn.mtu = mtu
        openvpn.save()
        return openvpn

    @classmethod
    def used_ipv4_addresses(cls):
        """Yields used IPv4 addresses."""
        for openvpn in cls:
            yield openvpn.ipv4addr

    @classmethod
    def free_ipv4_addresses(cls):
        """Yields availiable IPv4 addresses."""
        used = tuple(cls.used_ipv4_addresses())
        lowest = None

        for ipv4addr in NETWORK:
            if lowest is None:
                lowest = ipv4addr + 10
            elif ipv4addr >= lowest:
                if ipv4addr not in used:
                    yield ipv4addr

    @classmethod
    def generate_ipv4_address(cls, desired=None):
        """Generates a unique IPv4 address."""
        if desired is not None:
            ipv4addr = IPv4Address(desired)

            if ipv4addr in cls.free_ipv4_addresses():
                return ipv4addr

            raise ValueError('IPv4 address {} is already in use.'.format(
                ipv4addr))

        for ipv4addr in cls.free_ipv4_addresses():
            return ipv4addr

        raise TerminalConfigError('Network exhausted!')

    @property
    def ipv4addr(self):
        """Returns an IPv4 Address."""
        return IPv4Address(self.ipv4addr_)

    @ipv4addr.setter
    def ipv4addr(self, ipv4addr):
        """Sets the IPv4 address."""
        self.ipv4addr_ = int(ipv4addr)

    def to_dict(self, *args, **kwargs):
        """Returns a JSON-like dictionary."""
        dictionary = super().to_dict(*args, **kwargs)
        dictionary['ipv4addr'] = str(self.ipv4addr)
        return dictionary


class Connection(TerminalModel):
    """Internet connection information."""

    name = CharField(4)
    timeout = IntegerField()

    def __str__(self):
        return '{} ({})'.format(self.name, self.timeout)


class Location(TerminalModel):
    """Location of a terminal."""

    address = CascadingFKField(Address, db_column='address')
    annotation = CharField(255, null=True)

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
        """Returns a unique one-liner with annotation."""
        if self.annotation:
            return self.oneliner + ' ({})'.format(self.annotation)

        return self.oneliner

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
        except cls.DoesNotExist:
            return cls._add(address, annotation=annotation)

    @property
    def oneliner(self):
        """Returns a unique one-liner."""
        return repr(self.address)

    @property
    def shortinfo(self):
        """Returns a short information e.g. for Nagios."""
        result = ' '.join((self.address.street, self.address.house_number))

        if self.annotation:
            result = ' - '.join((result, self.annotation))

        return result

    def to_dict(self, *args, address=True, **kwargs):
        """Returns a JSON-like dictionary."""
        dictionary = super().to_dict(*args, **kwargs)

        if address:
            dictionary['address'] = self.address.to_dict(*args, **kwargs)

        return dictionary


class Terminal(TerminalModel):
    """A physical terminal out in the field."""

    # Ping once
    _CHK_CMD = '/bin/ping -c 1 -W {timeout} {host}'
    logger = Logger('Terminal', level=LogLevel.SUCCESS)

    tid = IntegerField()    # Customer-unique terminal identifier
    customer = ForeignKeyField(
        Customer, db_column='customer', on_update='CASCADE')
    class_ = ForeignKeyField(
        Class, null=True, db_column='class',
        on_delete='SET NULL', on_update='CASCADE')
    os = ForeignKeyField(
        OS, null=True, db_column='os',
        on_delete='SET NULL', on_update='CASCADE')
    connection = ForeignKeyField(
        Connection, null=True, db_column='connection',
        on_delete='SET NULL', on_update='CASCADE')
    vpn = ForeignKeyField(
        VPN, null=True, db_column='vpn',
        on_delete='SET NULL', on_update='CASCADE')
    domain = ForeignKeyField(Domain, db_column='domain', on_update='CASCADE')
    location = ForeignKeyField(
        Location, null=True, db_column='location',
        on_delete='SET NULL', on_update='CASCADE')
    vid = IntegerField(null=True)
    weather = CharField(16, null=True)
    scheduled = DateField(null=True)
    deployed = DateTimeField(null=True)
    deleted = DateTimeField(null=True)
    testing = BooleanField(default=False)
    replacement = BooleanField(default=False)
    tainted = BooleanField(default=False)
    monitor = BooleanField(null=True)
    annotation = CharField(255, null=True)
    serial_number = CharField(255, null=True)

    def __str__(self):
        """Converts the terminal to a unique string."""
        return '{}.{}'.format(self.tid, self.subdomain)

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
        return cls.select().join(Customer).where(Customer.cid == cid).order_by(
            Terminal.tid)

    @classmethod
    def by_ids(cls, cid, tid, deleted=False):
        """Get a terminal by customer id and terminal id."""
        if deleted:
            deleted_sel = True
        else:
            deleted_sel = cls.deleted >> None

        for terminal in cls.select().join(Customer).where(
                (Customer.cid == cid) & (cls.tid == tid) & deleted_sel):
            return terminal

        raise cls.DoesNotExist()

    @classmethod
    def by_virt(cls, customer, vid):
        """Yields terminals of a customer that
        run the specified virtual terminal.
        """
        return cls.select().where(
            (cls.customer == customer) & (cls.vid == vid)).order_by(
                Terminal.tid)

    @classmethod
    def tids(cls, customer):
        """Yields used terminal IDs for a certain customer."""
        for terminal in cls.select().where(cls.customer == customer):
            yield terminal.tid

    @classmethod
    def gen_tid(cls, customer):
        """Generates a terminal ID."""
        tids = tuple(cls.tids(customer))
        tid = 1

        while tid in tids:
            tid += 1

        return tid

    @classmethod
    def add(cls, customer, class_, os_, connection, vpn, domain, location=None,
            weather=None, scheduled=None, testing=False, annotation=None,
            serial_number=None):
        """Adds a new terminal."""
        terminal = cls()
        terminal.tid = cls.gen_tid(customer)
        terminal.customer = customer
        terminal.class_ = class_
        terminal.os = os_
        terminal.connection = connection
        terminal.vpn = vpn
        terminal.domain = domain
        terminal.location = location
        terminal.vid = None
        terminal.weather = weather
        terminal.scheduled = scheduled
        terminal.deployed = None
        terminal.deleted = None
        terminal.testing = testing
        terminal.replacement = False
        terminal.annotation = annotation
        terminal.serial_number = serial_number
        terminal.save()
        return terminal

    @property
    def _check_command(self):
        """Returns the respective check command."""
        return CHECK_COMMAND + (str(self.connection.timeout), self.hostname)

    @property
    def subdomain(self):
        """Returns the respective subdomain."""
        return '.'.join(
            get_hostname(customer) for customer
            in self.customer.reselling_chain)

    @property
    def hostname(self):
        """Returns the terminal's host name."""
        return '{}.{}'.format(str(self), self.domain.name)

    @property
    def ipv4addr(self):
        """Returns an IPv4 Address."""
        if self.vpn is None:
            raise VPNUnconfiguredError()

        return self.vpn.ipv4addr

    @property
    def address(self):
        """Returns the terminal's address."""
        location = self.location

        if location is not None:
            return location.oneliner

        raise AddressUnconfiguredError()

    @property
    def online(self):
        """Determines whether the terminal is online.
        This may take some time, so use it carefully.
        """
        try:
            check_call(self._check_command, stdout=DEVNULL, stderr=DEVNULL)
        except (AttributeError, CalledProcessError):
            return False

        return True

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
        return self.scheduled is not None and self.scheduled <= date.today()

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

    def to_dict(self, *args, short=False, online_state=False, **kwargs):
        """Returns a JSON-like dictionary."""

        if short:
            dictionary = {
                'id': self.id,
                'tid': self.tid,
                'customer': self.customer.id}
        else:
            dictionary = super().to_dict(*args, **kwargs)

        if online_state:
            dictionary['online'] = self.online

        location = self.location

        if location is not None:
            dictionary['location'] = location.to_dict(*args, **kwargs)

        if short:
            return dictionary

        dictionary['customer'] = self.customer.to_dict(
            *args, company=True, **kwargs)

        if self.class_ is not None:
            dictionary['class'] = self.class_.to_dict(*args, **kwargs)

        if self.os is not None:
            dictionary['os'] = self.os.to_dict(*args, **kwargs)

        dictionary['domain'] = self.domain.to_dict(*args, **kwargs)

        if self.connection is not None:
            dictionary['connection'] = self.connection.to_dict(
                *args, **kwargs)

        if self.vpn is not None:
            dictionary['vpn'] = self.vpn.to_dict(*args, **kwargs)

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

    terminal = CascadingFKField(Terminal, db_column='terminal')
    started = DateTimeField()
    finished = DateTimeField(null=True)
    reload = BooleanField(null=True)
    force = BooleanField(null=True)
    nocheck = BooleanField(null=True)
    result = BooleanField(null=True)
    annotation = CharField(255, null=True)

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

        return False

    def to_dict(self, *args, terminal=None, **kwargs):
        """Returns a JSON-like dictionary."""
        dictionary = super().to_dict(*args, **kwargs)

        if terminal is None:
            dictionary['terminal'] = self.terminal.id
        elif terminal:
            dictionary['terminal'] = self.terminal.to_dict(*args, **kwargs)

        return dictionary


class Admin(TerminalModel):
    """Many-to-many mapping in-between
    Employees and terminal classes.
    """

    class Meta:
        db_table = 'admin'

    name_ = CharField(16, db_column='name', null=True)
    employee = CascadingFKField(Employee, db_column='employee')
    email_ = CharField(255, db_column='email', null=True)
    root = BooleanField(default=False)

    @property
    def name(self):
        """Returns a short name."""
        if self.name_ is None:
            return self.employee.surname

        return self.name_

    @property
    def email(self):
        """Returns the admin's email."""
        if self.email_ is None:
            return self.employee.email

        return self.email_

    def to_dict(self):
        """Returns a JSON-like dictionary."""
        return {
            'name': self.name,
            'email': self.email,
            'root': self.root}


class Statistics(JSONModel):
    """Stores application access statistics."""

    class Meta:
        database = MySQLDatabase(
            CONFIG['statistics']['database'],
            host=CONFIG['statistics']['host'],
            user=CONFIG['statistics']['user'],
            passwd=CONFIG['statistics']['passwd'],
            closing=True)
        schema = database.database

    customer = IntegerField()
    tid = IntegerField(null=True)
    vid = IntegerField()
    document = CharField(255)
    timestamp = DateTimeField()

    @classmethod
    def latest(cls, terminal):
        """Returns the latest statistics
        record for the respective terminal.
        """
        for statistics in cls.select().limit(1).where(
                (cls.customer == terminal.customer.id) &
                (cls.tid == terminal.tid)).order_by(
                    cls.timestamp.desc()):
            return statistics


class LatestStats(TerminalModel):
    """Stores the last statistics of the respective terminal."""

    class Meta:
        db_table = 'latest_stats'

    terminal = CascadingFKField(Terminal, db_column='terminal')
    statistics = CascadingFKField(
        Statistics, db_column='statistics', null=True)

    @classmethod
    def refresh(cls, terminal=None):
        """Refreshes the stats for the respective terminal."""
        if terminal is None:
            for terminal in Terminal:
                cls.refresh(terminal=terminal)
        else:
            try:
                current = cls.get(cls.terminal == terminal)
            except cls.DoesNotExist:
                current = cls()
                current.terminal = terminal

            current.statistics = Statistics.latest(terminal)
            current.save()
