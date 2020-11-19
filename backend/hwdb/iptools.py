"""Tools for IPv4 address pools handling."""

from peewee import Model, ModelBase

from hwdb.exceptions import TerminalConfigError
from hwdb.types import IPAddress, IPAddresses, IPNetwork


__all__ = ['get_address', 'used_ipv4addresses']


def get_address(network: IPNetwork, used: IPAddresses = (),
                reserved: IPAddresses = ()) -> IPAddress:
    """Returns a free IPv4Address.
    XXX: Beware of race conditions!
    """

    blacklist = set(used) | set(reserved)

    for address in network:
        if address not in blacklist:
            return address

    raise TerminalConfigError('Network exhausted!')


def used_ipv4addresses(model: ModelBase) -> Model:
    """Yields all used IPv4 addresses."""

    for record in model:
        yield record.ipv4address
