"""System related actions."""

from logging import getLogger

from hwdb.exceptions import AmbiguityError, TerminalError
from hwdb.orm import Deployment, System
from hwdb.tools.common import iterprint
from hwdb.tools.system import get, listsys, printsys


__all__ = ['find', 'list']


LOGGER = getLogger('hwutil')


def get_systems(args):
    """Yields systems selected by the CLI arguments."""

    select = System.select()
    condition = True

    if args.id:
        condition &= System.id << args.id

    if args.customer:
        select = select.join(Deployment)
        condition &= Deployment.customer << args.customer

    if args.deployment:
        condition &= System.deployment << args.deployment

    if args.deployed is not None:
        if args.deployed:
            condition &= ~(System.deployment >> None)
        else:
            condition &= System.deployment >> None

    if args.operating_system:
        condition &= System.operating_system << args.operating_system

    if args.manufacturer:
        condition &= System.manufacturer << args.manufacturer

    if args.configured is not None:
        condition &= System.configured == args.configured

    return select.where(condition)


def find(args):
    """Finds a system."""

    try:
        system = get(
            args.pattern, house_number=args.house_number,
            annotation=args.pattern)
    except AmbiguityError as ambiguous:
        LOGGER.warning('Ambiguous systems.')

        for system in ambiguous:
            printsys(system)

        return False
    except TerminalError as error:
        LOGGER.error(error)
        return False

    printsys(system)
    return True


def list(args):     # pylint: disable=W0622
    """Lists systems."""

    return iterprint(listsys(get_systems(args), fields=args.fields))
