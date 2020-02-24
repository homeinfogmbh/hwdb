"""WireGuard configuration for terminals."""

from ipaddress import IPv4Address, IPv4Network

from peewee import FixedCharField

from peeweeplus import IPv4AddressField

from terminallib.config import CONFIG
from terminallib.iptools import used_ipv4addresses, get_ipv4address
from terminallib.orm.common import BaseModel


__all__ = ['WireGuard']


NETWORK = IPv4Network(CONFIG['WireGuard']['network'])
SERVER = IPv4Address(CONFIG['WireGuard']['server'])


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
        ipv4address = get_ipv4address(NETWORK, used=used, reserved={SERVER})
        record = cls(ipv4address=ipv4address)
        record.save()
        return record
