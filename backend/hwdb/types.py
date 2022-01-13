"""Common types."""

from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network
from typing import Iterable, NamedTuple, Union


__all__ = ['IPAddress', 'IPNetwork', 'IPAddresses', 'IPSocket']


IPAddress = Union[IPv4Address, IPv6Address]
IPNetwork = Union[IPv4Network, IPv6Network]
IPAddresses = Iterable[IPAddress]


class IPSocket(NamedTuple):
    """Represents an IP socket."""

    ipaddress: IPAddress
    port: int

    def __str__(self):
        if isinstance(self.ipaddress, IPv6Address):
            return f'[{self.ipaddress}]:{self.port}'

        return f'{self.ipaddress}:{self.port}'
