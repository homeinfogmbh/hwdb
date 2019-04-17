"""OpenVPN connections."""

from ipaddress import IPv4Network

from peewee import CharField
from peewee import IntegerField

from peeweeplus import IPv4AddressField

from terminallib.config import CONFIG
from terminallib.iptools import used_ipv4addresses, get_ipv4address
from terminallib.orm.common import BaseModel


__all__ = ['OpenVPN']


NETBASE = CONFIG['OpenVPN']['network']
NETMASK = CONFIG['OpenVPN']['netmask']
NETWORK = IPv4Network('{}/{}'.format(NETBASE, NETMASK))
RESERVED = {addr for index, addr in enumerate(NETWORK) if index <= 10}


class OpenVPN(BaseModel):
    """OpenVPN settings."""

    ipv4address = IPv4AddressField()
    key = CharField(36, null=True)
    mtu = IntegerField(null=True)

    def __str__(self):
        """Returns a human readable representation."""
        return str(self.ipv4address)

    @classmethod
    def generate(cls, key=None, mtu=None):
        """Adds a record for the terminal."""
        used = used_ipv4addresses(cls)
        ipv4address = get_ipv4address(NETWORK, used=used, reserved=RESERVED)
        record = cls(ipv4address=ipv4address, key=key, mtu=mtu)
        record.save()
        return record
