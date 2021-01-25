"""Type-like functions for argparse."""

from datetime import date as Date, datetime
from typing import Callable

from peewee import JOIN

from mdb import Address, Company, Customer

from hwdb.enumerations import from_string
from hwdb.enumerations import Connection
from hwdb.enumerations import DeploymentType
from hwdb.enumerations import OperatingSystem
from hwdb.hooks import HOOKS
from hwdb.orm import Deployment, System


__all__ = [
    'connection',
    'customer',
    'date',
    'deployment',
    'hook',
    'operating_system',
    'system',
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

    lpt_address = Address.alias()
    select = Deployment.select(
        Deployment, Customer, Company, Address, lpt_address
    ).join(Deployment, Customer).join(Company).join_from(
        Deployment, Address, on=Deployment.address == Address.id
    ).join_from(
        Deployment, lpt_address, on=Deployment.lpt_address == lpt_address,
        join_type=JOIN.LEFT_OUTER
    )

    try:
        return select.where(Deployment.id == int(ident))
    except Deployment.DoesNotExist:
        raise ValueError('No such deployment.') from None


def hook(name: str) -> Callable:
    """Returns the respective hook."""

    try:
        return HOOKS[name]
    except KeyError:
        raise ValueError('No such hook.') from None


def operating_system(name: str) -> OperatingSystem:
    """Returns a connection."""

    return from_string(OperatingSystem, name)


def system(ident: str) -> System:
    """Returns the respective system."""

    try:
        return System[int(ident)]
    except System.DoesNotExist:
        raise ValueError('No such system.') from None


def deployment_type(string: str) -> DeploymentType:
    """Returns a connection."""

    return from_string(DeploymentType, string)