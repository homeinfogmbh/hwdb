"""Hardware database configuration."""

from functools import cache, partial
from ipaddress import ip_address, ip_network
from logging import getLogger

from configlib import load_config

from hwdb.types import IPAddress, IPNetwork


__all__ = [
    'LOGGER',
    'LOG_FORMAT',
    'get_config',
    'get_openvpn_network',
    'get_openvpn_server',
    'get_ping',
    'get_wireguard_network',
    'get_wireguard_server'
]


LOGGER = getLogger('hwdb')
LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
get_config = partial(cache(load_config), 'hwdb.conf')


def get_openvpn_network() -> IPNetwork:
    """Returns the OpenVPN network."""

    return ip_network(get_config().get('OpenVPN', 'network'))


def get_openvpn_server() -> IPAddress:
    """Returns the OpenVPN server address."""

    return ip_address(get_config().get('OpenVPN', 'server'))


def get_ping() -> str:
    """Returns the ping binary path."""

    return get_config().get('binaries', 'PING')


def get_wireguard_network() -> IPNetwork:
    """Returns the WireGuard network."""

    return ip_network(get_config().get('WireGuard', 'network'))


def get_wireguard_server() -> IPAddress:
    """Returns the WireGuard server address."""

    return ip_address(get_config().get('WireGuard', 'server'))
