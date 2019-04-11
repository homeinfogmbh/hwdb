"""OpenVPN connections."""

from ipaddress import IPv4Network, IPv4Address

from peewee import CharField
from peewee import IntegerField

from peeweeplus import IPv4AddressField

from terminallib.config import CONFIG
from terminallib.exceptions import TerminalConfigError

from terminallib.orm.common import BaseModel


__all__ = ['OpenVPN']


NETWORK = IPv4Network('{}/{}'.format(
    CONFIG['OpenVPN']['network'], CONFIG['OpenVPN']['mask']))


class OpenVPN(BaseModel):
    """OpenVPN settings."""

    ipv4addr = IPv4AddressField()
    key = CharField(36, null=True)
    mtu = IntegerField(null=True)

    @classmethod
    def add(cls, ipv4addr=None, key=None, mtu=None):
        """Adds a record for the terminal."""
        openvpn = cls()
        openvpn.ipv4addr = cls.generate_ipv4_address(desired=ipv4addr)
        openvpn.key = key
        openvpn.mtu = mtu
        openvpn.save()
        return openvpn

    @classmethod
    def used_ipv4_addresses(cls):
        """Yields used IPv4 addresses."""
        for openvpn in cls:
            yield openvpn.ipv4addr

    @classmethod
    def free_ipv4_addresses(cls):
        """Yields availiable IPv4 addresses."""
        used = tuple(cls.used_ipv4_addresses())
        lowest = None

        for ipv4addr in NETWORK:
            if lowest is None:
                lowest = ipv4addr + 10
            elif ipv4addr >= lowest:
                if ipv4addr not in used:
                    yield ipv4addr

    @classmethod
    def generate_ipv4_address(cls, desired=None):
        """Generates a unique IPv4 address."""
        if desired is not None:
            ipv4addr = IPv4Address(desired)

            if ipv4addr in cls.free_ipv4_addresses():
                return ipv4addr

            raise ValueError('IPv4 address {} is already in use.'.format(
                ipv4addr))

        for ipv4addr in cls.free_ipv4_addresses():
            return ipv4addr

        raise TerminalConfigError('Network exhausted!')
