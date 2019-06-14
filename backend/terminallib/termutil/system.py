"""System related actions."""

from logging import getLogger
from sys import stderr

from terminallib.tools.system import get, listsys, printsys
from terminallib.exceptions import AmbiguityError, TerminalError
from terminallib.orm.system import System


__all__ = ['find', 'list']


LOGGER = getLogger('termutil')


def get_systems(args):
    """Yields systems selected by the CLI arguments."""

    select = True

    if args.id:
        select &= System.id << args.id

    if args.deployment:
        select &= System.deployment << args.deployment

    if args.deployed is not None:
        if args.deployed:
            select &= ~(System.deployment >> None)
        else:
            select &= System.deployment >> None

    if args.operating_system:
        select &= System.operating_system << args.operating_system

    return System.select().where(select)


def find(args):
    """Finds a system."""

    try:
        system = get(
            args.street, house_number=args.house_number,
            annotation=args.annotation)
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

    fields = args.fields

    for line in listsys(
            get_systems(args), header=not args.no_header, fields=fields,
            sep=args.separator):
        try:
            print(line, flush=True)
        except BrokenPipeError:
            stderr.close()
            break

    return True
