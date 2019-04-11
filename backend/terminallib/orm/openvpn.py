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
NETMASK = CONFIG['OpenVPN']['mask']
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
    def add(cls, key=None, mtu=None):
        """Adds a record for the terminal."""
        openvpn = cls()
        openvpn.ipv4address = get_ipv4address(
            NETWORK, used=used_ipv4addresses(cls), reserved=RESERVED)
        openvpn.key = key
        openvpn.mtu = mtu
        openvpn.save()
        return openvpn
