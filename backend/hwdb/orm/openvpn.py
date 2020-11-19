"""OpenVPN connections."""

from __future__ import annotations

from peewee import CharField
from peewee import IntegerField

from peeweeplus import IPv4AddressField

from hwdb.config import OPENVPN_NETWORK
from hwdb.iptools import get_address, used_ipv4addresses
from hwdb.orm.common import BaseModel


__all__ = ['OpenVPN']


RESERVED = {addr for index, addr in enumerate(OPENVPN_NETWORK) if index <= 10}


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
            OPENVPN_NETWORK, used=used_ipv4addresses(cls), reserved=RESERVED)
        record = cls(ipv4address=ipv4address, key=key, mtu=mtu)
        record.save()
        return record

    @property
    def filename(self) -> str:
        """Returns the CCD file name."""
        return self.key or str(self.id)
