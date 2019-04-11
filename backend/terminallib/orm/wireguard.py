"""WireGuard configuration for terminals."""

from pathlib import Path

from peewee import CharField, FixedCharField

from peeweeplus import IPv4AddressField
from wgtools import keypair

from terminallib.config import CONFIG
from terminallib.exceptions import TerminalConfigError
from terminallib.iptools import used_ipv4addresses, get_ipv4address
from terminallib.orm.common import BaseModel


__all__ = ['WireGuard']


NETWORK = CONFIG['WireGuard']['network']
SERVER = CONFIG['WireGuard']['server']
KEYS_DIR = Path('/usr/lib/terminals/keys')


class WireGuard(BaseModel):
    """WireGuard configuration."""

    ipv4address = IPv4AddressField()
    pubkey = FixedCharField(44)

    def __str__(self):
        """Returns a human readable representation."""
        return str(self.ipv4address)

    @classmethod
    def add(cls):
        """Adds a new WireGuard configuration."""
        record = cls()
        record.pubkey, record.key = keypair()
        record.ipv4address = get_ipv4address(
            NETWORK, used=used_ipv4addresses(cls), reserved={SERVER})
        record.save()
        return record

    @property
    def keyfile(self):
        """Returns the respective key file."""
        return KEYS_DIR.joinpath(str(self.id))

    @property
    def pskfile(self):
        """Returns the respective key file."""
        return KEYS_DIR.joinpath('terminals.psk')

    @property
    def key(self):
        """Returns the private key."""
        with self.keyfile.open('r') as file:
            return file.read().strip()

    @key.setter
    def key(self, key):
        """Sets the private key."""
        with self.keyfile.open('w') as file:
            return file.write(key)

    @property
    def psk(self):
        """Returns the pre-shared key."""
        with self.pskfile.open('r') as file:
            return file.read().strip()
