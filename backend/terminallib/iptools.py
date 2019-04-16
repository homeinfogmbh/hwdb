"""Tools for IPv4 address pools handling."""

from terminallib.exceptions import TerminalConfigError


__all__ = ['used_ipv4addresses', 'get_ipv4address']


def used_ipv4addresses(model):
    """Yields all used IPv4 addresses."""

    for record in model:
        yield record.ipv4address


def get_ipv4address(network, used=frozenset(), reserved=frozenset()):
    """Returns a free IPv4Address.
    XXX: Beware of race conditions!
    """

    blacklist = used | reserved

    for ipv4address in network:
        if ipv4address not in blacklist:
            return ipv4address

    raise TerminalConfigError('Network exhausted!')
