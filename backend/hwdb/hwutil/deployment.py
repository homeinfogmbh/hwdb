"""Deployment actions."""

from logging import getLogger

from peewee import JOIN

from hwdb.exceptions import AmbiguityError, TerminalError
from hwdb.orm import Deployment, System
from hwdb.tools.common import iterprint
from hwdb.tools.deployment import get, listdep, printdep, DeploymentField


__all__ = ['find', 'list']


LOGGER = getLogger('hwutil')


def get_deployments(args):
    """Yields deployments selected by the CLI."""

    select = Deployment.select()
    condition = True

    if args.id:
        condition &= Deployment.id << args.id

    if args.customer:
        condition &= Deployment.customer << args.customer

    if args.testing is not None:
        condition &= Deployment.testing == bool(args.testing)

    if args.type:
        condition &= Deployment.type << args.type

    if args.connection:
        condition &= Deployment.connection << args.connection

    if args.system:
        dataset = System.alias()
        select = select.join(
            System, JOIN.LEFT_OUTER, on=Deployment.id == System.deployment
        ).join_from(
            Deployment, dataset, JOIN.LEFT_OUTER,
            on=Deployment.id == dataset.dataset
        )
        condition &= (System.id << args.system) | (dataset.id << args.system)

    return select.where(condition)


def find(args):
    """Finds a deployment."""

    try:
        deployment = get(
            args.pattern, house_number=args.house_number,
            annotation=args.pattern)
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

    if args.list_fields:
        return iterprint(field.value for field in DeploymentField)

    return iterprint(listdep(get_deployments(args), fields=args.fields))
