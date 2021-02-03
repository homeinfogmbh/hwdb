"""Terminal filters."""

from typing import Generator, Iterable

from peewee import JOIN, Expression, ModelBase, ModelSelect

from mdb import Customer

from hwdb.config import LOGGER
from hwdb.enumerations import Connection, DeploymentType, OperatingSystem
from hwdb.orm import Deployment, System


__all__ = [
    'filter_online',
    'filter_offline',
    'get_deployments',
    'get_systems'
]


def _parse_ids(idents: Iterable[str]) -> Generator[int, None, None]:
    """Yields system IDs."""

    for ident in idents:
        try:
            yield int(ident)
        except ValueError:
            LOGGER.warning('Ignoring invalid system ID: %s', ident)


def _get_expression(ids: Iterable[str], model: ModelBase) -> Expression:
    """Returns a peewee.Expression for the respective systems selection."""

    if not ids:
        return True

    ids = set(_parse_ids(ids))
    return model.id << ids


def filter_online(systems: Iterable[System]) -> Generator[System, None, None]:
    """Yields online systems."""

    for system in systems:
        if system.online:
            yield system


def filter_offline(systems: Iterable[System]) -> Generator[System, None, None]:
    """Yields offline systems."""

    for system in systems:
        if not system.online:
            yield system


def get_deployments(ids: Iterable[int] = None,
                    customers: Iterable[Customer] = None,
                    testing: bool = None,
                    types: Iterable[DeploymentType] = None,
                    connections: Iterable[Connection] = None,
                    systems: Iterable[System] = None
                    ) -> ModelSelect:
    """Yields deployments."""

    select = Deployment.select()
    condition = True

    if ids:
        condition &= Deployment.id << ids

    if customers:
        condition &= Deployment.customer << customers

    if testing is not None:
        condition &= Deployment.testing == bool(testing)

    if types:
        condition &= Deployment.type << types

    if connections:
        condition &= Deployment.connection << connections

    if systems:
        dataset = System.alias()
        select = select.join(
            System, JOIN.LEFT_OUTER, on=Deployment.id == System.deployment
        ).join_from(
            Deployment, dataset, JOIN.LEFT_OUTER,
            on=Deployment.id == dataset.dataset
        )
        condition &= (System.id << systems) | (dataset.id << systems)

    return select.where(condition)


def get_systems(ids: Iterable[int],
                customers: Iterable[Customer] = None,
                deployments: Iterable[Deployment] = None,
                datasets: Iterable[Deployment] = None,
                configured: bool = None,
                deployed: bool = None,
                fitted: bool = None,
                operating_systems: Iterable[OperatingSystem] = None,
                operators: Iterable[Customer] = None,
                online: bool = None
                ) -> Generator[System, None, None]:
    """Yields systems for the respective expressions and filters."""

    condition = True

    if ids:
        condition &= System.id << ids

    if customers:
        condition &= Deployment.customer << customers

    if deployments:
        condition &= System.deployment << deployments

    if datasets:
        condition &= System.dataset << datasets

    if configured is not None:
        if configured:
            condition &= ~(System.configured >> None)
        else:
            condition &= System.configured >> None

    if deployed is not None:
        if deployed:
            condition &= ~(System.deployment >> None)
        else:
            condition &= System.deployment >> None

    if fitted is not None:
        condition &= System.fitted == fitted

    if operating_systems:
        condition &= System.operating_system << operating_systems

    if operators:
        condition &= System.operator << operators

    select = System.select(cascade=True).where(condition)

    if online is None:
        return select

    if online:
        return filter_online(select)

    return filter_offline(select)
