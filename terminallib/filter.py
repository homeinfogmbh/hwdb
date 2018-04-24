"""Terminal filters."""

from terminallib.orm import Class, OS, Terminal

__all__ = ['parse', 'get_terminals']


def _online(terminal_expr):
    """Yields online terminals."""

    for terminal in Terminal.select().where(terminal_expr):
        if terminal.online:
            yield terminal


def parse(expressions):
    """Returns a peewee.Expression for the respective terminal expressions."""

    if not expressions:
        return True

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


def get_terminals(expressions, deployed=None, testing=None, classes=None,
                  os=None, online=None):
    """Yields terminals for the respective expressions and filters."""

    terminal_expr = parse(expressions)

    if deployed is not None:
        if deployed in (True, False):
            if deployed:
                terminal_expr &= ~ (Terminal.deployed >> None)
            else:
                terminal_expr &= Terminal.deployed >> None
        else:  # Compare to datetime.
            terminal_expr &= Terminal.deployed == deployed

    if testing is not None:
        if testing:
            terminal_expr &= Terminal.testing == 1
        else:
            terminal_expr &= Terminal.testing == 0

    if classes:
        class_ids = []

        for value in classes:
            try:
                class_id = int(value)
            except ValueError:
                class_ = Class.get(
                    (Class.name == value) | (Class.full_name == value))
                class_id = class_.id

            class_ids.append(class_id)

        terminal_expr &= Terminal.class_ >> class_ids

    if os is not None:
        try:
            os_ = int(os)
        except ValueError:
            os_ = OS.get((OS.family == os) | (OS.name == os))

        terminal_expr &= Terminal.os == os_

    if online:
        return _online(terminal_expr)

    return Terminal.select().where(terminal_expr)
