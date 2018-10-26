"""Terminal filters."""

from terminallib.orm import Class, OS, Terminal


__all__ = ['parse', 'get_terminals']


def filter_online(terminals):
    """Yields online terminals."""

    for terminal in terminals:
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
                  oss=None, online=None):
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
        class_ids = set()

        for class_desc in classes:
            try:
                class_id = int(class_desc)
            except ValueError:
                class_ = Class.get(
                    (Class.name == class_desc)
                    | (Class.full_name == class_desc))
                class_id = class_.id

            class_ids.add(class_id)

        terminal_expr &= Terminal.class_ << class_ids

    if oss:
        os_ids = set()

        for od_desc in oss:
            try:
                os_id = int(od_desc)
            except ValueError:
                os_ = OS.get((OS.family == od_desc) | (OS.name == od_desc))
                os_id = os_.id

            os_ids.add(os_id)

        terminal_expr &= Terminal.os << os_ids

    terminals = Terminal.select().where(terminal_expr)

    if online:
        return filter_online(terminals)

    return terminals
