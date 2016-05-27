"""Terminal query utilities"""


from homeinfo.lib.strf import Terminal as TerminalColor

from homeinfo.terminals.filter import TerminalFilter
from homeinfo.terminals.orm import Class, Domain, OS, Terminal,\
    AddressUnconfiguredError


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

    def __init__(self, *args,
                 deployed=None, undeployed=None,
                 testing=None, productive=None):
        self.args = args
        self.deployed = deployed
        self.undeployed = undeployed
        self.testing = testing
        self.productive = productive

    def __iter__(self):
        """Filters terminals for productiveness and deployment"""
        for arg in self.args:
            # TODO: Implement
            if False:
                yield None

    def __str__(self):
        """Prints filtered terminals"""
        return '\n'.join((self.format(terminal) for terminal in self))

    @property
    def terminals(self):
        """Yields terminals selected by self.expr"""
        if self.expr:
            return TerminalFilter(expr)
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
