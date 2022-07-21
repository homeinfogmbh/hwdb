"""System handling."""

from argparse import Namespace
from logging import getLogger
from typing import Iterable

from hwdb.exceptions import TerminalConfigError
from hwdb.orm.openvpn import OpenVPN
from hwdb.orm.system import System


__all__ = ['add', 'dataset', 'deploy', 'toggle_updating']


LOGGER = getLogger('hwadm')


def add(args: Namespace) -> bool:
    """Adds a new system."""

    if args.key is not None:
        LOGGER.warning('Divergent OpenVPN key specified: "%s"!', args.key)

    try:
        openvpn = OpenVPN.generate(key=args.key, mtu=args.mtu)
    except TerminalConfigError as tce:
        LOGGER.error(tce)
        return False

    system = System(
        openvpn=openvpn, group=args.group,
        operating_system=args.operating_system,
        serial_number=args.serial_number, model=args.model
    )
    system.save()
    LOGGER.info('Added system: %i', system.id)
    return True


def dataset(args: Namespace) -> None:
    """Manage system dataset."""

    if args.remove:
        if args.dataset:
            LOGGER.warning('Dataset ignored when removing it.')

        args.system.dataset = None
        args.system.save()
        return

    if args.dataset:
        args.system.dataset = args.dataset
        args.system.save()
        return

    LOGGER.info("System's current dataset: %s", args.system.dataset)


def _undeploy(system: System) -> None:
    """Un-deploy a system."""

    for system, old, new in system.deploy(None):
        LOGGER.info(
            'Change deployment of system "%s" from "%s" to "%s"',
            system, old, new
        )


def _deploy(args: Namespace) -> None:
    """Deploy a system."""

    for system, old, new in args.system.deploy(
            args.deployment, exclusive=args.exclusive, fitted=args.fitted
    ):
        LOGGER.info(
            'Change deployment of system "%s" from "%s" to "%s"',
            system, old, new
        )


def _fit(system: System) -> None:
    """Mark the system as fitted."""

    system.fitted = True
    system.save()
    LOGGER.info('System marked as fitted.')


def deploy(args: Namespace) -> None:
    """Manage system deployment."""

    if args.remove:
        if args.deployment:
            LOGGER.warning('Deployment ignored when removing it.')

        _undeploy(args.system)
        return

    if args.deployment:
        _deploy(args)
        return

    if args.fitted:
        _fit(args.system)
        return

    LOGGER.info('System is currently deployed at: %s', args.system.deployment)


def toggle_updating(systems: Iterable[System]) -> None:
    """Toggle the updating flag on the given systems.."""

    for system in systems:
        system.updating = not system.updating
        system.save()
