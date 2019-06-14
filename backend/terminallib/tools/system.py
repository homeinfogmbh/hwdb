"""Systems handling."""

from enum import Enum
from sys import stderr

from mdb import Address

from terminallib.tools.common import FieldFormatter
from terminallib.exceptions import AmbiguityError, TerminalError
from terminallib.orm import Deployment, System


__all__ = ['DEFAULT_FIELDS', 'find', 'get', 'listsys', 'printsys']


class SystemField(Enum):
    """Terminal field names."""

    CONFIGURED = 'configured'
    CREATED = 'created'
    DEPLOYMENT = 'deployment'
    ID = 'id'
    MANUFACTURER = 'manufacturer'
    MODEL = 'model'
    MONITOR = 'monitor'
    ONLINE = 'online'
    OPENVPN = 'openvpn'
    OS = 'os'
    SN = 'sn'
    WIREGUARD = 'wireguard'


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
    SystemField.ID, SystemField.DEPLOYMENT, SystemField.OPENVPN,
    SystemField.MANUFACTURER, SystemField.CONFIGURED, SystemField.OS
)


def find(street, house_number=None, annotation=None):
    """Finds systems at the specified address."""

    selection = Address.street ** f'%{street}%'

    if house_number is not None:
        selection &= Address.house_number ** f'%{house_number}%'

    if annotation is not None:
        selection &= Deployment.annotation ** f'%{annotation}%'

    join_condition = Address.id == Deployment.address
    join = System.select().join(Deployment).join(Address, on=join_condition)
    return join.where(selection)


def get(street, house_number=None, annotation=None):
    """Finds a system by its address."""

    try:
        system, *superfluous = find(
            street, house_number=house_number, annotation=annotation)
    except ValueError:
        raise TerminalError('No system matching query.')

    if superfluous:
        raise AmbiguityError(system, superfluous)

    return system


def listsys(systems, header=True, fields=DEFAULT_FIELDS, sep='  '):
    """Yields formatted systems for console outoput."""

    formatters = [FIELDS[field] for field in fields]

    if header:
        yield sep.join(str(frmtr) for frmtr in formatters)

    for system in systems:
        yield sep.join(frmtr.format(system) for frmtr in formatters)


def printsys(system):
    """Prints the respective system."""

    if system.deployment is not None:
        print(system.deployment, file=stderr)

    print(system.id)
