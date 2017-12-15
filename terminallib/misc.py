"""Miscellaneous functions."""

from string import ascii_letters, digits

__all__ = ['LET_DIG', 'LET_DIG_HYP', 'is_label', 'get_hostname']


LET_DIG = ascii_letters + digits
LET_DIG_HYP = LET_DIG + '-'


def is_label(string, strict=True):
    """Checks whether the string is a label according to RFC-1035.
    See: <https://tools.ietf.org/html/rfc1035>.
    """

    if not string:
        return False

    if strict:
        if string[0] not in ascii_letters:
            return False
    else:
        if string[0] not in LET_DIG:
            return False

    if string[-1] not in LET_DIG:
        return False

    if not all(char in LET_DIG_HYP for char in string):
        return False

    return True


def get_hostname(customer):
    """Returns a host name from the respective customer."""

    if is_label(customer.cid, strict=False):
        return customer.cid

    return str(customer.id)