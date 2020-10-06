"""System related actions."""

from logging import getLogger

from hwdb.exceptions import AmbiguityError, TerminalError
from hwdb.orm import Deployment, System
from hwdb.tools.common import iterprint
from hwdb.tools.system import get, listsys, printsys, SystemField


__all__ = ['find', 'list']


LOGGER = getLogger('hwutil')


def get_systems(args):  # pylint: disable=R0912
    """Yields systems selected by the CLI arguments."""

    select = System.depjoin() if args.customer else System.select()
    condition = True

    if args.id:
        condition &= System.id << args.id

    if args.customer:
        condition &= Deployment.customer << args.customer

    if args.deployment:
        condition &= System.deployment << args.deployment

    if args.dataset:
        condition &= System.dataset << args.dataset

    if args.configured is not None:
        if args.configured:
            condition &= ~(System.configured >> None)
        else:
            condition &= System.configured >> None

    if args.deployed is not None:
        if args.deployed:
            condition &= ~(System.deployment >> None)
        else:
            condition &= System.deployment >> None

    if args.fitted is not None:
        condition &= System.fitted == args.fitted

    if args.operating_system:
        condition &= System.operating_system << args.operating_system

    if args.manufacturer:
        condition &= System.manufacturer << args.manufacturer

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

    if args.list_fields:
        return iterprint(field.value for field in SystemField)

    return iterprint(listsys(get_systems(args), fields=args.fields))
