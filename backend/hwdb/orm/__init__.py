"""Hardware ORM models."""

from hwdb.orm.deployment import Deployment, DeploymentTemp
from hwdb.orm.display import Display
from hwdb.orm.generic import GenericHardware
from hwdb.orm.group import Group
from hwdb.orm.openvpn import OpenVPN
from hwdb.orm.smart_tv import SmartTV
from hwdb.orm.system import System, get_free_ipv6_address


__all__ = [
    "MODELS",
    "create_tables",
    "get_free_ipv6_address",
    "Deployment",
    "DeploymentTemp",
    "Display",
    "GenericHardware",
    "Group",
    "OpenVPN",
    "SmartTV",
    "System",
]


MODELS = (Group, Deployment, SmartTV, OpenVPN, System, Display, GenericHardware)


def create_tables(models=MODELS):
    """Creates the respective tables."""

    for model in models:
        model.create_table()
