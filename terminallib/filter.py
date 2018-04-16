"""Terminal filters."""

from terminallib.orm import Terminal

__all__ = ['parse', 'terminals']


def parse(expressions):
    """Yields parsers from expressions"""

    terminal_expr = None

    for expression in expressions:
        try:
            tid, cid = expression.split('.')
        except ValueError:
            expr = Terminal.customer == expression
        else:
            expr = (Terminal.tid == tid) & (Terminal.customer == cid)

        if terminal_expr is None:
            terminal_expr = expr
        else:
            terminal_expr |= expr

    if terminal_expr is None:
        return True

    return terminal_expr


def terminals(expressions):
    """Yields terminals for the respective expressions."""

    return Terminal.select().where(parse(expressions))
