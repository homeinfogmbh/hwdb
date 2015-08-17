"""Application programming interface"""

from .db import Terminal

__all__ = ['TerminalGetter']


class TerminalGetter():
    """Gets terminals by ID strings"""

    _IDENT_SEP = ','
    _IDENT_RANGE = '-'
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
                if ident.startswith(self._VID_PREFIX):
                    vid = ident.replace(self._VID_PREFIX, '')
                    try:
                        start, end = ident.split(self._IDENT_RANGE)
                    except ValueError:
                        try:
                            vid = int(vid)
                        except ValueError:
                            raise ValueError('VID must be an integer')
                        else:
                            if vid not in processed:
                                processed.append(vid)
                                yield vid
                    else:
                        try:
                            start, end = int(start), int(end)
                        except (ValueError, TypeError):
                            raise ValueError('VID must be an integer')
                        else:
                            for vid in range(start, end+1):
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
                if ident and not ident.startswith(self._VID_PREFIX):
                    try:
                        start, end = ident.split(self._IDENT_RANGE)
                    except ValueError:
                        try:
                            tid = int(ident)
                        except ValueError:
                            raise ValueError('VID must be an integer')
                        else:
                            if tid not in processed:
                                processed.append(tid)
                                yield tid
                    else:
                        try:
                            start, end = int(start), int(end)
                        except (ValueError, TypeError):
                            raise ValueError('VID must be an integer')
                        else:
                            for tid in range(start, end+1):
                                if tid not in processed:
                                    processed.append(tid)
                                    yield tid
