"""Common types."""

from ipaddress import IPv4Address, IPv6Address, IPv4Network, IPv6Network
from typing import Iterable, Union


__all__ = ['IPAddress', 'IPNetwork', 'IPAddresses']


IPAddress = Union[IPv4Address, IPv6Address]
IPNetwork = Union[IPv4Network, IPv6Network]
IPAddresses = Iterable[IPAddress]
