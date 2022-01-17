"""Systems handling."""

from enum import Enum
from sys import stderr
from typing import Iterable, Iterator

from peewee import Select

from mdb import Address

from hwdb.tools.common import format_iter, FieldFormatter
from hwdb.exceptions import AmbiguityError, TerminalError
from hwdb.orm import Deployment, System


__all__ = [
    'DEFAULT_FIELDS',
    'SystemField',
    'find',
    'get',
    'listsys',
    'printsys'
]


class SystemField(Enum):
    """Terminal field names."""

    CONFIGURED = 'configured'
    CREATED = 'created'
    DATASET = 'dataset'
    DEPLOYMENT = 'deployment'
    FITTED = 'fitted'
    GROUP = 'group'
    ID = 'id'
    IP = 'ip'
    MODEL = 'model'
    MONITOR = 'monitor'
    ONLINE = 'online'
    OPENVPN = 'openvpn'
    OS = 'os'
    SN = 'sn'
    WG_ADDR = 'wg'
    WG_PUBKEY = 'pubkey'


FIELDS = {
    SystemField.CONFIGURED: FieldFormatter(
        lambda sys: sys.configured.isoformat() if sys.configured else None,
        'Configured', size=24),
    SystemField.CREATED: FieldFormatter(
        lambda sys: sys.created.isoformat(), 'Created', size=24),
    SystemField.DATASET: FieldFormatter(
        lambda sys: sys.dataset_id, 'Dataset'),
    SystemField.DEPLOYMENT: FieldFormatter(
        lambda sys: sys.deployment_id, 'Deployment'),
    SystemField.FITTED: FieldFormatter(lambda sys: sys.fitted, 'Fitted'),
    SystemField.GROUP: FieldFormatter(
        lambda sys: sys.group.id, 'Group', size=12),
    SystemField.ID: FieldFormatter(lambda sys: sys.id, 'ID', size=5),
    SystemField.IP: FieldFormatter(
        lambda sys: sys.ip_address, 'IP address', size=25),
    SystemField.MODEL: FieldFormatter(
        lambda sys: sys.model, 'Model', size=24, align_left=True),
    SystemField.MONITOR: FieldFormatter(lambda sys: sys.monitor, 'Monitor'),
    SystemField.ONLINE: FieldFormatter(lambda sys: sys.online, 'Online'),
    SystemField.OPENVPN: FieldFormatter(
        lambda sys: sys.openvpn, 'OpenVPN Address', size=14),
    SystemField.OS: FieldFormatter(
        lambda sys: sys.operating_system.value, 'OS', size=25),
    SystemField.SN: FieldFormatter(
        lambda sys: sys.serial_number, 'Serial Number', size=32),
    SystemField.WG_ADDR: FieldFormatter(
        lambda sys: sys.ipv6address, 'WireGuard IPv6 address', size=23),
    SystemField.WG_PUBKEY: FieldFormatter(
        lambda sys: sys.pubkey, 'WireGuard pubkey', size=44)
}
DEFAULT_FIELDS = (
    SystemField.ID, SystemField.DEPLOYMENT, SystemField.DATASET,
    SystemField.IP, SystemField.GROUP, SystemField.CONFIGURED,
    SystemField.FITTED, SystemField.OS
)


def find(street: str, house_number: str = None,
         annotation: str = None) -> Select:
    """Finds systems at the specified address."""

    condition = Address.street ** f'%{street}%'

    if house_number is not None:
        condition &= Address.house_number ** f'%{house_number}%'

    if annotation is not None:
        condition |= Deployment.annotation ** f'%{annotation}%'

    return System.select(cascade=True).where(condition)


def get(street: str, house_number: str = None,
        annotation: str = None) -> System:
    """Finds a system by its address."""

    try:
        system, *superfluous = find(
            street, house_number=house_number, annotation=annotation)
    except ValueError:
        raise TerminalError('No system matching query.') from None

    if superfluous:
        raise AmbiguityError(system, superfluous)

    return system


def listsys(systems: Iterable[System],
            fields: Iterable[SystemField] = DEFAULT_FIELDS) -> Iterator[str]:
    """Yields formatted systems for console output."""

    return format_iter(systems, FIELDS, fields)


def printsys(system: System):
    """Prints the respective system."""

    if system.deployment is not None:
        print(system.deployment, file=stderr)

    print(system.id)
