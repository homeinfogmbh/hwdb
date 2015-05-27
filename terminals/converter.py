"""Terminal data conversion"""


def orm2dom(terminal_orm):
    """Converts a terminal ORM instance
    to a terminal DOM instance
    """
    tso = dom.TerminalShortInfo()
    # Elements
    class_ = dom.TerminalClass(terminal.class_.name)
    class_.full_name = terminal.class_.full_name
    class_.touch = terminal.class_.touch
    tso.class_ = class_
    # Attributes
    tso.tid = terminal.tid
    tso.cid = terminal.customer.id
    if terminal.deleted is not None:
        tso.deleted = terminal.deleted
    tso.status = True  # TODO: Implement
    tso.ipv4addr_ = str(terminal.ipv4addr)
    tso.domain = terminal.domain.fqdn
    # Screenshot thubnail
    # TODO: Implement
    thumbnail = dom.Picture('Not implemented'.encode())
    thumbnail.mimetype = 'text/plain'
    thumbnail.timestamp = datetime.now()
    tso.thumbnail = thumbnail