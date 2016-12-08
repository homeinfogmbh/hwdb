"""Terminal filters"""

from itertools import chain

from peewee import DoesNotExist

from .orm import Terminal
from .parse import TerminalSelectionParser

__all__ = [
    'NoSuchTerminals',
    'parse',
    'VidFilter',
    'TidFilter',
    'TerminalFilter']


class NoSuchTerminals(Exception):
    """Indicates nonexistant terminals"""

    def __init__(self, cids):
        """Sets nonexistant terminals"""
        self.cids = cids


def parse(*expressions, fltr=None):
    """Yields parsers from expressions"""

    fltr = TerminalFilter if fltr is None else fltr
    processed = set()
    missing = {}

    for expression in expressions:
        try:
            for result in fltr(expression):
                if result not in processed:
                    processed.add(result)
                    yield result
        except NoSuchTerminals as e:
            for cid in e.cids:
                try:
                    tids_ = missing[cid]
                except KeyError:
                    missing[cid] = e.cids[cid]
                else:
                    for tid in e.cids[cid]:
                        tids_.append(tid)

    if missing:
        raise NoSuchTerminals(missing)


class IdFilter():
    """An abstract identifier filter"""

    def __init__(self, cid_or_expr, vids=None, tids=None):
        """Sets the respective expression, TIDs and VIDs"""
        if type(cid_or_expr) is int:
            self._parser = None
            self._cid = cid_or_expr
            self._vids = vids
            self._tids = tids
        else:
            self._parser = TerminalSelectionParser(cid_or_expr)
            self._cid = None
            self._vids = None
            self._tids = None

    @property
    def cid(self):
        if self._parser is None:
            return self._cid
        else:
            return self._parser.cid

    @property
    def vids(self):
        if self._parser is None:
            if self._vids is not None:
                yield from self._vids
        else:
            yield from self._parser.vids

    @property
    def tids(self):
        if self._parser is None:
            if self._tids is not None:
                yield from self._tids
        else:
            yield from self._parser.tids

    @property
    def all(self):
        """Determines whether all terminals should be selected

        XXX: This is True iff no VID or TID has been specified
        """
        for _ in chain(self.vids, self.tids):
            return False
        else:
            return True


class VidFilter(IdFilter):
    """Filters expressions for virtual IDs"""

    def __iter__(self):
        """Yields virtual IDs"""
        processed = set()

        if self.all:
            for terminal in Terminal.by_cid(self.cid):
                if terminal.vid is not None:
                    if terminal.vid not in processed:
                        processed.add(terminal.vid)
                        yield terminal.vid
        else:
            for vid in self.vids:
                if vid not in processed:
                    processed.add(vid)
                    yield vid

            for tid in self.tids:
                try:
                    terminal = Terminal.by_ids(self.cid, tid)
                except DoesNotExist:
                    pass
                else:
                    if terminal.vid is not None:
                        if terminal.vid not in processed:
                            processed.add(terminal.vid)
                            yield terminal.vid


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
                    if terminal.tid not in processed:
                        processed.add(terminal.tid)
                        yield terminal.tid


class TerminalFilter(IdFilter):
    """Filters expressions for terminal records"""

    def __iter__(self):
        """Yields appropriate terminal records"""
        if self.all:
            yield from Terminal.by_cid(self.cid)
        else:
            processed = set()
            nonexistant = set()

            for tid in self.tids:
                if tid not in processed:
                    processed.add(tid)

                    try:
                        terminal = Terminal.by_ids(self.cid, tid)
                    except DoesNotExist:
                        nonexistant.add(tid)
                    else:
                        yield terminal

            for vid in self.vids:
                for terminal in Terminal.by_virt(self.cid, vid):
                    if terminal.tid not in processed:
                        processed.add(terminal.tid)
                        yield terminal

            if nonexistant:
                raise NoSuchTerminals({self.cid: nonexistant})
