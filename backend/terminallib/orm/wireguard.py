"""WireGuard configuration for terminals."""

from ipaddress import IPv4Address, IPv4Network
from pathlib import Path

from peewee import FixedCharField

from peeweeplus import IPv4AddressField, PasswordField
from wgtools import keypair     # pylint: disable=C0411

from terminallib.config import CONFIG
from terminallib.iptools import used_ipv4addresses, get_ipv4address
from terminallib.orm.common import BaseModel


__all__ = ['WireGuard']


NETWORK = IPv4Network(CONFIG['WireGuard']['network'])
SERVER = IPv4Address(CONFIG['WireGuard']['server'])
KEYS_DIR = Path('/usr/lib/terminals/keys')
PSK_FILE = KEYS_DIR.joinpath('terminals.psk')


class WireGuard(BaseModel):
    """WireGuard configuration."""

    ipv4address = IPv4AddressField()
    pubkey = FixedCharField(44)
    key = PasswordField(44)

    def __str__(self):
        """Returns a human readable representation."""
        return str(self.ipv4address)

    @classmethod
    def generate(cls):
        """Adds a new WireGuard configuration."""
        used = used_ipv4addresses(cls)
        ipv4address = get_ipv4address(NETWORK, used=used, reserved={SERVER})
        pubkey, key = keypair()
        record = cls(ipv4address=ipv4address, pubkey=pubkey, key=key)
        record.save()
        return record

    @property
    def psk(self):
        """Returns the pre-shared key."""
        with PSK_FILE.open('r') as file:
            return file.read().strip()
