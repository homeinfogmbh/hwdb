"""Terminal filters"""

from contextlib import suppress

from peewee import DoesNotExist

from homeinfo.terminals.orm import Terminal
from homeinfo.terminals.parse import TerminalSelection

__all__ = ['parse', 'terminals']


def parse(*expressions):
    """Yields parsers from expressions"""

    for expression in expressions:
        for terminal in TerminalSelection(expression):
            yield terminal


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
