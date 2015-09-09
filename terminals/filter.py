"""Terminal filters"""

from .parse import VidParser, TidParser
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

    def __init__(self, expr=None, vids=None, tids=None):
        """Sets the respective expression, TIDs and VIDs"""
        self._vid_parser = VidParser(expr) if expr is not None else None
        self._tid_parser = TidParser(expr) if expr is not None else None
        self._vids = vids
        self._tids = tids

    @property
    def tids(self):
        """Yields the respective tids"""
        if self._tid_parser is not None:
            yield from self._tid_parser
        if self._tids is not None:
            yield from self._tids

    @property
    def vids(self):
        """Yields the respective tids"""
        if self._vid_parser is not None:
            yield from self._vid_parser
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
