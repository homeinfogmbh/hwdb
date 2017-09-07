"""Terminal selection expression parsing"""

from contextlib import suppress

from peewee import DoesNotExist

from .orm import Terminal

__all__ = [
    'InvalidExpression',
    'InvalidBlock',
    'InvalidIdentifier',
    'InvalidCustomerID',
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


def split_cid(expression, sep='.'):
    """Splits IDs and customer ID."""

    try:
        identifiers, cid = expression.split(sep)
    except ValueError:
        if sep in expression:
            raise InvalidExpression(expression) from None
        else:
            return (None, expression)
    else:
        return (identifiers, cid)


def split_blocks(identifiers, sep=','):
    """Splits TID / VID ID blocks."""

    for block in identifiers.split(sep):
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
        start = Identifier.from_string(block)
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

    def __contains__(self, identifier):
        """Determines whether the block is
        contained within this blocks reange.
        """
        if identifier.virtual:
            return identifier.value in self.vids

        return identifier.value in self.tids

    @property
    def identifiers(self):
        """Yields all identifiers."""
        for block in self.blocks:
            try:
                start, end = block
            except ValueError:
                yield block
            else:
                for value in range(start.value, end.value + 1):
                    yield Identifier(value, start.virtual)

    @property
    def vids(self):
        """Yields VIDs."""
        for identifier in self.identifiers:
            if identifier.virtual:
                yield identifier.value

    @property
    def tids(self):
        """Yields TIDs."""
        for identifier in self.identifiers:
            if identifier.physical:
                yield identifier.value


class TerminalSelection(IdentifierList):
    """Parses terminal selection expressions."""

    def __init__(self, expression):
        """Sets respective expression."""
        identifiers, self._cid = split_cid(expression)
        super().__init__(tuple(
            parse_block(block) for block in split_blocks(identifiers)))

    def __iter__(self):
        """Yields the selected terminals."""
        for vid in self.vids:
            with suppress(DoesNotExist):
                yield Terminal.get(
                    (Terminal.customer == self.cid) &
                    (Terminal.vid == vid))

        for tid in self.tids:
            with suppress(DoesNotExist):
                yield Terminal.get(
                    (Terminal.customer == self.cid) &
                    (Terminal.tid == tid))

    def __contains__(self, _):
        """Overrides inherited containment check, to fall back to __iter__."""
        return NotImplemented

    @property
    def cid(self):
        """Returns the customer ID."""
        try:
            return int(self._cid)
        except ValueError:
            raise InvalidCustomerID(self._cid)
