"""Terminal library ORM models"""

from datetime import datetime
from ipaddress import IPv4Network, IPv4Address, AddressValueError
from logging import getLogger

from peewee import Model, ForeignKeyField, IntegerField, CharField,\
    BigIntegerField, DoesNotExist, DateTimeField, BooleanField, PrimaryKeyField

from homeinfo.lib.misc import classproperty
from homeinfo.lib.system import run
from homeinfo.peewee import MySQLDatabase
from homeinfo.crm import Customer, Address, Employee

from .config import config

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
    'Admin']


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
            config.db['db'],
            host=config.db['host'],
            user=config.db['user'],
            passwd=config.db['passwd'],
            closing=True)
        schema = database.database


class Class(TerminalModel):
    """Terminal classes"""

    name = CharField(32)
    full_name = CharField(32)
    # Touch display flag
    touch = BooleanField()

    @classmethod
    def _add(cls, name, full_name=None, touch=False):
        """Forcibly adds a new class"""
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
        """Adds a terminal class"""
        try:
            return cls.get(
                (cls.name == name) &
                (cls.touch == touch))
        except DoesNotExist:
            return cls._add(name, full_name=None, touch=False)


class Domain(TerminalModel):
    """Terminal domains"""

    # The domain's fully qualified domain name
    _fqdn = CharField(32, db_column='fqdn')

    @classmethod
    def add(cls, fqdn):
        """Adds a domain with a certain FQDN"""
        try:
            return cls.get(cls._fqdn == fqdn)
        except DoesNotExist:
            domain = cls()
            domain.fqdn = fqdn
            domain.save()
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
        return '{name} {version}'.format(name=self.name, version=self.version)


class VPN(TerminalModel):
    """OpenVPN settings"""

    NETWORK = IPv4Network(
        '/'.join(
            (config.net['IPV4NET'],
             config.net['IPV4MASK'])))

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
        result = '{street} {house_number}, {zip_code} {city}'.format(
            street=self.address.street,
            house_number=self.address.house_number,
            zip_code=self.address.zip_code,
            city=self.address.city)

        if self.annotation:
            result += ' ({})'.format(self.annotation)

        return result

    @classmethod
    def _add(cls, address, annotation=None):
        """Forcibly adds a location record"""
        location = cls()
        location.address = address
        location.annotation = annotation
        location.save()
        return location

    @classmethod
    def add(cls, address, annotation=None):
        """Adds a unique location"""
        if annotation is None:
            try:
                return cls.get(
                    (cls.address == address) &
                    (cls.annotation >> None))
            except DoesNotExist:
                return cls._add(address)
        else:
            try:
                return cls.get(
                    (cls.address == address) &
                    (cls.annotation == annotation))
            except DoesNotExist:
                return cls._add(address, annotation=annotation)


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
    weather = CharField(16, null=True)
    scheduled = DateTimeField(null=True, default=None)
    deployed = DateTimeField(null=True, default=None)
    deleted = DateTimeField(null=True, default=None)
    testing = BooleanField(default=False)
    replacement = BooleanField(default=False)
    tainted = BooleanField(default=False)
    annotation = CharField(255, null=True, default=None)

    def __str__(self):
        """Converts the terminal to a unique string"""
        return '.'.join([str(ident) for ident in self.idents])

    @classproperty
    @classmethod
    def hosts(cls):
        """Yields entries for /etc/hosts"""
        for terminal in cls.select().where(True):
            yield '{ipv4addr}\t{hostname}'.format(
                ipv4addr=terminal.ipv4addr,
                hostname=terminal.hostname)

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
            if desired in cls.tids(cid):
                return cls.gen_tid(cid, desired=None)
            else:
                return desired

    @classmethod
    def min_tid(cls, customer):
        """Gets the lowest TID for the respective customer"""
        result = None

        for terminal in cls.select().where(cls.customer == customer):
            if result is None:
                result = terminal.tid
            else:
                result = min(result, terminal.tid)

        return result

    @classmethod
    def max_tid(cls, customer):
        """Gets the highest TID for the respective customer"""
        result = 0

        for terminal in cls.select().where(cls.customer == customer):
            result = max(result, terminal.tid)

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
            location=None, weather=None, annotation=None, tid=None):
        """Adds a new terminal"""
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
        return '{tid}.{cid}.{domain}'.format(
            tid=self.tid,
            cid=self.cid,
            domain=self.domain.name)

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
                street_houseno = '{street} {house_number}'.format(
                    street=address.street,
                    house_number=address.house_number)
            except (TypeError, ValueError):
                return None
            else:
                try:
                    zip_city = '{zip_code} {city}'.format(
                        zip_code=address.zip_code,
                        city=address.city)
                except (TypeError, ValueError):
                    return None
                else:
                    return '{street_houseno}, {zip_city}'.format(
                        street_houseno=street_houseno,
                        zip_city=zip_city)
        else:
            raise AddressUnconfiguredError()

    @property
    def online(self):
        """Determines whether the terminal is online

        XXX: This may take some time, so use it carefully.
        """
        if self.connection:
            chk_cmd = self._CHK_CMD.format(
                timeout=self.connection.timeout,
                host=self.hostname)

            if run(chk_cmd, shell=True):
                return True

        return False

    @property
    def status(self):
        """Determines the status of the terminal"""
        if not self.tainted:
            return self.online
        else:
            return False

    @property
    def due(self):
        """Determines whether the terminal is due for deployment"""
        if self.scheduled is not None:
            if self.scheduled <= datetime.now():
                return True

        return False

    @property
    def isdeployed(self):
        """Determines whether the terminal is deployed"""
        if self.deployed is not None:
            if self.deployed <= datetime.now():
                return True

        return False

    @property
    def productive(self):
        """Returns whether the system has been deployed and is non-testing"""
        return True if self.isdeployed and not self.testing else False

    def deploy(self, date_time=None, force=False):
        """Sets terminals to deployed"""
        if self.deployed is None or force:
            deployed = datetime.now() if date_time is None else date_time
            self.logger.info(
                'Deploying {terminal} on {date}'.format(
                    terminal=self, date=deployed))
            self.deployed = deployed
            self.save()
            return True
        else:
            self.logger.warning(
                '{terminal} has already been deployed on {date}'.format(
                    terminal=self, date=self.deployed))
            return False

    def undeploy(self, force=False):
        """Sets terminals to NOT deployed"""
        if self.deployed is not None or force:
            self.logger.info('Undeploying {terminal} from {date}'.format(
                terminal=self, date=self.deployed))
            self.deployed = None
            self.save()
            return True
        else:
            self.logger.warning('{terminal} is not deployed'.format(
                terminal=self))
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

    def stop(self, force=False):
        """Stops the synchronization"""
        if force or self.result is not None:
            self.finished = datetime.now()
            return self.save()


class Admin(TerminalModel):
    """Many-to-many mapping in-between
    Employees and terminal classes
    """

    class Meta:
        db_table = 'admin'

    _name = CharField(16, db_column='name', null=True, default=None)
    employee = ForeignKeyField(Employee, db_column='employee')
    _email = CharField(255, db_column='email', null=True, default=None)
    root = BooleanField(default=False)

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
