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

    ident = int(ident)

    try:
        return Deployment[ident]
    except Deployment.DoesNotExist:
        return ValueError('No such deployment.')


def hook(name):
    """Returns the respective hook."""

    try:
        return HOOKS[name]
    except KeyError:
        raise ValueError('No such hook.')


def system(ident):
    """Returns the respective system."""

    ident = int(ident)

    try:
        return System[ident]
    except System.DoesNotExist:
        raise ValueError('No such system.')
