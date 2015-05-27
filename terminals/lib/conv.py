"""Terminal data conversion"""

from datetime import datetime
from . import dom
# from . import db
from contextlib import suppress

__all__ = ['terminal2dom', 'pr2dom']


def terminal2dom(terminal):
    """Converts a terminal ORM instance
    to a terminal DOM instance
    """
    result = dom.TerminalShortInfo()
    # Elements
    class_ = dom.Class(terminal.class_.name)
    class_.full_name = terminal.class_.full_name
    class_.touch = terminal.class_.touch
    result.class_ = class_
    # Attributes
    result.tid = terminal.tid
    result.cid = terminal.customer.id
    if terminal.deleted is not None:
        result.deleted = terminal.deleted
    result.status = True  # TODO: Implement
    result.ipv4addr_ = str(terminal.ipv4addr)
    result.domain = terminal.domain.fqdn
    # Screenshot thubnail
    # TODO: Implement
    thumbnail = dom.Picture('Not implemented'.encode())
    thumbnail.mimetype = 'text/plain'
    thumbnail.timestamp = datetime.now()
    result.thumbnail = thumbnail
    return result


def pr2dom(process_result):
    """Converts a ProcessResult instance
    to a terminal DOM instance
    """
    result = dom.TerminalResult()
    result.exit_code = process_result.exit_code
    if process_result.stdout is not None:
        with suppress(ValueError):
            result.stdout = process_result.stdout.decode()
    if process_result.stderr is not None:
        with suppress(ValueError):
            result.stderr = process_result.stderr.decode()
    return result
