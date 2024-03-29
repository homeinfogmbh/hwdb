"""Deployments handling."""

from enum import Enum
from sys import stderr
from typing import Iterable, Iterator

from peewee import Select

from mdb import Address

from hwdb.tools.common import format_iter, FieldFormatter
from hwdb.exceptions import TerminalError, AmbiguityError
from hwdb.orm import Deployment


__all__ = ["DEFAULT_FIELDS", "DeploymentField", "find", "get", "listdep", "printdep"]


class DeploymentField(Enum):
    """Terminal field names."""

    ADDRESS = "address"
    ANNOTATION = "annotation"
    CONNECTION = "connection"
    CUSTOMER = "customer"
    ID = "id"
    LPT_ADDRESS = "lpt_address"
    SCHEDULED = "scheduled"
    TESTING = "testing"
    TYPE = "type"
    TIMESTAMP = "timestamp"


FIELDS = {
    DeploymentField.ID: FieldFormatter(lambda dep: dep.id, "ID", size=5),
    DeploymentField.CUSTOMER: FieldFormatter(
        lambda dep: dep.customer_id, "Customer", size=12
    ),
    DeploymentField.TYPE: FieldFormatter(
        lambda dep: dep.type.value, "Type", size=18, align_left=True
    ),
    DeploymentField.CONNECTION: FieldFormatter(
        lambda dep: dep.connection.value, "Connection", size=8
    ),
    DeploymentField.ADDRESS: FieldFormatter(
        lambda dep: str(dep.address), "Address", size=64, align_left=True
    ),
    DeploymentField.LPT_ADDRESS: FieldFormatter(
        lambda dep: str(dep.lpt_address) if dep.lpt_address else None,
        "Public Transport Address",
        size=64,
        align_left=True,
    ),
    DeploymentField.SCHEDULED: FieldFormatter(
        lambda dep: dep.scheduled.isoformat() if dep.scheduled else None,
        "Scheduled",
        size=12,
    ),
    DeploymentField.ANNOTATION: FieldFormatter(
        lambda dep: dep.annotation, "Annotation", size=40, align_left=True
    ),
    DeploymentField.TESTING: FieldFormatter(lambda dep: dep.testing, "Testing"),
    DeploymentField.TIMESTAMP: FieldFormatter(
        lambda dep: dep.timestamp.isoformat() if dep.timestamp else None,
        "Timestamp",
        size=12,
    ),
}
DEFAULT_FIELDS = (
    DeploymentField.ID,
    DeploymentField.CUSTOMER,
    DeploymentField.TYPE,
    DeploymentField.ADDRESS,
    DeploymentField.TESTING,
    DeploymentField.ANNOTATION,
)


def find(street: str, house_number: str = None, annotation: str = None) -> Select:
    """Finds systems at the specified address."""

    condition = Address.street ** f"%{street}%"

    if house_number is not None:
        condition &= Address.house_number ** f"%{house_number}%"

    if annotation is not None:
        condition |= Deployment.annotation ** f"%{annotation}%"

    return Deployment.select(cascade=True).where(condition)


def get(street: str, house_number: str = None, annotation: str = None) -> Deployment:
    """Finds a deployment by its address."""

    try:
        deployment, *superfluous = find(
            street, house_number=house_number, annotation=annotation
        )
    except ValueError:
        raise TerminalError("No deployment matching query.") from None

    if superfluous:
        raise AmbiguityError(deployment, superfluous)

    return deployment


def listdep(
    deployments: Iterable[Deployment],
    fields: Iterable[DeploymentField] = DEFAULT_FIELDS,
) -> Iterator[str]:
    """Yields formatted deployment for console output."""

    return format_iter(deployments, FIELDS, fields)


def printdep(deployment: Deployment):
    """Prints the respective system."""

    print(deployment, file=stderr)
    print(deployment.id)
