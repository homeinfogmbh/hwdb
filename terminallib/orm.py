"""Terminal library ORM models."""

from contextlib import suppress
from datetime import datetime, date
from ipaddress import IPv4Network, IPv4Address
from subprocess import DEVNULL, CalledProcessError, check_call

from peewee import BooleanField
from peewee import CharField
from peewee import DateField
from peewee import DateTimeField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import SmallIntegerField

from mdb import Customer, Address
from peeweeplus import CascadingFKField
from peeweeplus import IPv4AddressField
from peeweeplus import JSONModel
from peeweeplus import MySQLDatabase

from terminallib.config import CONFIG
from terminallib.csv import TerminalCSVRecord
from terminallib.exceptions import TerminalConfigError
from terminallib.exceptions import VPNUnconfiguredError


__all__ = [
    'Class',
    'Domain',
    'OS',
    'VPN',
    'LTEInfo',
    'Connection',
    'Terminal',
    'Synchronization',
    'ClassStakeholder']


NETWORK = IPv4Network('{}/{}'.format(
    CONFIG['net']['IPV4NET'], CONFIG['net']['IPV4MASK']))
CHECK_COMMAND = ('/bin/ping', '-c', '1', '-W')


class _TerminalModel(JSONModel):
    """Terminal manager basic Model."""

    class Meta:
        database = MySQLDatabase.from_config(CONFIG['terminalsdb'])
        schema = database.database


class Class(_TerminalModel):
    """Terminal classes."""

    name = CharField(32)
    full_name = CharField(32)
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
            return cls.get((cls.name == name) & (cls.touch == touch))
        except cls.DoesNotExist:
            return cls._add(name, full_name=full_name, touch=False)


class Domain(_TerminalModel):
    """Terminal domains."""

    # The domain's fully qualified domain name.
    fqdn = CharField(32)

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


class OS(_TerminalModel):
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


class VPN(_TerminalModel):
    """OpenVPN settings."""

    ipv4addr = IPv4AddressField()
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


class LTEInfo(_TerminalModel):
    """Represents information about LTE connections."""

    class Meta:
        table_name = 'lte_info'

    sim_id = CharField(32, null=True)
    pin = CharField(4, null=True)
    rssi = SmallIntegerField(null=True)


class Connection(_TerminalModel):
    """Internet connection information."""

    name = CharField(4)
    timeout = IntegerField()
    lte_info = ForeignKeyField(LTEInfo, null=True, column_name='lte_info')

    def __str__(self):
        """Returns name and timeout."""
        return '{} ({})'.format(self.name, self.timeout)


class Terminal(_TerminalModel):
    """A physical terminal out in the field."""

    tid = IntegerField()    # Customer-unique terminal identifier
    customer = ForeignKeyField(
        Customer, column_name='customer', on_update='CASCADE')
    class_ = ForeignKeyField(
        Class, null=True, column_name='class',
        on_delete='SET NULL', on_update='CASCADE')
    os = ForeignKeyField(
        OS, null=True, column_name='os',
        on_delete='SET NULL', on_update='CASCADE')
    connection = ForeignKeyField(
        Connection, null=True, column_name='connection',
        on_delete='SET NULL', on_update='CASCADE')
    vpn = ForeignKeyField(
        VPN, null=True, column_name='vpn', on_update='CASCADE')
    domain = ForeignKeyField(Domain, column_name='domain', on_update='CASCADE')
    address = ForeignKeyField(
        Address, null=True, column_name='address',
        on_delete='SET NULL', on_update='CASCADE')
    lpt_address = ForeignKeyField(  # Address for local public transport.
        Address, null=True, column_name='lpt_address',
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
        return '{}.{}'.format(self.tid, repr(self.customer))

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
        return cls.select().join(Customer).where(Customer.id == cid).order_by(
            Terminal.tid)

    @classmethod
    def by_ids(cls, cid, tid, deleted=False):
        """Get a terminal by customer id and terminal id."""
        if deleted:
            expression = True
        else:
            expression = cls.deleted >> None

        expression &= Customer.id == cid
        expression &= cls.tid == tid

        for terminal in cls.select().join(Customer).where(expression):
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
        tids = frozenset(cls.tids(customer))
        tid = 1

        while tid in tids:
            tid += 1

        return tid

    @classmethod
    def add(cls, customer, class_, os_, connection, vpn, domain, address=None,
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
        terminal.address = address
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

    @property
    def shortinfo(self):
        """Returns a short information e.g. for Nagios."""
        result = ' '.join((self.address.street, self.address.house_number))

        if self.annotation:
            result = ' - '.join((result, self.annotation))

        return result

    def deploy(self, date_time=None, force=False):
        """Sets terminals to deployed."""
        if self.deployed is None or force:
            deployed = datetime.now() if date_time is None else date_time
            self.deployed = deployed
            self.save()
            return deployed

        return self.deployed

    def undeploy(self, force=False):
        """Sets terminals to NOT deployed."""
        if self.deployed is not None or force:
            self.deployed = None
            self.save()

    def authorize(self, customer):
        """Authorizes the respective customer for this terminal."""
        if self.customer == customer:
            return True

        if self.customer.reseller == customer:
            return True

        with suppress(ClassStakeholder.DoesNotExist):
            ClassStakeholder.get(
                (ClassStakeholder.customer == customer)
                & (ClassStakeholder.class_ == self.class_))
            return True

        raise PermissionError('Customer {} may not access terminal {}.'.format(
            repr(customer), self))

    def to_json(self, *args, short=False, online_state=False, **kwargs):
        """Returns a JSON-like dictionary."""

        if short:
            dictionary = {
                'id': self.id,
                'tid': self.tid,
                'customer': self.customer.id}
        else:
            dictionary = super().to_json(*args, **kwargs)

        if online_state:
            dictionary['online'] = self.online

        address = self.address

        if address is not None:
            dictionary['address'] = address.to_json(*args, **kwargs)

        if short:
            return dictionary

        dictionary['customer'] = self.customer.to_json(
            *args, company=True, **kwargs)

        if self.class_ is not None:
            dictionary['class'] = self.class_.to_json(*args, **kwargs)

        if self.os is not None:
            dictionary['os'] = self.os.to_json(*args, **kwargs)

        dictionary['domain'] = self.domain.to_json(*args, **kwargs)

        if self.connection is not None:
            dictionary['connection'] = self.connection.to_json(
                *args, **kwargs)

        if self.vpn is not None:
            dictionary['vpn'] = self.vpn.to_json(*args, **kwargs)

        return dictionary

    def to_csv(self):
        """Returns a CSV record."""
        return TerminalCSVRecord.from_terminal(self)

    def delete_instance(self, **kwargs):
        """Removes the respective terminal."""
        if self.vpn is not None:
            self.vpn.delete_instance()

        return super().delete_instance(**kwargs)


class Synchronization(_TerminalModel):
    """Synchronization log.

    Recommended usage:

        with Synchronization.start(terminal) as sync:
            <do_sync_stuff>

            if sync_succeded:
                sync.status = True
            else:
                sync.status = False
    """

    terminal = CascadingFKField(Terminal, column_name='terminal')
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

    def to_json(self, *args, terminal=None, **kwargs):
        """Returns a JSON-ish dictionary."""
        dictionary = super().to_json(*args, **kwargs)

        if terminal is not None:
            dictionary['terminal'] = self.terminal.to_json(*args, **kwargs)

        return dictionary


class ClassStakeholder(_TerminalModel):
    """Mappings of customers that have access
    to terminals of certain classes.
    """

    class Meta:
        table_name = 'class_stakeholder'

    customer = ForeignKeyField(
        Customer, column_name='customer', on_delete='CASCADE')
    class_ = ForeignKeyField(Class, column_name='class', on_delete='CASCADE')
