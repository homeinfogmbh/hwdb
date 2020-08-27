"""Type-like functions for argparse."""

from datetime import datetime

from mdb import Customer

from hwdb.hooks import HOOKS
from hwdb.orm import Deployment, System


__all__ = ['customer', 'date', 'deployment', 'hook', 'system']


def customer(value):
    """Returns the respective customer."""

    try:
        return Customer.find(value).get()
    except Customer.DoesNotExist:
        raise ValueError('No such customer.')


def date(string):
    """Parses a date."""

    return datetime.strptime(string, '%Y-%m-%d').date()


def deployment(ident):
    """Returns the respective deployment."""

    return Deployment[ident]


def hook(name):
    """Returns the respective hook."""

    try:
        return HOOKS[name]
    except KeyError:
        raise ValueError(f'No such hook: {name}.')


def system(ident):
    """Returns the respective system."""

    return System[ident]
