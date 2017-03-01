"""Terminal query utilities"""

from sys import stderr

from homeinfo.lib.strf import Shell

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
            if terminal.isdeployed:
                if self.deployed:
                    yield terminal
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

    class TerminalField():
        """Wrapper to access terminal properties"""

        def __init__(self, name, caption, size=0):
            """Sets the field's name"""
            self.name = name
            self.caption = caption
            self.size = size

        def __str__(self):
            """Returns the formatted caption"""
            return Shell.bold(self.template.format(self.caption))

        @property
        def spacing(self):
            """Returns the required spacing"""
            return max(self.size, len(self.caption))

        @property
        def template(self):
            """Returns the formatting string"""
            return '{{0: >{0}.{0}}}'.format(self.spacing)

        def getattr(self, terminal):
            """Returns the terminal's field's value"""
            return getattr(terminal, self.name)

        def strval(self, terminal):
            """Returns the string representation of the value"""
            value = self.getattr(terminal)

            if value is None:
                return '–'
            elif value is True:
                return '✓'
            elif value is False:
                return '✗'
            else:
                return str(value)

        def format(self, terminal):
            """Formats the respective terminal"""
            return self.template.format(self.strval(terminal))

    class IdField(TerminalField):
        """Field to access the target's ID"""

        def getattr(self, terminal):
            """Returns the terminal's field's value"""
            return super().getattr(terminal).id

    class OSField(IdField):
        """Field to access the target's ID"""

        def strval(self, terminal):
            """Returns the terminal's field's value"""
            return '🐧' if self.getattr(terminal) == 1 else '⧉'

    class AddressField(TerminalField):
        """Field to access the terminal's address"""

        def strval(self, terminal):
            """Returns the terminal's field's value"""
            try:
                return super().strval(terminal)
            except AddressUnconfiguredError:
                return 'N/A'

    class LocationAnnotationField(TerminalField):
        """Field to access the terminal's location annotation"""

        def getattr(self, terminal):
            """Returns the terminal's field's value"""
            location = super().getattr(terminal)

            if location is not None:
                return location.annotation

    FIELDS = {
        'id': TerminalField('id', 'Record ID'),
        'tid': TerminalField('tid', 'Terminal ID'),
        'cid': IdField('customer', 'Customer ID'),
        'vid': TerminalField('vid', 'Virtual ID'),
        'os': OSField('os', 'OS', size=3),
        'ipv4addr': TerminalField('ipv4addr', 'IPv4 Address', size=14),
        'deployed': TerminalField('deployed', 'Deployed', size=21),
        'testing': TerminalField('testing', 'Testing'),
        'tainted': TerminalField('tainted', 'Tainted'),
        'address': AddressField('address', 'Address', size=40),
        'address-annotation': LocationAnnotationField(
            'location', 'Annotation', size=24),
        'annotation': TerminalField('annotation', 'Comment', size=24)}

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
                            if (annotation.lower() in annotation_.lower()):
                                yield terminal
                        else:
                            yield terminal
                else:
                    if annotation is not None:
                        if (annotation.lower() in annotation_.lower()):
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
                print('No {index}th terminal available ({n}).'.format(
                    index=index, n=len(terminals)), file=stderr)
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
                'testing', 'tainted', 'address', 'address-annotation',
                'annotation')

        fields = [self.FIELDS[field] for field in fields]

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

    def format(self, class_):
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
        for os in self:
            yield self.TEMP.format(
                id=str(os.id),
                family=os.family,
                name=os.name,
                version=os.version)


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
