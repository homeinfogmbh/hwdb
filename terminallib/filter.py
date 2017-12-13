"""Terminal filters."""

from collections import defaultdict
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

    def __iter__(self):
        """Yields the missing terminal IDs."""
        for cid, identifiers in self.missing.items():
            for identifier in identifiers:
                yield '{}.{}'.format(identifier, cid)


def parse(*expressions, quiet=False):
    """Yields parsers from expressions"""

    missing = defaultdict(set)

    for expression in expressions:
        try:
            for terminal in TerminalSelection(expression):
                yield terminal
        except MissingTerminals as missing_terminals:
            missing[missing_terminals.cid].update(
                missing_terminals.identifiers)

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
            for ident in value:
                print(self.template.format(ident), file=self.file, flush=True)

            return True