"""OpenVPN connections."""

from __future__ import annotations

from peewee import CharField
from peewee import IntegerField

from peeweeplus import IPv4AddressField

from hwdb.config import get_openvpn_network
from hwdb.iptools import get_address, used_ipv4addresses
from hwdb.orm.common import BaseModel
from hwdb.types import IPAddress, IPNetwork


__all__ = ['OpenVPN']


def get_reserved_addresses(openvpn_network: IPNetwork) -> set[IPAddress]:
    """Returns reserved addresses."""

    return {addr for index, addr in enumerate(openvpn_network) if index <= 10}


class OpenVPN(BaseModel):
    """OpenVPN settings."""

    ipv4address = IPv4AddressField()
    key = CharField(36, null=True)
    mtu = IntegerField(null=True)

    def __str__(self):
        """Returns a human readable representation."""
        return str(self.ipv4address)

    @classmethod
    def generate(cls, key: str = None, mtu: int = None) -> OpenVPN:
        """Adds a record for the terminal."""
        ipv4address = get_address(
            openvpn_network := get_openvpn_network(),
            used=used_ipv4addresses(cls),
            reserved=get_reserved_addresses(openvpn_network)
        )
        record = cls(ipv4address=ipv4address, key=key, mtu=mtu)
        record.save()
        return record

    @property
    def filename(self) -> str:
        """Returns the CCD file name."""
        return self.key or str(self.id)
