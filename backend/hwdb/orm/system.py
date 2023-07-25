"""Digital signage systems."""

from __future__ import annotations
from datetime import datetime
from ipaddress import IPv4Address, IPv6Address
from typing import Iterator, Optional

from peewee import JOIN
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import FixedCharField
from peewee import ForeignKeyField
from peewee import IntegerField
from peewee import Select

from mdb import Address, Company, Customer
from peeweeplus import EnumField, IPv6AddressField

from hwdb.ansible import AnsibleMixin
from hwdb.config import get_wireguard_network
from hwdb.ctrl import RemoteControllerMixin
from hwdb.enumerations import OperatingSystem
from hwdb.iptools import get_address
from hwdb.orm.common import BaseModel
from hwdb.orm.deployment import Deployment
from hwdb.orm.group import Group
from hwdb.orm.mixins import DeployingMixin, DNSMixin, MonitoringMixin
from hwdb.orm.openvpn import OpenVPN
from hwdb.types import IPAddress


__all__ = ["System", "get_free_ipv6_address"]


def get_free_ipv6_address() -> IPv6Address:
    """Returns a free IPv6 address."""

    return get_address(
        wireguard_network := get_wireguard_network(),
        used=System.used_ipv6_addresses(),
        reserved=[wireguard_network[0]],
    )


class System(
    BaseModel,
    DeployingMixin,
    DNSMixin,
    MonitoringMixin,
    RemoteControllerMixin,
    AnsibleMixin,
):
    """A physical computer system out in the field."""

    group = ForeignKeyField(
        Group,
        column_name="group",
        backref="systems",
        on_delete="SET NULL",
        on_update="CASCADE",
        lazy_load=False,
    )
    deployment = ForeignKeyField(
        Deployment,
        null=True,
        column_name="deployment",
        backref="systems",
        on_delete="SET NULL",
        on_update="CASCADE",
        lazy_load=False,
    )
    typo3_deployment_uid = IntegerField(null=True)
    dataset = ForeignKeyField(
        Deployment,
        null=True,
        column_name="dataset",
        backref="data_systems",
        on_delete="SET NULL",
        on_update="CASCADE",
        lazy_load=False,
    )
    openvpn = ForeignKeyField(
        OpenVPN,
        null=True,
        column_name="openvpn",
        backref="systems",
        on_delete="SET NULL",
        on_update="CASCADE",
        lazy_load=False,
    )
    ipv6address = IPv6AddressField(null=True, unique=True)
    pubkey = FixedCharField(44, null=True, unique=True)
    created = DateTimeField(default=datetime.now)
    configured = DateTimeField(null=True)
    fitted = BooleanField(default=False)
    operating_system = EnumField(OperatingSystem)
    monitor = BooleanField(null=True)
    serial_number = CharField(255, null=True)
    model = CharField(255, null=True)  # Hardware model.
    last_sync = DateTimeField(null=True)
    updating = BooleanField(default=False)

    @classmethod
    def used_ipv6_addresses(cls) -> Iterator[IPv6Address]:
        """Yields used IPv6 addresses."""
        for system in cls.select().where(~(cls.ipv6address >> None)):
            yield system.ipv6address

    @classmethod
    def select(cls, *args, cascade: bool = False) -> Select:
        """Selects systems."""
        if not cascade:
            return super().select(*args)

        lpt_address = Address.alias()
        dataset = Deployment.alias()
        ds_customer = Customer.alias()
        ds_company = Company.alias()
        ds_address = Address.alias()
        ds_lpt_address = Address.alias()
        return (
            super()
            .select(
                cls,
                Group,
                Customer,
                Company,
                Deployment,
                Address,
                lpt_address,
                dataset,
                ds_customer,
                ds_company,
                ds_address,
                ds_lpt_address,
                OpenVPN,
                *args,
            )
            .join(
                # Group
                Group
            )
            .join_from(
                # Deployment
                cls,
                Deployment,
                on=cls.deployment == Deployment.id,
                join_type=JOIN.LEFT_OUTER,
            )
            .join(Customer, join_type=JOIN.LEFT_OUTER)
            .join(Company, join_type=JOIN.LEFT_OUTER)
            .join_from(
                Deployment,
                Address,
                on=Deployment.address == Address.id,
                join_type=JOIN.LEFT_OUTER,
            )
            .join_from(
                Deployment,
                lpt_address,
                on=Deployment.lpt_address == lpt_address.id,
                join_type=JOIN.LEFT_OUTER,
            )
            .join_from(
                # Dataset
                cls,
                dataset,
                on=cls.dataset == dataset.id,
                join_type=JOIN.LEFT_OUTER,
            )
            .join(ds_customer, join_type=JOIN.LEFT_OUTER)
            .join(ds_company, join_type=JOIN.LEFT_OUTER)
            .join_from(
                dataset,
                ds_address,
                on=dataset.address == ds_address.id,
                join_type=JOIN.LEFT_OUTER,
            )
            .join_from(
                dataset,
                ds_lpt_address,
                on=dataset.lpt_address == ds_lpt_address.id,
                join_type=JOIN.LEFT_OUTER,
            )
            .join_from(
                # OpenVPN
                cls,
                OpenVPN,
                join_type=JOIN.LEFT_OUTER,
            )
        )

    @property
    def ipv4address(self) -> IPv4Address:
        """Returns the OpenVPN IPv4 address."""
        return self.openvpn.ipv4address

    @property
    def ip_address(self) -> IPAddress:
        """Returns the system's IP address."""
        return self.ipv4address if self.pubkey is None else self.ipv6address

    @property
    def syncdep(self) -> Optional[Deployment]:
        """Returns the deployment for synchronization."""
        return self.dataset or self.deployment

    def to_json(
        self, *, brief: bool = False, skip: set = frozenset(), **kwargs
    ) -> dict:
        """Returns a JSON-like dictionary."""
        if brief:
            skip |= {"openvpn", "ipv6address", "pubkey", "operator"}

        return super().to_json(skip=skip, **kwargs)
