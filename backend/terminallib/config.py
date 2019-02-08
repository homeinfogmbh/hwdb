"""Terminal setup configuration."""

from ipaddress import IPv4Network

from configlib import loadcfg


__all__ = ['CONFIG', 'WIREGUARD_NETWORK']


CONFIG = loadcfg('terminals.conf')
WIREGUARD_NETWORK = IPv4Network(CONFIG['wireguard']['network'])
WIREGUARD_SERVER = IPv4Network(CONFIG['wireguard']['server'])
