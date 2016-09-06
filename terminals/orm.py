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
    'NagiosAdmin',
    'NagiosService',
    'AdminClassService',
    'TerminalService',
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
                return cls._add(address, location=location)
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
            location=None, annotation=None, tid=None):
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
        return chain(
            Administrator.root,
            AdministratorTerminals.operators(self))

    @property
    def status(self):
        """Determines the status of the terminal

        This may take some time, so use it carefully
        """
        if self.connection:
            chk_cmd = self._CHK_CMD.format(
                timeout=self.connection.timeout,
                host=self.hostname)

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


class NagiosAdmin(TerminalModel):
    """Many-to-many mapping in-between
    Employees and terminal classes
    """

    class Meta:
        db_table = 'nagios_admin'

    _name = CharField(16, db_column='name', null=True, default=None)
    employee = ForeignKeyField(Employee, db_column='employee')
    _email = CharField(255, db_column='email', null=True, default=None)
    root = BooleanField(default=False)
    service_notification_period = CharField(16, default='24x7')
    host_notification_period = CharField(16, default='24x7')
    service_notification_options = CharField(16, default='w,u,c,r')
    host_notification_options = CharField(16, default='d,r')
    service_notification_commands = CharField(
        64, default='notify-service-by-email')
    host_notification_commands = CharField(
        64, default='notify-terminal-by-email-with-id')

    def __str__(self):
        """Returns the respective nagios configuration as a string"""
        return '\n'.join(self.render())

    @classmethod
    def applicable(cls, class_, service=None):
        """Sieves out stakeholders among admins
        for the respective class and service
        """
        for admin_class_service in AdminClassService:
            if admin_class_service.class_ is None:
                if admin_class_service.service is None:
                    yield admin_class_service.admin
                elif service is not None:
                    if admin_class_service.service == service:
                        yield admin_class_service.admin
            elif admin_class_service.class_ == class_:
                if admin_class_service.service is None:
                    yield admin_class_service.admin
                elif service is not None:
                    if admin_class_service.service == service:
                        yield admin_class_service.admin

    def render(self):
        """Yields config file lines"""
        yield 'define contact {'
        yield '    contact_name                   {}'.format(self.name)
        yield '    alias                          {}'.format(self.employee)
        yield '    service_notification_period    {}'.format(
            self.service_notification_period)
        yield '    host_notification_period       {}'.format(
            self.host_notification_period)
        yield '    service_notification_options   {}'.format(
            self.service_notification_options)
        yield '    host_notification_options      {}'.format(
            self.host_notification_options)
        yield '    service_notification_commands  {}'.format(
            self.service_notification_commands)
        yield '    host_notification_commands     {}'.format(
            self.host_notification_commands)
        yield '    email                          {}'.format(self.email)
        yield '}'

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


class NagiosService(TerminalModel):
    """Represents a nagios service"""

    CHECK_COMMAND = 'check_{}!{{terminal.tid}}!{{terminal.customer.id}}'

    class Meta:
        db_table = 'nagios_service'

    name = CharField(16)
    description = CharField(255, null=True, default=None)
    url = CharField(255, null=True, default=None)
    max_check_attempts = IntegerField(default=5)
    check_interval = IntegerField(default=15)
    retry_interval = IntegerField(default=5)
    check_period = CharField(8, default='24x7')
    notification_interval = IntegerField(default=0)
    notification_period = CharField(8, default='24x7')
    icon_image = CharField(255, null=True, default=None)

    @classmethod
    def applicable(cls, terminal):
        """Yields services applicable for the respective terminal"""
        for terminal_service in TerminalService:
            if terminal_service.os is None:
                if terminal_service.class_ is None:
                    yield terminal_service.service
                elif terminal_service.class_ == terminal.class_:
                    yield terminal_service.service
            elif terminal_service.os == terminal.os:
                if terminal_service.class_ is None:
                    yield terminal_service.service
                elif terminal_service.class_ == terminal.class_:
                    yield terminal_service.service

    def render(self, terminal, contacts, contact_groups):
        """Render the service for the respective
        terminal, contacts and contact groups
        """
        if terminal is None:
            raise ValueError('No terminal provided')

        if contacts is not None:
            contacts = list(contacts)

        if contact_groups is not None:
            contact_groups = list(contact_groups)

        yield 'define service {'
        yield '    host_name              {}'.format(terminal.hostname)

        if self.description:
            yield '    service_description    {}'.format(self.description)

        yield '    check_command          {}'.format(
            self.check_command.format(terminal=terminal))
        yield '    max_check_attempts     {}'.format(self.max_check_attempts)
        yield '    check_interval         {}'.format(self.check_interval)
        yield '    retry_interval         {}'.format(self.retry_interval)
        yield '    check_period           {}'.format(self.check_period)
        yield '    notification_interval  {}'.format(
            self.notification_interval)
        yield '    notification_period    {}'.format(self.notification_period)

        if contacts:
            yield '    contacts               {}'.format(
                ','.join(contact.name for contact in contacts))

        if contact_groups:
            yield '    contact_groups         {}'.format(
                ','.join(contact_groups))

        yield '    notes                  {}'.format(repr(terminal.location))

        if self.icon_image:
            yield '    icon_image             {}'.format(self.icon_image)

        yield '}'

    @property
    def template(self):
        """Loads the respective template file"""
        template = join(config.monitoring['TEMPLATE_DIR'], self.name)

        with open(template, 'r') as f:
            return f.read()

    @property
    def check_command(self):
        """Returns the check command template"""
        return self.CHECK_COMMAND.format(self.name)


class AdminClassService(TerminalModel):
    """Many-to-many mapping between admins, terminals and services"""

    class Meta:
        db_table = 'admin_class_service'

    admin = ForeignKeyField(NagiosAdmin, db_column='admin')
    class_ = ForeignKeyField(Class, db_column='class', null=True, default=None)
    service = ForeignKeyField(
        NagiosService, db_column='service', null=True, default=None)

    @classmethod
    def sieve(cls, class_=None, service=None):
        """Sieves for classes and services"""
        if class_ is None and service is None:
            return cls
        elif class_ is None:
            return cls.select().where(cls.service == service)
        elif service is None:
            return cls.select().where(cls.class_ == class_)
        else:
            return cls.select().where(
                (cls.service == service) &
                (cls.class_ == class_))


class TerminalService(TerminalModel):
    """Many-to-many mapping for terminal services"""

    class Meta:
        db_table = 'terminal_service'

    service = ForeignKeyField(NagiosService, db_column='service')
    os = ForeignKeyField(OS, db_column='os', null=True, default=None)
    class_ = ForeignKeyField(Class, db_column='class', null=True, default=None)

    @classmethod
    def sieve(cls, class_=None, os=None):
        """Sieves for classes and OSs"""
        if class_ is None and os is None:
            return cls
        elif class_ is None:
            return cls.select().where(cls.os == os)
        elif os is None:
            return cls.select().where(cls.class_ == class_)
        else:
            return cls.select().where(
                (cls.os == os) &
                (cls.class_ == class_))


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
