"""Hardware ORM models."""

from hwdb.orm.deployment import Deployment
from hwdb.orm.display import Display
from hwdb.orm.openvpn import OpenVPN
from hwdb.orm.system import System
from hwdb.orm.wireguard import WireGuard


__all__ = [
    'MODELS',
    'create_tables',
    'Deployment',
    'Display',
    'OpenVPN',
    'System',
    'WireGuard'
]


MODELS = (Deployment, OpenVPN, WireGuard, System, Display)


def create_tables(models=MODELS):
    """Creates the respective tables."""

    for model in models:
        model.create_table()
