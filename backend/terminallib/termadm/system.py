"""System handling."""

from logging import getLogger

from terminallib.exceptions import TerminalConfigError
from terminallib.orm.openvpn import OpenVPN
from terminallib.orm.system import System
from terminallib.orm.wireguard import WireGuard


__all__ = ['add', 'deploy', 'undeploy']


LOGGER = getLogger('termadm')


def add(args):
    """Adds a new system."""

    if args.key is not None:
        LOGGER.warning('Divergent OpenVPN key specified: "%s"!', args.key)

    try:
        openvpn = OpenVPN.generate(key=args.key, mtu=args.mtu)
    except TerminalConfigError as tce:
        LOGGER.error(tce)
        return False

    try:
        wireguard = WireGuard.generate()
    except TerminalConfigError as tce:
        LOGGER.error(tce)
        return False

    system = System(
        openvpn=openvpn, wireguard=wireguard, manufacturer=args.manufacturer,
        operating_system=args.operating_system,
        serial_number=args.serial_number, model=args.model)
    system.save()
    LOGGER.info('Added system: %i', system.id)
    return True


def deploy(args):
    """Deploys a system."""

    if args.system.deploy(args.deployment):
        return True

    return False


def undeploy(args):
    """Removed deployment of terminals."""

    for system in args.system:
        system.deploy(None)

    return True
