"""Digital signage systems."""

from __future__ import annotations
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import Iterator, NamedTuple, Optional, Union

from peewee import JOIN
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import Expression
from peewee import FixedCharField
from peewee import ForeignKeyField
from peewee import ModelSelect

from mdb import Address, Company, Customer
from peeweeplus import EnumField, IPv6AddressField

from hwdb.ansible import AnsibleMixin
from hwdb.config import LOGGER, get_wireguard_network
from hwdb.ctrl import RemoteControllerMixin
from hwdb.enumerations import OperatingSystem
from hwdb.iptools import get_address
from hwdb.orm.common import BaseModel
from hwdb.orm.deployment import Deployment
from hwdb.orm.group import Group
from hwdb.orm.mixins import DNSMixin
from hwdb.orm.openvpn import OpenVPN
from hwdb.types import IPAddress


__all__ = ['System', 'DeploymentChange', 'get_free_ipv6_address']


def get_free_ipv6_address() -> IPv6Address:
    """Returns a free IPv6 address."""

    return get_address(wireguard_network := get_wireguard_network(),
                       used=System.used_ipv6_addresses(),
                       reserved=[wireguard_network[0]])


# pylint: disable=R0901
class System(BaseModel, DNSMixin, RemoteControllerMixin, AnsibleMixin):
    """A physical computer system out in the field."""

    group = ForeignKeyField(
        Group, column_name='Group', backref='systems', on_delete='SET NULL',
        on_update='CASCADE', lazy_load=False)
    deployment = ForeignKeyField(
        Deployment, null=True, column_name='deployment', backref='systems',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    dataset = ForeignKeyField(
        Deployment, null=True, column_name='dataset', backref='data_systems',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    openvpn = ForeignKeyField(
        OpenVPN, null=True, column_name='openvpn', backref='systems',
        on_delete='SET NULL', on_update='CASCADE', lazy_load=False)
    ipv6address = IPv6AddressField(null=True, unique=True)
    pubkey = FixedCharField(44, null=True, unique=True)
    created = DateTimeField(default=datetime.now)
    configured = DateTimeField(null=True)
    fitted = BooleanField(default=False)
    operating_system = EnumField(OperatingSystem)
    monitor = BooleanField(null=True)
    serial_number = CharField(255, null=True)
    model = CharField(255, null=True)   # Hardware model.
    last_sync = DateTimeField(null=True)

    @classmethod
    def used_ipv6_addresses(cls) -> Iterator[IPv6Address]:
        """Yields used IPv6 addresses."""
        for system in cls.select().where(~(cls.ipv6address >> None)):
            yield system.ipv6address

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
        """Selects monitored systems."""
        return cls.select(cascade=True).where(cls.monitoring_cond())

    @classmethod
    def select(cls, *args, cascade: bool = False, **kwargs) -> ModelSelect:
        """Selects systems."""
        if not cascade:
            return super().select(*args, **kwargs)

        lpt_address = Address.alias()
        dataset = Deployment.alias()
        ds_customer = Customer.alias()
        ds_company = Company.alias()
        ds_address = Address.alias()
        ds_lpt_address = Address.alias()
        args = {
            cls, Group, Customer, Company, Deployment, Address, lpt_address,
            dataset, ds_customer, ds_company, ds_address, ds_lpt_address,
            OpenVPN, *args
        }
        return super().select(*args, **kwargs).join(
            # Group
            Group).join_from(
            # Deployment
            cls, Deployment, on=cls.deployment == Deployment.id,
            join_type=JOIN.LEFT_OUTER).join(
            Customer, join_type=JOIN.LEFT_OUTER).join(
            Company, join_type=JOIN.LEFT_OUTER).join_from(
            Deployment, Address, on=Deployment.address == Address.id,
            join_type=JOIN.LEFT_OUTER).join_from(
            Deployment, lpt_address,
            on=Deployment.lpt_address == lpt_address.id,
            join_type=JOIN.LEFT_OUTER).join_from(
            # Dataset
            cls, dataset, on=cls.dataset == dataset.id,
            join_type=JOIN.LEFT_OUTER).join(
            ds_customer, join_type=JOIN.LEFT_OUTER).join(
            ds_company, join_type=JOIN.LEFT_OUTER).join_from(
            dataset, ds_address, on=dataset.address == ds_address.id,
            join_type=JOIN.LEFT_OUTER).join_from(
            dataset, ds_lpt_address,
            on=dataset.lpt_address == ds_lpt_address.id,
            join_type=JOIN.LEFT_OUTER).join_from(
            # OpenVPN
            cls, OpenVPN, join_type=JOIN.LEFT_OUTER)

    @classmethod
    def undeploy_all(
            cls, deployment: Deployment, *,
            exclude: Optional[Union[System, int]] = None
    ) -> Iterator[DeploymentChange]:
        """Undeploy other systems."""
        condition = cls.deployment == deployment

        if exclude is not None:
            condition &= cls.id != exclude

        for system in cls.select().where(condition):
            LOGGER.info('Un-deploying #%i.', system.id)
            system.fitted = False
            yield DeploymentChange(system, system.deployment, None)
            system.deployment = None
            system.save()

    @property
    def ipv4address(self) -> IPv4Address:
        """Returns the OpenVPN IPv4 address."""
        return self.openvpn.ipv4address

    @property
    def ip_address(self) -> IPAddress:
        """Returns the system's IP address."""
        return self.ipv4address if self.pubkey is None else self.ipv6address

    @property
    def syncdep(self) -> Deployment:
        """Returns the deployment for synchronization."""
        return self.dataset or self.deployment

    def change_deployment(
            self, deployment: Deployment
    ) -> Optional[DeploymentChange]:
        """Changes the current deployment."""
        if deployment == self.deployment:
            return None

        if (old := self.deployment) is None:
            LOGGER.info('Initially deployed system at "%s".', deployment)
        else:
            LOGGER.info('Relocated system from "%s" to "%s".', old, deployment)

        self.deployment = deployment
        return DeploymentChange(self, old, deployment)

    def deploy(
            self, deployment: Optional[Deployment], *,
            exclusive: bool = False,
            fitted: bool = False
    ) -> Iterator[DeploymentChange]:
        """Locates a system at the respective deployment."""
        if exclusive and deployment is not None:
            yield from type(self).undeploy_all(deployment, exclude=self)

        if (change := self.change_deployment(deployment)) is not None:
            self.fitted = fitted and deployment is not None
            self.save()
            yield change

    def to_json(self, *, brief: bool = False, skip: set = frozenset(),
                **kwargs) -> dict:
        """Returns a JSON-like dictionary."""
        if brief:
            skip |= {'openvpn', 'ipv6address', 'pubkey', 'operator'}

        return super().to_json(skip=skip, **kwargs)


class DeploymentChange(NamedTuple):
    """Information about a changed deployment."""

    system: System
    old = Optional[Deployment] = None
    new = Optional[Deployment] = None
