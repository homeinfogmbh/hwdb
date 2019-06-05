"""Systems handling."""

from sys import stderr

from mdb import Address

from terminallib.cli.common import SystemField, FieldFormatter
from terminallib.exceptions import AmbiguityError, TerminalError
from terminallib.orm import Deployment, System


__all__ = [
    'DEFAULT_FIELDS',
    'print_system',
    'find_systems',
    'get_system',
    'list_systems'
]


FIELDS = {
    SystemField.ID: FieldFormatter(lambda sys: sys.id, 'ID', size=5),
    SystemField.DEPLOYMENT: FieldFormatter(
        lambda sys: sys.deployment_id, 'Deployment'),
    SystemField.OPENVPN: FieldFormatter(
        lambda sys: sys.openvpn, 'OpenVPN Address', size=14),
    SystemField.WIREGUARD: FieldFormatter(
        lambda sys: sys.wireguard, 'WireGuard Address', size=14),
    SystemField.MANUFACTURER: FieldFormatter(
        lambda sys: sys.manufacturer, 'Manufacturer', size=24),
    SystemField.CREATED: FieldFormatter(
        lambda sys: sys.created.isoformat(), 'Created', size=24),
    SystemField.CONFIGURED: FieldFormatter(
        lambda sys: sys.configured.isoformat() if sys.configured else None,
        'Created', size=24),
    SystemField.OS: FieldFormatter(
        lambda sys: sys.operating_system.value, 'OS', size=25),
    SystemField.MONITOR: FieldFormatter(lambda sys: sys.monitor, 'Monitor'),
    SystemField.SN: FieldFormatter(
        lambda sys: sys.serial_number, 'Serial Number', size=32),
    SystemField.MODEL: FieldFormatter(
        lambda sys: sys.model, 'Model', size=24,
        leftbound=True),
    SystemField.ONLINE: FieldFormatter(lambda sys: sys.online, 'Online')
}
DEFAULT_FIELDS = (
    SystemField.ID, SystemField.OS, SystemField.MANUFACTURER,
    SystemField.CONFIGURED
)


def print_system(system):
    """Prints the respective system."""

    if system.deployment is not None:
        print(system.deployment, file=stderr)

    print(system.id)


def find_systems(street, house_number=None, annotation=None):
    """Finds systems at the specified address."""

    selection = Address.street ** f'%{street}%'

    if house_number is not None:
        selection &= Address.house_number ** f'%{house_number}%'

    if annotation is not None:
        selection &= Deployment.annotation ** f'%{annotation}%'

    join_condition = Address.id == Deployment.address
    join = System.select().join(Deployment).join(Address, on=join_condition)
    return join.where(selection)


def get_system(street, house_number=None, annotation=None):
    """Finds a system by its address."""

    try:
        system, *superfluous = find_systems(
            street, house_number=house_number, annotation=annotation)
    except ValueError:
        raise TerminalError('No system matching query.')

    if superfluous:
        raise AmbiguityError(system, superfluous)

    return system


def list_systems(systems, header=True, fields=DEFAULT_FIELDS, sep='  '):
    """Yields formatted systems for console outoput."""

    if header:
        yield sep.join(str(field) for field in fields)

    for system in systems:
        yield sep.join(field.format(system) for field in fields)
