"""WireGuard configuration for terminals."""

from __future__ import annotations

from peewee import FixedCharField

from peeweeplus import IPv4AddressField

from hwdb.config import WIREGUARD_NETWORK, WIREGUARD_SERVER
from hwdb.iptools import get_address, used_ipv4addresses
from hwdb.orm.common import BaseModel


__all__ = ['WireGuard']


class WireGuard(BaseModel):
    """WireGuard configuration."""

    ipv4address = IPv4AddressField()
    pubkey = FixedCharField(44, null=True)

    def __str__(self):
        """Returns a human readable representation."""
        return str(self.ipv4address)

    @classmethod
    def generate(cls) -> WireGuard:
        """Adds a new WireGuard configuration."""
        record = cls(ipv4address=get_address(
            WIREGUARD_NETWORK, used=used_ipv4addresses(cls),
            reserved={WIREGUARD_SERVER})
        )
        record.save()
        return record
