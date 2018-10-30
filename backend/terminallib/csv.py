"""Terminal to CSV conversion."""

from collections import namedtuple


__all__ = ['TerminalCSVRecord']


SEP = ';'
_FIELDS = ('tid', 'cid', 'street', 'house_number', 'zip_code', 'city')


class TerminalCSVRecord(namedtuple('TerminalCSVRecord', _FIELDS)):
    """A terminal CSV record."""

    __slots__ = ()

    def __str__(self):
        """Returns a CSV representation of the respective terminal."""
        return SEP.join(map(lambda col: '' if col is None else str(col), self))

    @classmethod
    def from_terminal(cls, terminal):
        """Creates a TerminalCSV record from the respective terminal."""
        address = terminal.address

        if address is None:
            street = None
            house_number = None
            zip_code = None
            city = None
        else:
            street = address.street
            house_number = address.house_number
            zip_code = address.zip_code
            city = address.city

        return cls(terminal.tid, terminal.customer.id, street, house_number,
                   zip_code, city)
