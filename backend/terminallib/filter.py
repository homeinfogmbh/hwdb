"""Terminal filters."""

from terminallib.config import LOGGER
from terminallib.orm import Deployment, System


__all__ = [
    'filter_online',
    'filter_offline',
    'get_deployments',
    'get_systems'
]


def _parse_ids(idents):
    """Yields system IDs."""

    for ident in idents:
        try:
            yield int(ident)
        except ValueError:
            LOGGER.warning('Ignoring invalid system ID: %s', ident)


def _parse(ids, model):
    """Returns a peewee.Expression for the respective systems selection."""

    if not ids:
        return True

    ids = set(_parse_ids(ids))
    return model.id << ids


def filter_online(systems):
    """Yields online systems."""

    for system in systems:
        if system.is_online:
            yield system


def filter_offline(systems):
    """Yields offline systems."""

    for system in systems:
        if not system.is_online:
            yield system


def get_deployments(ids, customer=None, testing=None, types=None,
                    connections=None):
    """Yields deployments."""

    select = _parse(ids, Deployment)

    if customer is not None:
        select &= Deployment.customer == customer

    if testing is not None:
        select &= Deployment.testing == testing

    if types:
        select &= Deployment.types << types

    if connections:
        select &= Deployment.connection << connections

    return Deployment.select().where(select)


def get_systems(ids, deployments=None, deployed=None, oss=None, online=None):
    """Yields systems for the respective expressions and filters."""

    select = _parse(ids, System)

    if deployments is not None:
        select &= System.deployment << deployments

    if deployed is not None:
        if deployed:
            select &= ~(System.deployment >> None)
        else:
            select &= System.deployment >> None

    if oss:
        select &= System.operating_system << oss

    systems = System.select().where(select)

    if online is not None:
        if online:
            return filter_online(systems)

        return filter_offline(systems)

    return systems
