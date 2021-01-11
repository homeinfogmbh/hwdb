"""Hardware ORM models."""

from hwdb.orm.deployment import Deployment
from hwdb.orm.display import Display
from hwdb.orm.generic import GenericHardware
from hwdb.orm.openvpn import OpenVPN
from hwdb.orm.smart_tv import SmartTV
from hwdb.orm.system import System
from hwdb.orm.wireguard import WireGuard


__all__ = [
    'MODELS',
    'create_tables',
    'Deployment',
    'Display',
    'GenericHardware',
    'OpenVPN',
    'SmartTV',
    'System',
    'WireGuard'
]


MODELS = (
    Deployment, SmartTV, OpenVPN, WireGuard, System, Display, GenericHardware
)


def create_tables(models=MODELS):
    """Creates the respective tables."""

    for model in models:
        model.create_table()
