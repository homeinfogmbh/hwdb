"""Hardware database configuration."""

from ipaddress import ip_address, ip_network
from logging import getLogger

from configlib import loadcfg


__all__ = [
    'CONFIG',
    'LOGGER',
    'LOG_FORMAT',
    'OPENVPN_NETWORK',
    'OPENVPN_SERVER',
    'WIREGUARD_NETWORK',
    'WIREGUARD_SERVER'
]


CONFIG = loadcfg('hwdb.conf')
LOGGER = getLogger('hwdb')
LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
OPENVPN_NETWORK = ip_network(CONFIG['OpenVPN']['network'])
OPENVPN_SERVER = ip_address(CONFIG['OpenVPN']['server'])
WIREGUARD_NETWORK = ip_network(CONFIG['WireGuard']['network'])
WIREGUARD_SERVER = ip_address(CONFIG['WireGuard']['server'])
