"""Terminal query utilities"""

from sys import stderr

from strflib import Shell

from homeinfo.terminals.fields import get_address, get_annotation, \
    TerminalField
from homeinfo.terminals.filter import TerminalFilter
from homeinfo.terminals.orm import Class, Domain, OS, Terminal


__all__ = [
    'DeploymentFilter',
    'TestingFilter',
    'TerminalUtil',
    'ClassUtil',
    'OSUtil',
    'DomainUtil']


class DeploymentFilter():
    """Filters terminals for their deployment state."""

    def __init__(self, terminals, deployed=True, undeployed=True):
        self.terminals = terminals
        self.deployed = deployed
        self.undeployed = undeployed

    def __iter__(self):
        """Yields appropriate terminals."""
        for terminal in self.terminals:
            if terminal.isdeployed:
                if self.deployed:
                    yield terminal
            else:
                if self.undeployed:
                    yield terminal


class TestingFilter():
    """Filters terminals for their testing state."""

    def __init__(self, terminals, testing=True, productive=True):
        self.terminals = terminals
        self.testing = testing
        self.productive = productive

    def __iter__(self):
        """Yields appropriate terminals."""
        for terminal in self.terminals:
            if terminal.testing:
                if self.testing:
                    yield terminal
            else:
                if self.productive:
                    yield terminal


class TerminalUtil():
    """Terminals query utility"""

    FIELDS = {
        'id': TerminalField(lambda terminal: terminal.id, 'ID', size=4),
        'tid': TerminalField(lambda terminal: terminal.tid, 'TID', size=3),
        'cid': TerminalField(
            lambda terminal: terminal.customer.id, 'CID', size=10),
        'vid': TerminalField(lambda terminal: terminal.vid, 'VID', size=3),
        'os': TerminalField(
            lambda terminal: '🐧' if terminal.os.id == 1 else '⧉',
            'OS', size=3),
        'ipv4addr': TerminalField(
            lambda terminal: terminal.ipv4addr, 'IPv4 Address', size=14),
        'deployed': TerminalField(
            lambda terminal: terminal.deployed, 'Deployed', size=21),
        'testing': TerminalField(lambda terminal: terminal.testing, 'Testing'),
        'tainted': TerminalField(lambda terminal: terminal.tainted, 'Tainted'),
        'address': TerminalField(get_address, 'address', 'Address', size=40),
        'annotation': TerminalField(get_annotation, 'Annotation', size=24),
        'comment': TerminalField(
            lambda terminal: terminal.annotation, 'Comment', size=24)}

    def __init__(self, expr, deployed=None, testing=None):
        self.expr = expr
        self.deployed = deployed
        self.testing = testing

    def __iter__(self):
        """Filters the terminals by the respective settings"""
        deployed = self.deployed is None
        testing = self.testing is None

        for terminal in self.terminals:
            if ((deployed or terminal.isdeployed == self.deployed) and
                    (testing or terminal.testing == self.testing)):
                yield terminal

    @property
    def terminals(self):
        """Yields terminals selected by self.expr"""
        if self.expr:
            yield from TerminalFilter(self.expr)
        else:
            yield from Terminal

    @classmethod
    def find(cls, street, house_number=None, annotation=None):
        """Finds terminals in the specified location"""
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

    @classmethod
    def get(cls, street, house_number=None, annotation=None, index=None):
        """Finds a terminal by its location"""

        def _print(terminal):
            print(repr(terminal.location), file=stderr)
            print(str(terminal))

        terminals = list(cls.find(
            street, house_number=house_number, annotation=annotation))

        if not terminals:
            print('No terminal matching query.', file=stderr)
        elif len(terminals) == 1:
            terminal = terminals[0]
            _print(terminal)
            return True
        elif index is not None:
            try:
                terminal = terminals[index]
            except IndexError:
                print('No {}th terminal available ({}).'.format(
                    index, len(terminals)), file=stderr)
                return False
            else:
                _print(terminal)
                return True
        else:
            print(Shell.bold('Ambiguous terminals:'), file=stderr)

            for terminal in terminals:
                _print(terminal)

            return False

    def print(self, header=True, fields=None):
        """Yields formatted terminals for console outoput"""
        if fields is None:
            fields = (
                'id', 'tid', 'cid', 'vid', 'os', 'ipv4addr', 'deployed',
                'testing', 'tainted', 'address', 'annotation', 'comment')

        fields = tuple(self.FIELDS[field] for field in fields)

        if header:
            yield '  '.join(str(field) for field in fields)

        for terminal in self:
            yield '  '.join(field.format(terminal) for field in fields)


class ClassUtil():
    """Terminal classes query utility"""

    TEMP = ('{id: >5.5}  {name: <10.10}  '
            '{full_name: <10.10}  {touch: <5.5}')

    def __iter__(self):
        """Yields available classes"""
        yield from Class

    def print(self):
        """Yields formatted classes for console outoput"""
        for class_ in self:
            yield self.TEMP.format(
                id=str(class_.id),
                name=class_.name,
                full_name=class_.full_name,
                touch=str(class_.touch))


class OSUtil():
    """Terminal OS query utility"""

    TEMP = '{id: >5.5}  {family: <6.6}  {name: <8.8}  {version}'

    def __iter__(self):
        """Yields available OSs"""
        yield from OS

    def print(self):
        """Yields formatted OSs for console outoput"""
        for operating_system in self:
            yield self.TEMP.format(
                id=str(operating_system.id),
                family=operating_system.family,
                name=operating_system.name,
                version=operating_system.version)


class DomainUtil():
    """Terminal domains query utility"""

    TEMP = '{id: >5.5}  {fqdn}'

    def __iter__(self):
        """Yields available domains"""
        yield from Domain

    def print(self):
        """Yields formatted domains for console outoput"""
        for domain in self:
            yield self.TEMP.format(id=str(domain.id), fqdn=domain.fqdn)
