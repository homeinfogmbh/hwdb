"""Terminal filters"""

from .parse import TerminalSelectionParser
from .db import Terminal


__all__ = ['VidFilter', 'TidFilter', 'TerminalFilter']


class NoSuchTerminals(Exception):
    """Indicates nonexistant terminals"""

    def __init__(self, cid, tids):
        """Sets nonexistant terminals"""
        self.cid = cid
        self.tids = tids
        super().__init__(
            '.'.join([','.join([str(tid) for tid in self.tids]),
                      str(self.cid)]))


class IdFilter():
    """An abstract identifier filter"""

    def __init__(self, cid_or_expr, vids=None, tids=None):
        """Sets the respective expression, TIDs and VIDs"""
        if type(cid_or_expr) is str:
            parser = TerminalSelectionParser(cid_or_expr)
            self._cid = parser.cid
            self._vids = [vid for vid in parser.vids]
            self._tids = [tid for tid in parser.tids]
        else:
            self._cid = cid_or_expr
            self._vids = vids
            self._tids = tids

    @property
    def cid(self):
        """Returns the customer ID"""
        return self._cid

    @property
    def tids(self):
        """Yields the respective tids"""
        if self._parser is not None:
            yield from self._parser.tids
        if self._tids is not None:
            yield from self._tids

    @property
    def vids(self):
        """Yields the respective tids"""
        if self._parser is not None:
            yield from self._parser.vids
        if self._vids is not None:
            yield from self._vids


class VidFilter(IdFilter):
    """Filters expressions for virtual IDs"""

    def __iter__(self):
        """Yields virtual IDs"""
        processed = []
        for vid in self.vids:
            if vid not in processed:
                processed.append(vid)
                yield vid
        for tid in self.tids:
            terminal = Terminal.by_ids(self.cid, tid)
            if terminal is not None:
                vid = terminal.virtual_display
                if vid is not None:
                    if vid not in processed:
                        processed.append(vid)
                        yield vid


class TidFilter(IdFilter):
    """Filters expressions for physical IDs"""

    def __iter__(self):
        """Yields physical identifiers"""
        processed = []
        for tid in self.tids:
            if tid not in processed:
                processed.append(tid)
                yield tid
        for vid in self.vids:
            for terminal in Terminal.by_virt(self.cid, vid):
                tid = terminal.tid
                if tid not in processed:
                    processed.append(tid)
                    yield terminal.tid


class TerminalFilter(IdFilter):
    """Filters expressions for terminal records"""

    def __iter__(self):
        """Yields appropriate terminal records"""
        processed = []
        nonexistant = []
        for tid in self.tids:
            if tid not in processed:
                processed.append(tid)
                terminal = Terminal.by_ids(self.cid, tid)
                if terminal is not None:
                    yield terminal
                else:
                    nonexistant.append(tid)
        for vid in self.vids:
            for terminal in Terminal.by_virt(self.cid, vid):
                yield terminal
