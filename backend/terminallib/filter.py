"""Terminal filters."""

from terminallib.config import LOGGER
from terminallib.ctrl import is_online
from terminallib.orm import Location, System


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

    ids = frozenset(_parse_ids(ids))
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


def get_systems(ids, customer=None, deployed=None,  # pylint: disable=R0913
                testing=None, oss=None, online=None, offline=None):
    """Yields systems for the respective expressions and filters."""

    select = parse(ids)

    if customer is not None:
        select &= Location.customer == customer

    if deployed is not None:
        if deployed in {True, False}:
            if deployed:
                select &= ~(Location.deployed >> None)
            else:
                select &= Location.deployed >> None
        else:
            select &= Location.deployed == deployed

    if testing is not None:
        select &= System.testing == testing

    if oss:
        select &= System.operating_system << oss

    systems = System.select().join(Location).where(select)

    if online and not offline:
        return filter_online(systems)

    if offline and not online:
        return filter_offline(systems)

    return systems
