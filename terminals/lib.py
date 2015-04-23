"""Miscellaneous library"""

from math import pi

__date__ = "23.04.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['Rotation']


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
        elif degrees:
            if degrees in self._VALID_DEGREES:
                self._degrees = degrees
                self._pi = None
            else:
                raise ValueError(' '.join(['Degrees must be one of:',
                                           str(self._VALID_DEGREES)]))
        elif pi:
            if pi in self._VALID_PI_MULTIS:
                self._pi = pi
                self._degrees = None
            else:
                raise ValueError(' '.join(['Pi multiplier must be one of:',
                                           str(self._VALID_PI_MULTIS)]))

    def __repr__(self):
        """Converts the rotation to a string"""
        if self._degrees is not None:
            return str(self._degrees)
        elif self._pi is not None:
            return str(self._pi)

    def __str__(self):
        """Converts the rotation to a string"""
        if self._degrees is not None:
            return str(self._degrees) + '°'
        elif self._pi is not None:
            return str(self._pi) + ' π'

    def __int__(self):
        """Converts the rotation into an integer value"""
        return self.degrees

    def __float__(self):
        """Converts the rotation into a float value"""
        return self.pi * pi

    @property
    def degrees(self):
        """Returns the rotation in degrees"""
        if self._degrees is not None:
            return self._degrees
        else:
            return int(self._pi * 180)

    @property
    def pi(self):
        """Returns the rotation in multiples of pi"""
        if self._pi is not None:
            return self._pi
        else:
            return self._degrees / 180
