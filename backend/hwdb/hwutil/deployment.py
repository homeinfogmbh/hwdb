"""Deployment actions."""

from argparse import Namespace
from logging import getLogger
from typing import Iterator

from peewee import ModelSelect

from hwdb.exceptions import AmbiguityError, TerminalError
from hwdb.filter import get_deployments
from hwdb.tools.common import iter_print
from hwdb.tools.deployment import get, listdep, printdep, DeploymentField


__all__ = ["find", "list"]


LOGGER = getLogger("hwutil")


def _get_deployments(args: Namespace) -> ModelSelect:
    """Yields deployments selected by the CLI."""

    return get_deployments(
        ids=args.id,
        customers=args.customer,
        testing=args.testing,
        types=args.type,
        connections=args.connection,
        systems=args.system,
        sort=True,
    )


def find(args: Namespace) -> bool:
    """Finds a deployment."""

    try:
        deployment = get(
            args.pattern, house_number=args.house_number, annotation=args.pattern
        )
    except AmbiguityError as ambiguous:
        LOGGER.warning("Ambiguous deployments.")

        for deployment in ambiguous:
            printdep(deployment)

        return False
    except TerminalError as error:
        LOGGER.error(error)
        return False

    printdep(deployment)
    return True


def list(args: Namespace) -> bool:
    """Lists deployments."""

    if args.list_fields:
        return iter_print(field.value for field in DeploymentField)

    return iter_print(listdep(_get_deployments(args), fields=args.fields))
