"""Miscellaneous library"""

from math import pi
from datetime import datetime
from contextlib import suppress
from . import dom
# from . import db

__all__ = ['terminal2dom', 'pr2dom', 'Rotation']


def terminal2dom(terminal):
    """Converts a terminal ORM instance
    to a terminal DOM instance
    """
    result = dom.BasicTerminalInfo()
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
    thumbnail = dom.Screenshot('Not implemented'.encode())
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


class Rotation():
    """Terminal rotation"""

    _VALID_DEGREES = [0, 90, 180, 270]
    _VALID_PI_MULTIS = [0, 1/2, 1, 3/2]

    def __init__(self, degrees=None, pi=None):
        """Initializes the rotation with
        either degrees or multiples of pi
        XXX: Rotation is always clockwise
        """
        if degrees is None and pi is None:
            raise ValueError('Must specify either degrees or pi')
        elif degrees is not None and pi is not None:
            raise ValueError('Must specify either degrees or pi')
        elif degrees is not None:
            self.degrees = degrees
        else:
            self.pi = pi

    def __repr__(self):
        """Converts the rotation to a string"""
        if self._degrees is not None:
            return str(self._degrees)
        else:
            return str(self._pi)

    def __str__(self):
        """Converts the rotation to a string"""
        if self._degrees is not None:
            return str(self._degrees) + '°'
        else:
            return str(self._pi) + ' π'

    def __int__(self):
        """Converts the rotation into an integer value"""
        return self.degrees

    def __float__(self):
        """Converts the rotation into a float value"""
        return self.pi * pi

    def __bool__(self):
        """Converts the rotation into a boolean value"""
        return False if int(self) == 0 else True

    @property
    def degrees(self):
        """Returns the rotation in degrees"""
        if self._degrees is not None:
            return self._degrees
        else:
            return int(self._pi * 180)

    @degrees.setter
    def degrees(self, degrees):
        """Sets the amount of degrees"""
        if degrees in self._VALID_DEGREES:
            self._degrees = degrees
            self._pi = None
        else:
            raise ValueError(' '.join(['Degrees must be one of:',
                                       str(self._VALID_DEGREES)]))

    @property
    def pi(self):
        """Returns the rotation in multiples of pi"""
        if self._pi is not None:
            return self._pi
        else:
            return self._degrees / 180

    @pi.setter
    def pi(self, pi):
        """Sets the pi multiplier"""
        if pi in self._VALID_PI_MULTIS:
            self._pi = pi
            self._degrees = None
        else:
            raise ValueError(' '.join(['Pi multiplier must be one of:',
                                       str(self._VALID_PI_MULTIS)]))
