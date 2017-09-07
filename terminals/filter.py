"""Terminal filters"""

from contextlib import suppress
from sys import stderr

from peewee import DoesNotExist

from .orm import Terminal
from .parse import MissingTerminals, TerminalSelection

__all__ = ['NoSuchTerminals', 'parse', 'terminals', 'PrintMissing']


class NoSuchTerminals(Exception):
    """Idicates that the respective terminals are missing."""

    def __init__(self, missing):
        """Sets the missing terminals dictionary."""
        super().__init__(missing)
        self.missing = missing

    def __str__(self):
        """Prints the missing terminal IDs."""
        return '\n'.join(
            'Missing terminal: {}.'.format(terminal)
            for terminal in self.terminals)

    @property
    def terminals(self):
        """Yields the missing terminal IDs."""
        for cid, identifiers in self.missing.items():
            for identifier in identifiers:
                yield '{}.{}'.format(cid, identifier)


def parse(*expressions, quiet=False):
    """Yields parsers from expressions"""

    missing = {}

    for expression in expressions:
        try:
            for terminal in TerminalSelection(expression):
                yield terminal
        except MissingTerminals as missing_terminals:
            try:
                missing[missing_terminals.cid].update(
                    missing_terminals.identifiers)
            except KeyError:
                missing[missing_terminals.cid] = missing_terminals.identifiers

    if not quiet and missing:
        raise NoSuchTerminals(missing)


def terminals(customer, vids=None, tids=None):
    """Yields terminals for the respective customer, TIDs and VIDs."""

    if vids:
        vids = set(vids)

    if tids:
        tids = set(tids)

    if not vids and not tids:
        yield from Terminal.select().where(Terminal.customer == customer)
    else:
        for vid in vids:
            with suppress(DoesNotExist):
                yield Terminal.get(
                    (Terminal.customer == customer) &
                    (Terminal.vid == vid))

        for tid in tids:
            with suppress(DoesNotExist):
                yield Terminal.get(
                    (Terminal.customer == customer) &
                    (Terminal.tid == tid))


class PrintMissing:
    """Context to print out missing terminals."""

    def __init__(self, template='Missing terminal: {}.', file=stderr):
        """Sets the output file."""
        self.template = template
        self.file = file

    def __enter__(self):
        """Returns itself."""
        return self

    def __exit__(self, typ, value, _):
        """Checks for NoSuchTerminals exception."""
        if typ is NoSuchTerminals:
            print(type(value))
            print(str(value))
            print(value, file=self.file, flush=True)
            return True
