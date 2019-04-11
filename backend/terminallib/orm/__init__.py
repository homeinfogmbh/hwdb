"""Terminals ORM models."""

from terminallib.orm.location import Location
from terminallib.orm.openvpn import OpenVPN
from terminallib.orm.stakeholders import TypeStakeholder
from terminallib.orm.synchronization import Synchronization
from terminallib.orm.system import System
from terminallib.orm.wireguard import WireGuard


__all__ = [
    'Location',
    'OpenVPN',
    'Synchronization',
    'System',
    'TypeStakeholder',
    'WireGuard']
