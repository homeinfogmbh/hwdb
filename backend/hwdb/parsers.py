"""Type-like functions for argparse."""

from datetime import date as Date, datetime
from logging import Logger, getLogger
from typing import Callable, Iterable, Optional

from mdb import Customer

from hwdb.enumerations import from_string
from hwdb.enumerations import Connection
from hwdb.enumerations import DeploymentType
from hwdb.enumerations import OperatingSystem
from hwdb.hooks import HOOKS
from hwdb.orm import Deployment, Group, System


__all__ = [
    'connection',
    'customer',
    'date',
    'deployment',
    'group',
    'hook',
    'operating_system',
    'system',
    'systems',
    'deployment_type'
]


def connection(name: str) -> Connection:
    """Returns a connection."""

    return from_string(Connection, name)


def customer(string: str) -> Customer:
    """Returns the respective customer."""

    try:
        return Customer.find(string).get()
    except Customer.DoesNotExist:
        raise ValueError('No such customer.') from None


def date(string: str) -> Date:
    """Parses a date."""

    return datetime.strptime(string, '%Y-%m-%d').date()


def deployment(ident: str) -> Deployment:
    """Returns the respective deployment."""

    try:
        return Deployment.select(cascade=True).where(
            Deployment.id == ident).get()
    except Deployment.DoesNotExist:
        raise ValueError('No such deployment.') from None


def group(ident: str) -> Group:
    """Returns the respective group."""

    try:
        return Group.select().where(
            (Group.id == ident) | (Group.name ** ident))
    except Group.DoesNotExist:
        raise ValueError('No such group.') from None


def hook(name: str) -> Callable:
    """Returns the respective hook."""

    try:
        return HOOKS[name]
    except KeyError:
        raise ValueError('No such hook.') from None


def operating_system(name: Optional[str] = None, *,
                     fallback: Optional[OperatingSystem] = None
                     ) -> OperatingSystem:
    """Returns a connection."""

    if name is None and fallback is not None:
        return fallback

    return from_string(OperatingSystem, name)


def system(ident: str) -> System:
    """Returns the respective system."""

    try:
        return System.select(cascade=True).where(System.id == ident).get()
    except System.DoesNotExist:
        raise ValueError('No such system.') from None


def systems(
        idents: Iterable[int],
        *,
        strict: bool = False,
        logger: Logger = getLogger(__file__)
) -> Iterable[System]:
    """Returns the respective systems."""

    records = System.select(cascade=True).where(
        System.id << (idents := set(idents))
    )

    for ident in (missing := idents - {sys.id for sys in records}):
        if strict:
            raise ValueError('No such systems:', missing)

        logger.warning('No such system: %i', ident)

    return records


def deployment_type(string: str) -> DeploymentType:
    """Returns a connection."""

    return from_string(DeploymentType, string)
