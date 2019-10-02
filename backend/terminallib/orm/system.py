"""Digital signage systems."""

from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField

from mdb import Customer
from peeweeplus import EnumField

from terminallib.config import CONFIG, LOGGER
from terminallib.ctrl import RemoteControllerMixin
from terminallib.enumerations import OperatingSystem
from terminallib.orm.common import BaseModel
from terminallib.orm.deployment import Deployment
from terminallib.orm.openvpn import OpenVPN
from terminallib.orm.wireguard import WireGuard


__all__ = ['System']


class System(BaseModel, RemoteControllerMixin):
    """A physical terminal out in the field."""

    deployment = ForeignKeyField(
        Deployment, null=True, column_name='deployment', backref='systems',
        on_delete='SET NULL', on_update='CASCADE')
    openvpn = ForeignKeyField(
        OpenVPN, null=True, column_name='openvpn', backref='systems',
        on_delete='SET NULL', on_update='CASCADE')
    wireguard = ForeignKeyField(
        WireGuard, null=True, column_name='wireguard', backref='systems',
        on_delete='SET NULL', on_update='CASCADE')
    manufacturer = ForeignKeyField(
        Customer, null=True, column_name='manufacturer', backref='systems',
        on_delete='SET NULL', on_update='CASCADE')
    created = DateTimeField(default=datetime.now)
    configured = DateTimeField(null=True)
    operating_system = EnumField(OperatingSystem)
    monitor = BooleanField(null=True)
    serial_number = CharField(255, null=True)
    model = CharField(255, null=True)   # Hardware model.

    @classmethod
    def monitored(cls):
        """Yields monitored systems."""
        explicit = System.monitor == 1
        implicit = System.monitor >> None
        implicit &= ~(System.deployment >> None)
        return cls.select().where(explicit | implicit)

    @property
    def vpn_hostname(self):
        """Returns a host name for the OpenVPN network."""
        domain = CONFIG['OpenVPN']['domain']
        return f'{self.id}.{domain}'

    @property
    def wg_hostname(self):
        """Returns the respective host name."""
        domain = CONFIG['WireGuard']['domain']
        return f'{self.id}.{domain}'

    def deploy(self, deployment, *, exclusive=False):
        """Locates a system at the respective deployment."""
        self.deployment, old_deployment = deployment, self.deployment

        if old_deployment is None:
            LOGGER.info('Initially deployed system at "%s".', deployment)
        elif old_deployment == deployment:
            LOGGER.info('System still deployed at "%s".', deployment)
        else:
            LOGGER.info('Relocated system from "%s" to "%s".',
                        old_deployment, deployment)

        if exclusive:
            model = type(self)

            for system in model.select().where(model.deployment == deployment):
                LOGGER.info('Un-deploying #%i.', system.id)
                system.deployment = None
                system.save()

        return self.save()

    def to_json(self, brief=False, skip=None, **kwargs):
        """Returns a JSON-like dictionary."""
        skip = set(skip) if skip else set()

        if brief:
            skip |= {'openvpn', 'wireguard', 'manufacturer'}

        return super().to_json(skip=skip, **kwargs)
