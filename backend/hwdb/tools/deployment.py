"""Deployments handling."""

from enum import Enum
from sys import stderr

from mdb import Address

from hwdb.tools.common import FieldFormatter
from hwdb.exceptions import TerminalError, AmbiguityError
from hwdb.orm import Deployment


__all__ = ['DEFAULT_FIELDS', 'find', 'get', 'listdep', 'printdep']


class DeploymentField(Enum):
    """Terminal field names."""

    ADDRESS = 'address'
    ANNOTATION = 'annotation'
    CONNECTION = 'connection'
    CUSTOMER = 'customer'
    ID = 'id'
    LPT_ADDRESS = 'lpt_address'
    SCHEDULED = 'scheduled'
    TESTING = 'testing'
    TYPE = 'type'
    TIMESTAMP = 'timestamp'


FIELDS = {
    DeploymentField.ID: FieldFormatter(lambda dep: dep.id, 'ID', size=5),
    DeploymentField.CUSTOMER: FieldFormatter(
        lambda dep: dep.customer_id, 'Customer', size=12),
    DeploymentField.TYPE: FieldFormatter(
        lambda dep: dep.type.value, 'Type', size=18, leftbound=True),
    DeploymentField.CONNECTION: FieldFormatter(
        lambda dep: dep.connection.value, 'Connection', size=8),
    DeploymentField.ADDRESS: FieldFormatter(
        lambda dep: str(dep.address), 'Address', size=64, leftbound=True),
    DeploymentField.LPT_ADDRESS: FieldFormatter(
        lambda dep: str(dep.lpt_address) if dep.lpt_address else None,
        'Public Transport Address', size=64, leftbound=True),
    DeploymentField.SCHEDULED: FieldFormatter(
        lambda dep: dep.scheduled.isoformat() if dep.scheduled else None,
        'Scheduled', size=12),
    DeploymentField.ANNOTATION: FieldFormatter(
        lambda dep: dep.annotation, 'Annotation', size=40, leftbound=True),
    DeploymentField.TESTING: FieldFormatter(
        lambda dep: dep.testing, 'Testing'),
    DeploymentField.TIMESTAMP: FieldFormatter(
        lambda dep: dep.timestamp.isoformat() if dep.timestamp else None,
        'Timestamp', size=12)
}
DEFAULT_FIELDS = (
    DeploymentField.ID, DeploymentField.CUSTOMER, DeploymentField.TYPE,
    DeploymentField.ADDRESS, DeploymentField.TESTING,
    DeploymentField.ANNOTATION
)


def find(street, house_number=None, annotation=None):
    """Finds systems at the specified address."""

    selection = Address.street ** f'%{street}%'

    if house_number is not None:
        selection &= Address.house_number ** f'%{house_number}%'

    if annotation is not None:
        selection |= Deployment.annotation ** f'%{annotation}%'

    join_condition = Address.id == Deployment.address
    join = Deployment.select().join(Address, on=join_condition)
    return join.where(selection)


def get(street, house_number=None, annotation=None):
    """Finds a deployment by its address."""

    try:
        deployment, *superfluous = find(
            street, house_number=house_number, annotation=annotation)
    except ValueError:
        raise TerminalError('No deployment matching query.')

    if superfluous:
        raise AmbiguityError(deployment, superfluous)

    return deployment


def listdep(deployments, header=True, fields=DEFAULT_FIELDS, sep='  '):
    """Yields formatted deployment for console outoput."""

    formatters = [FIELDS[field] for field in fields]

    if header:
        yield sep.join(str(frmtr) for frmtr in formatters)

    for deployment in deployments:
        yield sep.join(frmtr.format(deployment) for frmtr in formatters)


def printdep(deployment):
    """Prints the respective system."""

    print(deployment, file=stderr)
    print(deployment.id)
