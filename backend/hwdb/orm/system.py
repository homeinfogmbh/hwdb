"""Digital signage systems."""

from datetime import datetime

from peewee import JOIN
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField

from mdb import Customer
from peeweeplus import EnumField

from hwdb.ansible import AnsibleMixin
from hwdb.config import LOGGER
from hwdb.ctrl import RemoteControllerMixin
from hwdb.enumerations import OperatingSystem
from hwdb.orm.common import BaseModel
from hwdb.orm.deployment import Deployment
from hwdb.orm.mixins import DNSMixin
from hwdb.orm.openvpn import OpenVPN
from hwdb.orm.wireguard import WireGuard


__all__ = ['System']


# pylint: disable=R0901
class System(BaseModel, DNSMixin, RemoteControllerMixin, AnsibleMixin):
    """A physical computer system out in the field."""

    deployment = ForeignKeyField(
        Deployment, null=True, column_name='deployment', backref='systems',
        on_delete='SET NULL', on_update='CASCADE')
    dataset = ForeignKeyField(
        Deployment, null=True, column_name='dataset', backref='data_systems',
        on_delete='SET NULL', on_update='CASCADE')
    openvpn = ForeignKeyField(
        OpenVPN, null=True, column_name='openvpn', backref='systems',
        on_delete='SET NULL', on_update='CASCADE')
    wireguard = ForeignKeyField(
        WireGuard, null=True, column_name='wireguard', backref='systems',
        on_delete='SET NULL', on_update='CASCADE')
    operator = ForeignKeyField(
        Customer, null=True, column_name='operator', backref='systems',
        on_delete='SET NULL', on_update='CASCADE')
    created = DateTimeField(default=datetime.now)
    configured = DateTimeField(null=True)
    fitted = BooleanField(default=False)
    operating_system = EnumField(OperatingSystem)
    monitor = BooleanField(null=True)
    serial_number = CharField(255, null=True)
    model = CharField(255, null=True)   # Hardware model.
    last_sync = DateTimeField(null=True)

    @classmethod
    def monitoring_cond(cls):
        """Returns the condition for monitored systems."""
        return (
            (
                (cls.monitor == 1)              # Monitoring is force-enabled.
            ) | (
                (cls.monitor >> None)           # Monitoring is not disabled.
                & (Deployment.testing == 0)     # Not a testing system.
                & (~(cls.deployment >> None))   # System has a deployment.
                & (cls.fitted == 1)             # System is fitted.
            )
        )

    @classmethod
    def monitored(cls):
        """Yields monitored systems."""
        return cls.depjoin(join_type=JOIN.LEFT_OUTER).where(
            cls.monitoring_cond())

    @classmethod
    def depjoin(cls, join_type=JOIN.INNER, on=None):    # pylint: disable=C0103
        """Selects all columns and joins on the deployment."""
        if on is None:
            on = cls.deployment == Deployment.id

        return cls.select().join(Deployment, join_type=join_type, on=on)

    @classmethod
    def undeploy_all(cls, deployment):
        """Undeploy other systems."""
        for system in cls.select().where(cls.deployment == deployment):
            LOGGER.info('Un-deploying #%i.', system.id)
            system.fitted = False
            system.deployment = None
            system.save()

    @property
    def ipv4address(self):
        """Returns the WireGuard (preferred) or OpenVPN IPv4 address."""
        if self.wireguard and self.wireguard.pubkey:
            return self.wireguard.ipv4address

        return self.openvpn.ipv4address

    @property
    def syncdep(self):
        """Returns the deployment for synchronization."""
        return self.dataset or self.deployment

    def deploy(self, deployment, *, exclusive=False, fitted=False):
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
            type(self).undeploy_all(deployment)

        self.fitted = fitted
        return self.save()

    def to_json(self, brief=False, skip=None, **kwargs):
        """Returns a JSON-like dictionary."""
        skip = set(skip) if skip else set()

        if brief:
            skip |= {'openvpn', 'wireguard', 'manufacturer'}

        return super().to_json(skip=skip, **kwargs)
