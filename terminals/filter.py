"""Terminal filters"""

from .orm import Terminal
from .parse import TerminalSelectionParser

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
        if type(cid_or_expr) is int:
            self.cid = cid_or_expr
            self.vids = vids or set()
            self.tids = tids or set()
        else:
            parser = TerminalSelectionParser(cid_or_expr)
            self.cid = parser.cid
            self.vids = {vid for vid in parser.vids}
            self.tids = {tid for tid in parser.tids}

    @property
    def all(self):
        """Determines whether all terminals should be selected"""
        if not self.vids and not self.tids:
            return True
        else:
            return False


class VidFilter(IdFilter):
    """Filters expressions for virtual IDs"""

    def __iter__(self):
        """Yields virtual IDs"""
        processed = set()
        if self.all:
            for terminal in Terminal.by_cid(self.cid):
                vid = terminal.vid
                if vid is not None:
                    if vid not in processed:
                        processed.add(vid)
                        yield vid
        else:
            for vid in self.vids:
                if vid not in processed:
                    processed.add(vid)
                    yield vid
            for tid in self.tids:
                terminal = Terminal.by_ids(self.cid, tid)
                if terminal is not None:
                    vid = terminal.vid
                    if vid is not None:
                        if vid not in processed:
                            processed.add(vid)
                            yield vid


class TidFilter(IdFilter):
    """Filters expressions for physical IDs"""

    def __iter__(self):
        """Yields physical identifiers"""
        if self.all:
            for terminal in Terminal.by_cid(self.cid):
                yield terminal.tid
        else:
            processed = set()
            for tid in self.tids:
                if tid not in processed:
                    processed.add(tid)
                    yield tid
            for vid in self.vids:
                for terminal in Terminal.by_virt(self.cid, vid):
                    tid = terminal.tid
                    if tid not in processed:
                        processed.add(tid)
                        yield terminal.tid


class TerminalFilter(IdFilter):
    """Filters expressions for terminal records"""

    def __iter__(self):
        """Yields appropriate terminal records"""
        if self.all:
            for terminal in Terminal.by_cid(self.cid):
                yield terminal
        else:
            processed = set()
            nonexistant = set()
            for tid in self.tids:
                if tid not in processed:
                    processed.add(tid)
                    terminal = Terminal.by_ids(self.cid, tid)
                    if terminal is not None:
                        yield terminal
                    else:
                        nonexistant.add(tid)
            for vid in self.vids:
                for terminal in Terminal.by_virt(self.cid, vid):
                    tid = terminal.tid
                    if tid not in processed:
                        processed.add(tid)
                        yield terminal
            if nonexistant:
                raise NoSuchTerminals(self.cid, nonexistant)
