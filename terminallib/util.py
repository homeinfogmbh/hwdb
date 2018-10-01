"""Terminal query utilities."""

from sys import stderr

from mdb import Address
from syslib import B64LZMA

from terminallib.fields import get_address, TerminalField
from terminallib.orm import Class, Domain, OS, Terminal


__all__ = [
    'ARNIE',
    'DEFAULT_FIELDS',
    'TerminalError',
    'AmbiguousTerminals',
    'print_terminal',
    'find_terminals',
    'get_terminal',
    'list_terminals',
    'list_classes',
    'list_oss',
    'list_domains']


FIELDS = {
    'id': TerminalField(lambda terminal: terminal.id, 'ID', size=4),
    'tid': TerminalField(lambda terminal: terminal.tid, 'TID', size=3),
    'cid': TerminalField(
        lambda terminal: terminal.customer.id, 'CID', size=10),
    'vid': TerminalField(lambda terminal: terminal.vid, 'VID', size=3),
    'class': TerminalField(
        lambda terminal: terminal.class_.name, 'Class', size=9,
        leftbound=True),
    'os': TerminalField(
        lambda terminal: repr(terminal.os), 'OS', size=19, leftbound=True),
    'ipv4addr': TerminalField(
        lambda terminal: terminal.ipv4addr, 'IPv4 Address', size=14),
    'scheduled': TerminalField(
        lambda terminal: terminal.scheduled, 'Scheduled', size=21),
    'deployed': TerminalField(
        lambda terminal: terminal.deployed, 'Deployed', size=21),
    'testing': TerminalField(lambda terminal: terminal.testing, 'Testing'),
    'tainted': TerminalField(lambda terminal: terminal.tainted, 'Tainted'),
    'address': TerminalField(
        get_address, 'Address', size=48, leftbound=True),
    'annotation': TerminalField(
        lambda terminal: terminal.annotation, 'Annotation', size=24,
        leftbound=True),
    'online': TerminalField(lambda terminal: terminal.online, 'Online')}

ARNIE = B64LZMA(
    '/Td6WFoAAATm1rRGAgAhARYAAAB0L+Wj4AIEAK9dABBuADwUaYt0gRsna7sph26BXekoRMls4'
    'PqOjQ0VHvqxoXly1uRgtvfLn9pvnm1DrCgcJiPp8HhWiGzH7ssJqMiSKm0l67Why5BVT8apzO'
    'CVXevyza2ZXmT21h0aDCiPYjN4ltUrrguxqC4Lwn0XwvoWRxpXGb0wAyV//ppegMFpCqvR3y/'
    'l6gnu1zzfCVOISaOCOjHXq2NiJ3ZUMv76UcKZjfFEnW11r/P35yFKGo4AAJxj7ZVSD0rZAAHL'
    'AYUEAADP/ZRYscRn+wIAAAAABFla')

CLASS_TEMP = '{id: >5.5}  {name: <10.10}  {full_name: <10.10}  {touch: <5.5}'
OS_TEMP = '{id: >5.5}  {family: <6.6}  {name: <8.8}  {version}'
DOMAIN_TEMP = '{id: >5.5}  {fqdn}'
DEFAULT_FIELDS = (
    'id', 'tid', 'cid', 'vid', 'os', 'ipv4addr', 'deployed', 'testing',
    'tainted', 'address', 'annotation')


class TerminalError(Exception):
    """Indicates an error with the respective terminal."""

    pass


class AmbiguousTerminals(TerminalError):
    """Indicates that a query for a single
    terminal yielded ambiguous terminals.
    """

    def __init__(self, message, terminals):
        """Sets message and terminals."""
        super().__init__(message)
        self.terminals = terminals


def _match_annotation(annotation, target):
    """Matches the annotation against the target value."""

    return annotation is None or annotation.lower() in target.lower()


def print_terminal(terminal):
    """Prints the respective terminal."""

    print(repr(terminal.address), '({})'.format(terminal.annotation),
          file=stderr)
    print(str(terminal))


def find_terminals(street, house_number=None, annotation=None):
    """Finds terminals in the specified location."""

    selection = Address.street ** '%{}%'.format(street)

    if house_number is not None:
        selection &= Address.house_number ** '%{}%'.format(house_number)

    if annotation is not None:
        selection &= Terminal.annotation ** '%{}%'.format(annotation)

    return Terminal.select().join(
        Address, on=(Terminal.address == Address.id)).where(selection)


def get_terminal(street, house_number=None, annotation=None, index=0):
    """Finds a terminal by its location."""

    terminals = tuple(find_terminals(
        street, house_number=house_number, annotation=annotation))

    if not terminals:
        raise TerminalError('No terminal matching query.')

    index = index or 0

    try:
        return terminals[index]
    except IndexError:
        raise TerminalError('No terminal #{} available ({}).'.format(
            index, len(terminals)))

    raise AmbiguousTerminals('Ambiguous terminals:', terminals)


def list_terminals(terminals, header=True, fields=DEFAULT_FIELDS, sep='  '):
    """Yields formatted terminals for console outoput."""

    fields = tuple(FIELDS[field] for field in fields)

    if header:
        yield sep.join(str(field) for field in fields)

    for terminal in terminals:
        yield sep.join(field.format(terminal) for field in fields)


def list_classes():
    """Yields formatted terminal classes."""

    for class_ in Class:
        yield CLASS_TEMP.format(
            id=str(class_.id), name=class_.name, full_name=class_.full_name,
            touch=str(class_.touch))


def list_oss():
    """Yields formatted operating system entries."""

    for operating_system in OS:
        yield OS_TEMP.format(
            id=str(operating_system.id), family=operating_system.family,
            name=operating_system.name, version=operating_system.version)


def list_domains():
    """Lists formatted domains."""

    for domain in Domain:
        yield DOMAIN_TEMP.format(id=str(domain.id), fqdn=domain.fqdn)
