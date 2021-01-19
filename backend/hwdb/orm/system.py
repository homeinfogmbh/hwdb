"""Digital signage systems."""

from datetime import datetime
from ipaddress import IPv4Address

from peewee import JOIN
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import Expression
from peewee import ForeignKeyField
from peewee import ModelSelect

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

    operator = ForeignKeyField(
        Customer, column_name='operator', backref='systems',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    deployment = ForeignKeyField(
        Deployment, null=True, column_name='deployment', backref='systems',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    dataset = ForeignKeyField(
        Deployment, null=True, column_name='dataset', backref='data_systems',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    openvpn = ForeignKeyField(
        OpenVPN, null=True, column_name='openvpn', backref='systems',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    wireguard = ForeignKeyField(
        WireGuard, null=True, column_name='wireguard', backref='systems',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    created = DateTimeField(default=datetime.now)
    configured = DateTimeField(null=True)
    fitted = BooleanField(default=False)
    operating_system = EnumField(OperatingSystem)
    monitor = BooleanField(null=True)
    serial_number = CharField(255, null=True)
    model = CharField(255, null=True)   # Hardware model.
    last_sync = DateTimeField(null=True)

    @classmethod
    def monitoring_cond(cls) -> Expression:
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
    def monitored(cls) -> ModelSelect:
        """Yields monitored systems."""
        return cls.select().join(
            Deployment, join_type=JOIN.LEFT_OUTER,
            on=cls.deployment == Deployment.id).where(
            cls.monitoring_cond()
        )

    @classmethod
    def depjoin(cls, join_type: str = JOIN.INNER,   # pylint: disable=C0103
                on: Expression = None) -> ModelSelect:
        """Selects all columns and joins on the deployment."""
        if on is None:
            on = cls.deployment == Deployment.id

        return cls.select().join(Deployment, join_type=join_type, on=on)

    @classmethod
    def undeploy_all(cls, deployment: Deployment) -> list:
        """Undeploy other systems."""
        changes = []

        for system in cls.select().where(cls.deployment == deployment):
            LOGGER.info('Un-deploying #%i.', system.id)
            system.fitted = False
            system.deployment, old_deployment = None, system.deployment
            system.save()
            changes.append((system, old_deployment))

        return changes

    @property
    def ipv4address(self) -> IPv4Address:
        """Returns the WireGuard (preferred) or OpenVPN IPv4 address."""
        if self.wireguard and self.wireguard.pubkey:
            return self.wireguard.ipv4address

        return self.openvpn.ipv4address

    @property
    def syncdep(self) -> Deployment:
        """Returns the deployment for synchronization."""
        return self.dataset or self.deployment

    def deploy(self, deployment: Deployment, *, exclusive: bool = False,
               fitted: bool = False) -> list:
        """Locates a system at the respective deployment."""
        self.deployment, old_deployment = deployment, self.deployment

        if old_deployment is None:
            LOGGER.info('Initially deployed system at "%s".', deployment)
        elif old_deployment == deployment:
            LOGGER.info('System still deployed at "%s".', deployment)
        else:
            LOGGER.info('Relocated system from "%s" to "%s".',
                        old_deployment, deployment)

        changes = [(self, old_deployment)]

        if exclusive:
            changes += type(self).undeploy_all(deployment)

        self.fitted = fitted
        self.save()
        return changes

    def to_json(self, brief: bool = False, skip: set = None, **kwargs) -> dict:
        """Returns a JSON-like dictionary."""
        skip = set(skip) if skip else set()

        if brief:
            skip |= {'openvpn', 'wireguard', 'operator'}

        return super().to_json(skip=skip, **kwargs)
