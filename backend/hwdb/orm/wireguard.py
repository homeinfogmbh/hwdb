"""WireGuard configuration for terminals."""

from peewee import FixedCharField

from peeweeplus import IPv4AddressField

from hwdb.config import WIREGUARD_NETWORK, WIREGUARD_SERVER
from hwdb.iptools import used_ipv4addresses, get_ipv4address
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
    def generate(cls):
        """Adds a new WireGuard configuration."""
        used = used_ipv4addresses(cls)
        ipv4address = get_ipv4address(
            WIREGUARD_NETWORK, used=used, reserved={WIREGUARD_SERVER})
        record = cls(ipv4address=ipv4address)
        record.save()
        return record
