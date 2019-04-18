"""Command line interface utilities."""

from sys import stderr

from mdb import Address
from syslib import B64LZMA

from terminallib.config import LOGGER
from terminallib.fields import TerminalField
from terminallib.orm import Deployment, System
from terminallib.enumerations import OperatingSystem, Type
from terminallib.exceptions import TerminalError, AmbiguousSystems


__all__ = [
    'ARNIE',
    'DEFAULT_FIELDS',
    'print_system',
    'find_systems',
    'get_system',
    'list_oss',
    'list_systems',
    'list_types']


FIELDS = {
    'id': TerminalField(lambda system: system.id, 'ID', size=5),
    'os': TerminalField(
        lambda system: system.operating_system.value, 'OS', size=19),
    'openvpn': TerminalField(
        lambda system: system.openvpn, 'OpenVPN Address', size=14),
    'wireguard': TerminalField(
        lambda system: system.wireguard, 'WireGuard Address', size=14),
    'testing': TerminalField(lambda system: system.testing, 'Testing'),
    'monitor': TerminalField(lambda system: system.monitor, 'Monitor'),
    'sn': TerminalField(
        lambda system: system.serial_number, 'Serial Number', size=32),
    'deployment': TerminalField(
        lambda system: system.deployment, 'Deployment', size=48,),
    'connection': TerminalField(
        lambda system: system.connection.value, 'Connection', size=8),
    'model': TerminalField(
        lambda system: system.model, 'Model', size=24,
        leftbound=True),
    'online': TerminalField(lambda system: system.online, 'Online')}

ARNIE = B64LZMA(
    '/Td6WFoAAATm1rRGAgAhARYAAAB0L+Wj4AIEAK9dABBuADwUaYt0gRsna7sph26BXekoRMls4'
    'PqOjQ0VHvqxoXly1uRgtvfLn9pvnm1DrCgcJiPp8HhWiGzH7ssJqMiSKm0l67Why5BVT8apzO'
    'CVXevyza2ZXmT21h0aDCiPYjN4ltUrrguxqC4Lwn0XwvoWRxpXGb0wAyV//ppegMFpCqvR3y/'
    'l6gnu1zzfCVOISaOCOjHXq2NiJ3ZUMv76UcKZjfFEnW11r/P35yFKGo4AAJxj7ZVSD0rZAAHL'
    'AYUEAADP/ZRYscRn+wIAAAAABFla')

CLASS_TEMP = '{id: >5.5}  {name: <10.10}  {full_name: <10.10}  {touch: <5.5}'
OS_TEMP = '{id: >5.5}  {family: <6.6}  {name: <8.8}  {version}'
DOMAIN_TEMP = '{id: >5.5}  {fqdn}'
DEFAULT_FIELDS = ('id', 'os', 'openvpn', 'wireguard', 'testing', 'deployment')


def _get_fields(fields):
    """Yields valid fields from a string of field names."""

    for field in fields:
        try:
            yield FIELDS[field]
        except KeyError:
            LOGGER.warning('Ignoring invalid field: %s', field)


def print_system(system):
    """Prints the respective system."""

    deployment = system.deployment

    if deployment is not None:
        print(str(deployment.address), '({})'.format(deployment.annotation),
              file=stderr)

    print(system.id)


def find_systems(street, house_number=None, annotation=None):
    """Finds systems at the specified address."""

    selection = Address.street ** '%{}%'.format(street)

    if house_number is not None:
        selection &= Address.house_number ** '%{}%'.format(house_number)

    if annotation is not None:
        selection &= Deployment.annotation ** '%{}%'.format(annotation)

    join_condition = Address.id == Deployment.address
    join = System.select().join(Deployment).join(Address, on=join_condition)
    return join.where(selection)


def get_system(street, house_number=None, annotation=None):
    """Finds a system by its address."""

    try:
        system, superfluous = find_systems(
            street, house_number=house_number, annotation=annotation)
    except ValueError:
        raise TerminalError('No system matching query.')

    if superfluous:
        raise AmbiguousSystems(superfluous)

    return system


def list_oss():
    """Yields formatted operating system entries."""

    for operating_system in OperatingSystem:
        yield str(operating_system)


def list_systems(systems, header=True, fields=DEFAULT_FIELDS, sep='  '):
    """Yields formatted systems for console outoput."""

    fields = tuple(_get_fields(fields))

    if header:
        yield sep.join(str(field) for field in fields)

    for system in systems:
        yield sep.join(field.format(system) for field in fields)


def list_types():
    """Yields formatted terminal classes."""

    for typ in Type:
        yield str(typ)
