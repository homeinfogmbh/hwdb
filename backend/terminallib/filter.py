"""Terminal filters."""

from terminallib.config import LOGGER
from terminallib.ctrl import is_online
from terminallib.orm import Deployment, System


__all__ = ['parse', 'filter_online', 'filter_offline', 'get_systems']


def _parse_ids(idents):
    """Yields system IDs."""

    for ident in idents:
        try:
            yield int(ident)
        except ValueError:
            LOGGER.warning('Ignoring invalid system ID: %s', ident)


def parse(ids):
    """Returns a peewee.Expression for the respective systems selection."""

    if not ids:
        return True

    ids = set(_parse_ids(ids))
    return System.id << ids


def filter_online(systems):
    """Yields online systems."""

    for system in systems:
        if is_online(system):
            yield system


def filter_offline(systems):
    """Yields offline systems."""

    for system in systems:
        if not is_online(system):
            yield system


def get_systems(ids, customer=None, deployed=None, testing=None, types=None,
                oss=None, online=None):
    """Yields systems for the respective expressions and filters."""

    select = parse(ids)
    join_deployment = False

    if customer is not None:
        select &= Deployment.customer == customer
        join_deployment = True

    if deployed is not None:
        if deployed:
            select &= ~(System.deployment >> None)
        else:
            select &= System.deployment >> None

    if testing is not None:
        select &= Deployment.testing == testing
        join_deployment = True

    if types:
        select &= Deployment.types << types
        join_deployment = True

    if oss:
        select &= System.operating_system << oss

    systems = System.select()

    if join_deployment:
        systems = systems.join(Deployment)

    systems = systems.where(select)

    if online is not None:
        if online:
            return filter_online(systems)

        return filter_offline(systems)

    return systems
