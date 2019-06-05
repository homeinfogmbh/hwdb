"""Deployments handling."""

from sys import stderr

from mdb import Address

from terminallib.cli.common import DeploymentField, FieldFormatter
from terminallib.exceptions import TerminalError, AmbiguityError
from terminallib.orm import Deployment


__all__ = [
    'DEFAULT_FIELDS',
    'print_deployment',
    'find_deployments',
    'get_deployment',
    'list_deployments'
]


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
    DeploymentField.WEATHER: FieldFormatter(
        lambda dep: dep.weather, 'Weather', size=12),
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


def print_deployment(deployment):
    """Prints the respective system."""

    print(deployment, file=stderr)
    print(deployment.id)


def find_deployments(street, house_number=None, annotation=None):
    """Finds systems at the specified address."""

    selection = Address.street ** f'%{street}%'

    if house_number is not None:
        selection &= Address.house_number ** f'%{house_number}%'

    if annotation is not None:
        selection &= Deployment.annotation ** f'%{annotation}%'

    return Deployment.select().join(
        Address, on=Address.id == Deployment.address).where(selection)


def get_deployment(street, house_number=None, annotation=None):
    """Finds a deployment by its address."""

    try:
        deployment, *superfluous = find_deployments(
            street, house_number=house_number, annotation=annotation)
    except ValueError:
        raise TerminalError('No deployment matching query.')

    if superfluous:
        raise AmbiguityError(deployment, superfluous)

    return deployment


def list_deployments(deployments, header=True, fields=DEFAULT_FIELDS, sep='  '):
    """Yields formatted deployment for console outoput."""

    formatters = [FIELDS[field] for field in fields]

    if header:
        yield sep.join(str(frmtr) for frmtr in formatters)

    for deployment in deployments:
        yield sep.join(frmtr.format(deployment) for frmtr in formatters)
