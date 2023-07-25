"""OpenVPN config generator."""

from ipaddress import ip_network
from logging import getLogger
from os import linesep
from pathlib import Path
from subprocess import CalledProcessError
from typing import Iterable

from hwdb.config import get_config, get_openvpn_network
from hwdb.exceptions import NoConnection
from hwdb.orm.openvpn import OpenVPN
from hwdb.orm.system import System
from hwdb.system import root, systemctl
from hwdb.types import IPNetwork


__all__ = ["openvpncfgen"]


LOGGER = getLogger("openvpn")
OPENVPN_SERVICE = "openvpn-server@terminals.service"
ROUTE = 'push "route {network.network_address} {network.netmask} {nexthop}"'
TEMPLATE = """# Generated by openvpncfg-gen.
# DO NOT EDIT THIS FILE MANUALLY!
# System ID: {id}
# OpenVPN ID: {vpn}
# Legacy key: {key}

ifconfig-push {ipaddress} {network.netmask}
push "route {network.network_address} {network.netmask}"
"""


def get_clients_dir() -> Path:
    """Returns the clients directory."""

    return Path(get_config().get("OpenVPN", "clients_dir"))


def get_routes() -> list[IPNetwork]:
    """Returns the OpenVPN routes."""

    return [
        ip_network(route) for route in get_config().get("OpenVPN", "routes").split()
    ]


def get_openvpn_config(system: System, openvpn: OpenVPN) -> str:
    """Returns the OpenVPN configuration for the respective system."""

    ipaddress = openvpn.ipv4address
    config = TEMPLATE.format(
        id=system.id,
        vpn=openvpn.id,
        key=openvpn.key,
        ipaddress=ipaddress,
        network=get_openvpn_network(),
    )

    for network in get_routes():
        config += ROUTE.format(network=network, nexthop=ipaddress) + linesep

    return config


def write_config_file(system: System):
    """Returns the OpenVPN configuration for the respective system."""

    openvpn = system.openvpn

    if openvpn is None:
        raise NoConnection()

    with get_clients_dir().joinpath(openvpn.filename).open("w") as cfg:
        cfg.write(get_openvpn_config(system, openvpn))


def write_config_files(systems: Iterable[System]):
    """Generates the respective configuration files."""

    for system in systems:
        try:
            write_config_file(system)
        except NoConnection:
            LOGGER.error("System %i has no VPN configuration.", system.id)


def remove_config_files():
    """Removes all existing client config files."""

    for file in get_clients_dir().glob("*"):
        if file.is_file():
            file.unlink()


@root(LOGGER)
def openvpncfgen() -> bool:
    """Runs the OpenVPN config generator."""

    LOGGER.info("Generating configuration.")
    remove_config_files()
    write_config_files(System.select(cascade=True).where(True))

    try:
        systemctl("restart", OPENVPN_SERVICE)
    except CalledProcessError:
        return False

    return True
