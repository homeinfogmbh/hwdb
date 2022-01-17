"""System related actions."""

from argparse import Namespace
from logging import getLogger
from typing import Iterator

from hwdb.exceptions import AmbiguityError, TerminalError
from hwdb.filter import get_systems
from hwdb.orm.system import System
from hwdb.tools.common import iter_print
from hwdb.tools.system import get, listsys, printsys, SystemField


__all__ = ['find', 'list']


LOGGER = getLogger('hwutil')


def _get_systems(args: Namespace) -> Iterator[System]:
    """Yields systems selected by the CLI arguments."""

    return get_systems(
        ids=args.id, customers=args.customer, deployments=args.deployment,
        datasets=args.dataset, configured=args.configured,
        deployed=args.deployed, fitted=args.fitted,
        operating_systems=args.operating_system, groups=args.group, sort=True)


def find(args: Namespace) -> bool:
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


def list(args: Namespace) -> bool:
    """Lists systems."""

    if args.list_fields:
        return iter_print(field.value for field in SystemField)

    return iter_print(listsys(_get_systems(args), fields=args.fields))
