"""Terminal filters."""

from collections import defaultdict
from contextlib import suppress
from sys import stderr

from peewee import DoesNotExist

from terminallib.orm import Terminal
from terminallib.parse import NoSuchCustomer, MissingTerminals, \
    TerminalSelection

__all__ = ['ParsingError', 'parse', 'terminals', 'PrintErrors']


class ParsingError(Exception):
    """Idicates that the respective terminals are missing."""

    def __init__(self, invalid_customers, invalid_terminals):
        """Sets the missing terminals dictionary."""
        super().__init__(invalid_customers, invalid_terminals)
        self.invalid_customers = invalid_customers
        self.invalid_terminals = invalid_terminals

    def __str__(self):
        """Returns the complete error message."""
        return '\n'.join(self.messages)

    @property
    def customers(self):
        """Yields missing customer IDs."""
        for cids in self.invalid_customers:
            yield '/'.join(cids)

    @property
    def terminals(self):
        """Yields the missing terminal IDs."""
        for customer, identifiers in self.invalid_terminals.items():
            for identifier in identifiers:
                yield '{}.{}'.format(identifier, repr(customer))

    @property
    def messages(self):
        """Yields messages."""
        for customer in self.customers:
            yield 'No such customer: {}.'.format(customer)

        for terminal in self.terminals:
            yield 'No such terminal: {}.'.format(terminal)


def parse(*expressions, quiet=False):
    """Yields parsers from expressions"""

    invalid_customers = set()
    invalid_terminals = defaultdict(set)

    for expression in expressions:
        try:
            for terminal in TerminalSelection(expression):
                yield terminal
        except NoSuchCustomer as no_such_customer:
            invalid_customers.add(tuple(no_such_customer.cids))
        except MissingTerminals as missing_terminals:
            invalid_terminals[missing_terminals.customer].update(
                missing_terminals.identifiers)

    if invalid_customers or invalid_terminals:
        if not quiet:
            raise ParsingError(invalid_customers, invalid_terminals)


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


class PrintErrors:
    """Context to print out missing terminals."""

    def __init__(self, file=stderr):
        """Sets the output file."""
        self.file = file

    def __enter__(self):
        """Returns itself."""
        return self

    def __exit__(self, _, value, __):
        """Checks for NoSuchTerminals exception."""
        if isinstance(value, ParsingError):
            print(value, file=self.file, flush=True)
            return True
