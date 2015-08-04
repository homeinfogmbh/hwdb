"""Miscellaneous library"""

from math import pi

from .db import Terminal

__all__ = ['TerminalGetter', 'Rotation']


class TerminalGetter():
    """Gets terminals by ID strings"""

    _IDENT_SEP = ','
    _VID_PREFIX = 'v'

    def __init__(self, expr):
        """Sets the terminal expression"""
        try:
            idents, cid = expr.split('.')
        except (ValueError, TypeError):
            idents = None
            cid = expr
        self._cid = int(cid)
        self._idents = idents

    def __iter__(self):
        """Yields appropriate terminals"""
        if self._idents is None:
            for terminal in Terminal.select().where(
                    Terminal.customer == self._cid):
                yield terminal
        else:
            processed = []
            for vid in self.vids:
                for terminal in Terminal.select().where(
                        (Terminal.customer == self._cid) &
                        (Terminal.virtual_display == vid)):
                    ident = terminal.id
                    if ident not in processed:
                        processed.append(ident)
                        yield terminal
            for tid in self.tids:
                for terminal in Terminal.select().where(
                        (Terminal.customer == self._cid) &
                        (Terminal.tid == tid)):
                    ident = terminal.id
                    if ident not in processed:
                        processed.append(ident)
                        yield terminal

    def vid2tids(self, vid):
        """Converts a virtual ID into a physical ID"""
        for terminal in Terminal.select().where(
                (Terminal.customer == self._cid) &
                (Terminal.virtual_display == vid)):
            yield terminal.tid

    @property
    def vids(self):
        """Yields virtual IDs"""
        processed = []
        if self._idents is None:
            return None
        else:
            for ident in self._idents.split(self._IDENT_SEP):
                if ident:
                    if ident.startswith(self._VID_PREFIX):
                        vid = ident.replace(self._VID_PREFIX, '')
                        try:
                            vid = int(vid)
                        except ValueError:
                            raise ValueError('VID must be an integer')
                        else:
                            if vid not in processed:
                                processed.append(vid)
                                yield vid

    @property
    def tids(self):
        """Yields physical terminal IDs"""
        processed = []
        if self._idents is None:
            return None
        else:
            for ident in self._idents.split(self._IDENT_SEP):
                if ident:
                    if not ident.startswith(self._VID_PREFIX):
                        try:
                            tid = int(ident)
                        except ValueError:
                            raise ValueError('TID must be an integer')
                        else:
                            if tid not in processed:
                                processed.append(tid)
                                yield tid


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
            raise ValueError('Degrees must be one of: {0}'.format(
                self._VALID_DEGREES))

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
            raise ValueError('Pi multiplier must be one of: {0}'.format(
                self._VALID_PI_MULTIS))
