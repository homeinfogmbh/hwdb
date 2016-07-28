"""Terminal query utilities"""

from sys import stderr

from homeinfo.terminals.filter import TerminalFilter
from homeinfo.terminals.orm import Class, Domain, OS, Terminal,\
    AddressUnconfiguredError


__all__ = [
    'DeploymentFilter',
    'TestingFilter',
    'TerminalUtil',
    'ClassUtil',
    'OSUtil',
    'DomainUtil']


class DeploymentFilter():
    """Filters terminals for their deployment state"""

    def __init__(self, terminals, deployed=True, undeployed=True):
        self.terminals = terminals
        self.deployed = deployed
        self.undeployed = undeployed

    def __iter__(self):
        """Yields appropriate terminals"""
        for terminal in self.terminals:
            if terminal.deployed is not None:
                if self.deployed:
                    yield terminals
            else:
                if self.undeployed:
                    yield terminal


class TestingFilter():
    """Filters terminals for their testing state"""

    def __init__(self, terminals, testing=True, productive=True):
        self.terminals = terminals
        self.testing = testing
        self.productive = productive

    def __iter__(self):
        """Yields appropriate terminals"""
        for terminal in self.terminals:
            if terminal.testing:
                if self.testing:
                    yield terminal
            else:
                if self.productive:
                    yield terminal


class TerminalUtil():
    """Terminals query utility"""

    TEMP = ('{id: >5.5} {tid: >5.5} {cid: >10.10} {vid: >5.5} '
            '{ipv4addr: >12.12} {deployed: >21.21} {testing: >6.6}  '
            '{address: <50.50} {annotation}')

    def __init__(self, expr,
                 deployed=None, undeployed=None,
                 testing=None, productive=None):
        self.expr = expr
        self.deployed = deployed
        self.undeployed = undeployed
        self.testing = testing
        self.productive = productive

    def __str__(self):
        """Filters terminals for productiveness and deployment"""
        for terminal in self.filter(terminals):
            try:
                address_str = str(terminal.address)
            except AddressUnconfiguredError:
                address_str = 'N/A'

            print(template.format(
                id=str(terminal.id),
                tid=str(terminal.tid),
                cid=str(terminal.customer.id),
                vid=str(terminal.vid),
                ipv4addr=str(terminal.ipv4addr),
                deployed=str(terminal.deployed),
                testing=str(terminal.testing),
                address=address_str,
                annotation=str(terminal.annotation)))

    def __str__(self):
        """Prints filtered terminals"""
        return '\n'.join(self.format(terminal) for terminal in self)

    def __iter__(self):
        """Filters the terminals by the respective settings"""
        for terminal in self.terminals:
            if self.deployed:
                if self.undeployed:
                    if self.testing:
                        if self.productive:
                            yield terminal
                        else:
                            if terminal.testing:
                                yield terminal
                    else:
                        if self.productive:
                            if not terminal.testing:
                                yield terminal
                else:
                    if terminal.deployed is not None:
                        if self.testing:
                            if self.productive:
                                yield terminal
                            else:
                                if terminal.testing:
                                    yield terminal
                        else:
                            if self.productive:
                                if not terminal.testing:
                                    yield terminal
            else:
                if terminal.deployed is None:
                    if self.undeployed:
                        if self.testing:
                            if self.productive:
                                yield terminal
                            else:
                                if terminal.testing:
                                    yield terminal
                        else:
                            if self.productive:
                                if not terminal.testing:
                                    yield terminal

    @property
    def terminals(self):
        """Yields terminals selected by self.expr"""
        if self.expr:
            return TerminalFilter(self.expr)
        else:
            return Terminal.select().where(True)

    def format(self, terminal):
        """Formats the terminal with the template string"""
        try:
            address_str = str(terminal.address)
        except AddressUnconfiguredError:
            address_str = 'N/A'

        return self.TEMP.format(
            id=str(terminal.id),
            tid=str(terminal.tid),
            cid=str(terminal.customer.id),
            vid=str(terminal.vid),
            ipv4addr=str(terminal.ipv4addr),
            deployed=str(terminal.deployed),
            testing=str(terminal.testing),
            address=address_str,
            annotation=str(terminal.annotation))

    @classmethod
    def find(cls, street, house_number, annotation=None):
        """Finds terminals bathing the specified location"""

        for terminal in Terminal.select().where(
                ~ (Terminal.location >> None)):
            address = terminal.location.address
            house_number_ = address.house_number.replace(' ', '')
            annotation_ = terminal.location.annotation

            if street.lower() in address.street.lower():
                if house_number.lower() == house_number_.lower():
                    if annotation is not None:
                        if (annotation.lower() in annotation_.lower()):
                            yield terminal
                    else:
                        yield terminal

    @classmethod
    def get(cls, street, house_number, annotation=None, index=None):
        """Finds a terminal by its location"""

        def _print(terminal):
            print(repr(terminal.location), file=stderr)
            print(str(terminal))
            return True

        terminals = [t for t in cls.find(
            street, house_number, annotation=None)]

        if not terminals:
            print('No terminal matching query.', file=stderr)
        elif len(terminals) == 1:
            terminal = terminals[0]
            return _print(terminal)
        elif index is not None:
            try:
                terminal = terminals[index]
            except IndexError:
                print('No {index}th terminal available ({n}).'.format(
                    index=index, n=len(terminals)), file=stderr)
                return False
            else:
                return _print(terminal)
        else:
            print('Ambiguous terminals:', terminals, file=stderr)
            return False


class ClassUtil():
    """Terminal classes query utility"""

    TEMP = ('{id: >5.5}  {name: <10.10}  '
            '{full_name: <10.10}  {touch: <5.5}')

    def __init__(self):
        pass

    def __iter__(self):
        """Lists available classes"""
        return Class.select().where(True)

    def __str__(self):
        """Prints available terminal classes"""
        return '\n'.join(self.format(class_) for class_ in self)

    def format(self, class_):
        """Formats the class with the template string"""
        return self.TEMP.format(
            id=str(class_.id),
            name=class_.name,
            full_name=class_.full_name,
            touch=str(class_.touch))


class OSUtil():
    """Terminal OS query utility"""

    TEMP = '{id: >5.5}  {family: <6.6}  {name: <8.8}  {version}'

    def __init__(self):
        pass

    def __iter__(self):
        """Lists available OSs"""
        return OS.select().where(True)

    def __str__(self):
        """Lists available operating systems"""
        return '\n'.join((self.format(os) for os in self))

    def format(self, os):
        """Formats the OS with the template string"""
        return self.TEMP.format(
            id=str(os.id),
            family=os.family,
            name=os.name,
            version=os.version)


class DomainUtil():
    """Terminal domains query utility"""

    TEMP = '{id: >5.5}  {fqdn}'

    def __init__(self):
        pass

    def __iter__(self):
        return Domain.select().where(True)

    def __str__(self):
        """Lists available domains"""
        return '\n'.join((self.format(domain) for domain in self))

    def format(self, domain):
        return self.TEMP.format(
            id=str(domain.id),
            fqdn=domain.fqdn)
