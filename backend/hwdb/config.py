"""Terminal setup configuration."""

from ipaddress import IPv4Address, IPv4Network
from logging import getLogger

from configlib import loadcfg


__all__ = [
    'CONFIG',
    'LOGGER',
    'LOG_FORMAT',
    'OPENVPN_NETBASE',
    'OPENVPN_NETMASK',
    'OPENVPN_NETWORK',
    'WIREGUARD_NETWORK',
    'WIREGUARD_SERVER'
]


CONFIG = loadcfg('hwdb.conf')
LOGGER = getLogger('hwdb')
LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
OPENVPN_NETBASE = CONFIG['OpenVPN']['network']
OPENVPN_NETMASK = CONFIG['OpenVPN']['netmask']
OPENVPN_NETWORK = IPv4Network(f'{OPENVPN_NETBASE}/{OPENVPN_NETMASK}')
WIREGUARD_NETWORK = IPv4Network(CONFIG['WireGuard']['network'])
WIREGUARD_SERVER = IPv4Address(CONFIG['WireGuard']['server'])
