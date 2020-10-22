"""System handling."""

from logging import getLogger

from hwdb.exceptions import TerminalConfigError
from hwdb.orm.openvpn import OpenVPN
from hwdb.orm.system import System
from hwdb.orm.wireguard import WireGuard
from hwdb.system import root


__all__ = ['add', 'dataset', 'deploy']


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
        openvpn=openvpn, wireguard=wireguard, operator=args.operator,
        operating_system=args.operating_system,
        serial_number=args.serial_number, model=args.model)
    system.save()
    LOGGER.info('Added system: %i', system.id)
    return True


def dataset(args):
    """Manage system dataset."""

    if args.remove:
        if args.dataset:
            LOGGER.warning('Dataset ignored when removing it.')

        args.system.dataset = None
        return args.system.save()

    if args.dataset:
        args.system.dataset = args.dataset
        return args.system.save()

    LOGGER.info("System's current dataset: %s", args.system.dataset)
    return True


def deploy(args):
    """Manage system deployment."""

    if args.remove:
        if args.deployment:
            LOGGER.warning('Deployment ignored when removing it.')

        return args.system.deploy(None)

    if args.deployment:
        return args.system.deploy(args.deployment)

    LOGGER.info('System is currently deployed at: %s', args.system.deployment)
    return True
