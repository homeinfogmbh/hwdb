"""WireGuard configuration for terminals."""

from pathlib import Path

from peewee import CharField, FixedCharField

from peeweeplus import IPv4AddressField
from wgtools import keypair

from terminallib.config import CONFIG
from terminallib.exceptions import TerminalConfigError
from terminallib.orm.common import BaseModel


__all__ = ['WireGuard']


NETWORK = CONFIG['WireGuard']['network']
SERVER = CONFIG['WireGuard']['server']
KEYS = Path('/usr/lib/terminals/keys')


class WireGuard(BaseModel):
    """WireGuard configuration."""

    ipv4address = IPv4AddressField()
    pubkey = FixedCharField(44)
    psk = CharField(16, null=True)  # Name of the pre-shared key.

    @classmethod
    def add(cls):
        """Adds a new WireGuard configuration."""
        record = cls()
        record.pubkey, record.key = keypair()
        record.ipv4address = cls.genipv4address()
        record.save()
        return record

    @property
    def keyfile(self):
        """Returns the respective key file."""
        return KEYS.joinpath(str(self.id))

    @property
    def key(self):
        """Returns the private key."""
        with self.keyfile.open('r') as file:
            return file.read()

    @key.setter
    def key(self, key):
        """Sets the private key."""
        with self.keyfile.open('w') as file:
            return file.write(key)

    @classmethod
    def ipv4addresses(cls):
        """Yields all used IPv4 addresses."""
        for record in cls:
            yield record.ipv4address

    @classmethod
    def free_ipv4_address(cls):
        """Returns a free WireGuard IPv4Address.
        XXX: Beware of race conditions!
        """
        used = frozenset(cls.ipv4addresses())

        for ipv4address in NETWORK:
            if ipv4address not in used and ipv4address < SERVER:
                return ipv4address

        raise TerminalConfigError('Network exhausted!')
