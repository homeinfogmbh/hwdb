"""System handling."""

from logging import getLogger

from hwdb.exceptions import TerminalConfigError
from hwdb.orm.openvpn import OpenVPN
from hwdb.orm.system import System
from hwdb.orm.wireguard import WireGuard
from hwdb.system import root


__all__ = ['add', 'deploy', 'undeploy']


LOGGER = getLogger('hwadm')


@root(LOGGER)   # Needed to write WireGuard private keys.
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
