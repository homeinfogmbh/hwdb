"""Deployment actions."""

from logging import getLogger
from sys import stderr

from terminallib.exceptions import AmbiguityError, TerminalError
from terminallib.orm.deployment import Deployment
from terminallib.tools.deployment import get, listdep, printdep


__all__ = ['find', 'list']


LOGGER = getLogger('termutil')


def get_deployments(args):
    """Yields deployments selected by the CLI."""

    select = True

    if args.id:
        select &= Deployment.id << args.id

    if args.customer:
        select &= Deployment.customer << args.customer

    if args.testing is not None:
        select &= Deployment.testing == bool(args.testing)

    if args.type:
        select &= Deployment.type << args.type

    if args.connection:
        select &= Deployment.connection << args.connection

    return Deployment.select().where(select)


def find(args):
    """Finds a deployment."""

    try:
        deployment = get(
            args.street, house_number=args.house_number,
            annotation=args.annotation)
    except AmbiguityError as ambiguous:
        LOGGER.warning('Ambiguous deployments.')

        for deployment in ambiguous:
            printdep(deployment)

        return False
    except TerminalError as error:
        LOGGER.error(error)
        return False

    printdep(deployment)
    return True


def list(args):     # pylint: disable=W0622
    """Lists deployments."""

    fields = args.fields

    for line in listdep(
            get_deployments(args), header=not args.no_header, fields=fields,
            sep=args.separator):
        try:
            print(line, flush=True)
        except BrokenPipeError:
            stderr.close()
            break

    return True