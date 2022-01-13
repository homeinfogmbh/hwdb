"""Common types."""

from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network
from typing import ForwardRef, Iterable, NamedTuple, Optional, Union


__all__ = [
    'DeploymentChange',
    'IPAddress',
    'IPNetwork',
    'IPAddresses',
    'IPSocket'
]


IPAddress = Union[IPv4Address, IPv6Address]
IPNetwork = Union[IPv4Network, IPv6Network]
IPAddresses = Iterable[IPAddress]


class DeploymentChange(NamedTuple):
    """Information about a changed deployment."""

    system: ForwardRef('System')
    old = Optional[ForwardRef('Deployment')] = None
    new = Optional[ForwardRef('Deployment')] = None


class IPSocket(NamedTuple):
    """Represents an IP socket."""

    ipaddress: IPAddress
    port: int

    def __str__(self):
        if isinstance(self.ipaddress, IPv6Address):
            return f'[{self.ipaddress}]:{self.port}'

        return f'{self.ipaddress}:{self.port}'
