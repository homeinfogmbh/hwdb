"""Terminal database query utility."""

from logging import DEBUG, INFO, basicConfig, getLogger
from pathlib import Path
from sys import exit, stderr    # pylint: disable=W0622

from syslib import script

from terminallib.termutil.argparse import get_args
from terminallib.cli import ARNIE
from terminallib.cli import DEFAULT_FIELDS
from terminallib.cli import print_system
from terminallib.cli import get_system
from terminallib.cli import list_systems
from terminallib.exceptions import TerminalError, AmbiguousSystems
from terminallib.filter import get_systems


__all__ = ['main']


LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
LOGGER = getLogger(Path(__file__).name)


def _list_systems(args):
    """Lists systems."""

    fields = args.fields or DEFAULT_FIELDS

    systems = get_systems(
        args.id, customer=args.customer, deployed=args.deployed,
        testing=args.testing, oss=args.os, types=args.type)

    for line in list_systems(
            systems, header=not args.no_header, fields=fields,
            sep=args.separator):
        try:
            print(line, flush=True)
        except BrokenPipeError:
            stderr.close()
            break

    return 0


def _find_system(args):
    """Finds a system."""

    try:
        system = get_system(
            args.street, house_number=args.house_number,
            annotation=args.annotation)
    except AmbiguousSystems as ambiguous:
        LOGGER.warning('Ambiguous systems.')

        for system in ambiguous:
            print_system(system)

        return 1
    except TerminalError as error:
        LOGGER.error(error)
        return 2

    print_system(system)
    return 0


@script
def main():
    """Runs the system utility."""

    args = get_args()
    basicConfig(level=DEBUG if args.verbose else INFO, format=LOG_FORMAT)
    retval = 0

    if args.action == 'ls':
        if args.target == 'sys':
            retval = _list_systems(args)
        elif args.target == 'dep':
            LOGGER.error('Listing of deployments is not yet implemented.')
    elif args.action == 'find':
        if args.target == 'sys':
            retval = _find_system(args)
        elif args.target == 'dep':
            LOGGER.error('Finding deployments is not yet implemented.')
    elif args.action == 'CSM-101':
        print(ARNIE)

    exit(retval)
