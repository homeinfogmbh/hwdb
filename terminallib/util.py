"""Terminal query utilities."""

from sys import stderr

from syslib import B64LZMA

from terminallib.fields import get_address, get_annotation, TerminalField
from terminallib.filter import parse
from terminallib.orm import Class, Domain, OS, Terminal


__all__ = [
    'ARNIE',
    'TerminalError',
    'AmbiguousTerminals',
    'print_terminal',
    'filter_terminals',
    'find_terminals',
    'get_terminal',
    'list_terminals',
    'deployment_filter',
    'testing_filter',
    'list_classes',
    'list_oss',
    'list_domains']


FIELDS = {
    'id': TerminalField(lambda terminal: terminal.id, 'ID', size=4),
    'tid': TerminalField(lambda terminal: terminal.tid, 'TID', size=3),
    'cid': TerminalField(
        lambda terminal: terminal.customer.cid, 'CID', size=10),
    'vid': TerminalField(lambda terminal: terminal.vid, 'VID', size=3),
    'class': TerminalField(
        lambda terminal: terminal.class_.name, 'Class', size=9,
        leftbound=True),
    'os': TerminalField(
        lambda terminal: repr(terminal.os), 'OS', size=19, leftbound=True),
    'ipv4addr': TerminalField(
        lambda terminal: terminal.ipv4addr, 'IPv4 Address', size=14),
    'deployed': TerminalField(
        lambda terminal: terminal.deployed, 'Deployed', size=21),
    'testing': TerminalField(lambda terminal: terminal.testing, 'Testing'),
    'tainted': TerminalField(lambda terminal: terminal.tainted, 'Tainted'),
    'address': TerminalField(
        get_address, 'Address', size=48, leftbound=True),
    'annotation': TerminalField(
        get_annotation, 'Annotation', size=32, leftbound=True),
    'comment': TerminalField(
        lambda terminal: terminal.annotation, 'Comment',
        size=24, leftbound=True),
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


def print_terminal(terminal):
    """Prints the respective terminal."""

    print(repr(terminal.location), file=stderr)
    print(str(terminal))


def filter_terminals(
        expr=None, *, deployed=None, testing=None, class_=None, os=None,
        online=None):
    """Lists terminals."""

    terminals = parse(expr) if expr else Terminal

    for terminal in terminals:
        if all((deployed is None or terminal.isdeployed == deployed,
                testing is None or terminal.testing == testing,
                class_ is None or terminal.class_ == class_,
                os is None or terminal.os == os)):
            # Perform online check after all other
            # checks, since it is extremely slow.
            if not online or terminal.online:
                yield terminal


def find_terminals(street, house_number=None, annotation=None):
    """Finds terminals in the specified location."""

    for terminal in Terminal.select().where(~ (Terminal.location >> None)):
        address = terminal.location.address
        house_number_ = address.house_number.replace(' ', '')
        annotation_ = terminal.location.annotation

        if street.lower() in address.street.lower():
            if house_number is not None:
                if house_number.lower() == house_number_.lower():
                    if annotation is not None:
                        if annotation.lower() in annotation_.lower():
                            yield terminal
                    else:
                        yield terminal
            else:
                if annotation is not None:
                    if annotation.lower() in annotation_.lower():
                        yield terminal
                else:
                    yield terminal


def get_terminal(street, house_number=None, annotation=None, index=None):
    """Finds a terminal by its location."""

    terminals = tuple(find_terminals(
        street, house_number=house_number, annotation=annotation))

    if not terminals:
        raise TerminalError('No terminal matching query.')
    elif len(terminals) == 1:
        return terminals[0]
    elif index is not None:
        try:
            return terminals[index]
        except IndexError:
            raise TerminalError('No {}th terminal available ({}).'.format(
                index, len(terminals)))

    raise AmbiguousTerminals('Ambiguous terminals:', terminals)


def list_terminals(terminals, header=True, fields=None, sep='  '):
    """Yields formatted terminals for console outoput."""

    if fields is None:
        fields = (
            'id', 'tid', 'cid', 'vid', 'os', 'ipv4addr', 'deployed',
            'testing', 'tainted', 'address', 'annotation')

    fields = tuple(FIELDS[field] for field in fields)

    if header:
        yield sep.join(str(field) for field in fields)

    for terminal in terminals:
        yield sep.join(field(terminal) for field in fields)


def deployment_filter(terminals, deployed=True, undeployed=True):
    """Yields deployed terminals."""

    for terminal in terminals:
        if terminal.isdeployed:
            if deployed:
                yield terminal
        else:
            if undeployed:
                yield terminal


def testing_filter(terminals, testing=True, productive=True):
    """Yields the respective terminals."""

    for terminal in terminals:
        if terminal.testing:
            if testing:
                yield terminal
        else:
            if productive:
                yield terminal


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
