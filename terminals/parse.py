"""Terminal selection expression parsing."""

from peewee import DoesNotExist

from .orm import Terminal

__all__ = [
    'InvalidExpression',
    'InvalidBlock',
    'InvalidIdentifier',
    'InvalidCustomerID',
    'NoSuchTerminals',
    'Identifier',
    'IdentifierList',
    'TerminalSelection']


class InvalidExpression(ValueError):
    """Indicates that an invalid expression was specified."""

    def __init__(self, expression):
        """Sets the invalid expression."""
        super().__init__(expression)
        self.expression = expression


class InvalidBlock(ValueError):
    """Indicates that an invalid identifier block was specified."""

    def __init__(self, block):
        """Sets the invalid block."""
        super().__init__(block)
        self.block = block


class InvalidIdentifier(ValueError):
    """Indicates that an invalid identifier (VID/TID)
    has been specified.
    """

    def __init__(self, identifier):
        """Sets the invalid identifier."""
        super().__init__(identifier)
        self.identifier = identifier


class InvalidCustomerID(ValueError):
    """Indicates that an invalid customer ID has been specified."""

    def __init__(self, cid):
        """Sets the invalid cid."""
        super().__init__(cid)
        self.cid = cid


class NoSuchTerminals(ValueError):
    """indicates that the respective terminals were missing."""

    def __init__(self, cid, identifiers):
        """Sets the customer ID and identifiers."""
        super().__init__((cid, identifiers))
        self.cid = cid
        self.identifiers = identifiers


def split_cid(expression, sep='.'):
    """Splits IDs and customer ID."""

    try:
        blocks, cid = expression.split(sep)
    except ValueError:
        if sep in expression:
            raise InvalidExpression(expression) from None
        else:
            return (None, expression)
    else:
        return (blocks, cid)


def split_blocks(blocks, sep=','):
    """Splits TID / VID ID blocks."""

    for block in blocks.split(sep):
        yield block.strip()


def parse_block(block, sep='-'):
    """Yields the block's values."""

    try:
        start, end = block.split(sep)
    except ValueError:
        if sep in block:
            raise InvalidBlock(block) from None
        else:
            return Identifier.from_string(block)
    else:
        start = Identifier.from_string(start)
        end = Identifier.from_string(end)

        if int(start) < int(end):
            return (start, end)
        else:
            raise ValueError(
                'Invalid range {}→{}. Start must be smaller than end.'.format(
                    start, end))


class Identifier:
    """Represents VIDs and TIDs."""

    def __init__(self, value, virtual):
        """Sets value and virtual flag."""
        self.value = value
        self.virtual = virtual

    def __str__(self):
        """Returns the integer value as string."""
        return str(self.value)

    def __int__(self):
        """Returns the value."""
        return self.value

    def __eq__(self, other):
        """Compares the identifier to another."""
        if isinstance(other, self.__class__):
            return self.value == other.value and self.virtual == other.virtual

    def __hash__(self):
        """Hashes the identifier."""
        return hash((self.value, self.virtual))

    @classmethod
    def from_string(cls, string, vid_prefix='v'):
        """Sets the ID from from the provided string."""
        if string.startswith(vid_prefix):
            virtual = True
            string = string[1:]
        else:
            virtual = False

        try:
            value = int(string)
        except ValueError:
            raise InvalidIdentifier(string) from None
        else:
            return cls(value, virtual)

    @property
    def physical(self):
        """Determines whether this is a physical ID."""
        return not self.virtual


class IdentifierList:
    """Represents list of identifiers."""

    def __init__(self, blocks):
        """Sets the blocks."""
        self.blocks = blocks

    def __iter__(self):
        """Yields the respective identifiers."""
        for block in self.blocks:
            try:
                start, end = block
            except ValueError:
                yield block
            else:
                yield start

                for value in range(start.value + 1, end.value):
                    yield Identifier(value, start.virtual)

                yield end

    @property
    def vids(self):
        """Yields VIDs."""
        for identifier in self:
            if identifier.virtual:
                yield identifier.value

    @property
    def tids(self):
        """Yields TIDs."""
        for identifier in self:
            if identifier.physical:
                yield identifier.value


class TerminalSelection:
    """Parses terminal selection expressions."""

    def __init__(self, expression):
        """Sets respective expression."""
        self.expression = expression

    def __str__(self):
        """Returns the expression."""
        return self.expression

    def __iter__(self):
        """Yields the selected terminals."""
        identifiers = self.identifiers

        if identifiers is None:
            yield from Terminal.select().where(Terminal.customer == self.cid)
        else:
            missing = set()

            for identifier in identifiers:
                if identifier.virtual:
                    try:
                        yield Terminal.get(
                            (Terminal.customer == self.cid) &
                            (Terminal.vid == identifier.value))
                    except DoesNotExist:
                        missing.add(identifier)
                else:
                    try:
                        yield Terminal.get(
                            (Terminal.customer == self.cid) &
                            (Terminal.tid == identifier.value))
                    except DoesNotExist:
                        missing.add(identifier)

            if missing:
                raise NoSuchTerminals(self.cid, identifiers)

    @property
    def expression(self):
        """Returns the expression."""
        return self._expression

    @expression.setter
    def expression(self, expression):
        """Sets the expression."""
        self._expression = expression
        self._blocks, self.cid = split_cid(expression)

    @property
    def blocks(self):
        """Returns the parsed blocks."""
        if self._blocks is not None:
            for block in split_blocks(self._blocks):
                yield parse_block(block)

    @property
    def identifiers(self):
        """Returns the selected identifiers."""
        blocks = tuple(self.blocks)

        if blocks:
            return IdentifierList(self.blocks)
