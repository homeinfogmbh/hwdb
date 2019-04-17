"""Terminals ORM models."""

from terminallib.orm.deployment import Deployment
from terminallib.orm.openvpn import OpenVPN
from terminallib.orm.synchronization import Synchronization
from terminallib.orm.system import System
from terminallib.orm.wireguard import WireGuard


__all__ = [
    'MODELS',
    'create_tables',
    'Deployment',
    'OpenVPN',
    'Synchronization',
    'System',
    'WireGuard']


MODELS = (Deployment, OpenVPN, WireGuard, System, Synchronization)


def create_tables(models=MODELS):
    """Creates the respective tables."""

    for model in models:
        model.create_table()
