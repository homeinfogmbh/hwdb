"""Terminal database query utility."""

from logging import DEBUG, INFO, basicConfig, getLogger
from pathlib import Path
from sys import exit, stderr    # pylint: disable=W0622

from syslib import script

from terminallib.termutil.argparse import get_args
from terminallib.cli import ARNIE
from terminallib.cli.deployment import DEFAULT_FIELDS as DEPLOYMENT_FIELDS
from terminallib.cli.deployment import print_deployment
from terminallib.cli.deployment import get_deployment
from terminallib.cli.deployment import list_deployments
from terminallib.cli.system import DEFAULT_FIELDS as SYSTEM_FIELDS
from terminallib.cli.system import print_system
from terminallib.cli.system import get_system
from terminallib.cli.system import list_systems
from terminallib.exceptions import TerminalError, AmbiguityError
from terminallib.filter import get_deployments, get_systems


__all__ = ['main']


LOG_FORMAT = '[%(levelname)s] %(name)s: %(message)s'
LOGGER = getLogger(Path(__file__).name)


def _list_deployments(args):
    """Lists deployments."""

    fields = args.fields or DEPLOYMENT_FIELDS

    deployments = get_deployments(
        args.id, customer=args.customer, testing=args.testing,
        types=args.type, connections=args.connection)

    for line in list_deployments(
            deployments, header=not args.no_header, fields=fields,
            sep=args.separator):
        try:
            print(line, flush=True)
        except BrokenPipeError:
            stderr.close()
            break

    return 0


def _find_deployment(args):
    """Finds a deployment."""

    try:
        deployment = get_deployment(
            args.street, house_number=args.house_number,
            annotation=args.annotation)
    except AmbiguityError as ambiguous:
        LOGGER.warning('Ambiguous deployments.')

        for deployment in ambiguous:
            print_deployment(deployment)

        return 1
    except TerminalError as error:
        LOGGER.error(error)
        return 2

    print_deployment(deployment)
    return 0


def _list_systems(args):
    """Lists systems."""

    fields = args.fields or SYSTEM_FIELDS

    systems = get_systems(
        args.id, deployments=args.deployment, deployed=args.deployed,
        oss=args.os)

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
    except AmbiguityError as ambiguous:
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
            retval = _list_deployments(args)
    elif args.action == 'find':
        if args.target == 'sys':
            retval = _find_system(args)
        elif args.target == 'dep':
            retval = _find_deployment(args)
    elif args.action == 'CSM-101':
        print(ARNIE)

    exit(retval)
