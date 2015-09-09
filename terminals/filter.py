"""Terminal filters"""

from .db import Terminal


class InvalidCustomerID(Exception):
    """Indicates an invalid customer ID"""
    pass


class InvalidTerminalIDs(Exception):
    """Indicates invalid terminal identifiers"""
    pass


class InvalidRangeError(Exception):
    """Indicates an invalid ID range definition"""
    pass


class InvalidIDError(Exception):
    """Indicates an invalid ID"""
    pass


class NoSuchTerminals(Exception):
    """Indicates nonexistant terminals"""

    def __init__(self, cid, tids):
        """Sets nonexistant terminals"""
        self.cid = cid
        self.tids = tids
        super().__init__(
            '.'.join([','.join([str(tid) for tid in self.tids]),
                      str(self.cid)]))


class ExpressionParser():
    """Parses terminal selection expressions"""

    IDENT_SEP = '.'
    VID_PREFIX = 'v'
    BLOCK_SEP = ','
    RANGE_SEP = '-'

    def __init__(self, expr):
        """Initializes with the respective expression"""
        self._ids_cid = expr.split(self.IDENT_SEP)

    @property
    def _cid_str(self):
        """Returns the raw customer ID string"""
        return self._ids_cid[-1]

    @property
    def cid(self):
        """Returns the customer ID"""
        try:
            cid = int(self._cid_str)
        except ValueError:
            raise InvalidCustomerID(self._cid_str)
        else:
            return cid

    @property
    def _ident_str(self):
        """Returns the respective ID expressions"""
        ids_c = len(self._ids_cid)
        if ids_c == 1:
            return None
        elif ids_c == 2:
            return self._ids_cid[0]
        else:
            raise InvalidTerminalIDs()

    @property
    def _blocks(self):
        """Yields identifier blocks"""
        for block in self._ident_str.split(self.BLOCK_SEP):
            if block:
                yield block

    def _block_range(self, block):
        """Yields elements of a block range or a single ID"""
        if self.RANGE_SEP in block:
            try:
                start, end = block.split(self.RANGE_SEP)
            except ValueError:
                raise InvalidRangeError(block)
            else:
                try:
                    start = int(start)
                except ValueError:
                    raise InvalidIDError(start)
                else:
                    try:
                        end = int(end)
                    except ValueError:
                        raise InvalidIDError(start)
                    else:
                        return range(start, end+1)
        else:
            try:
                ident = int(block)
            except ValueError:
                raise InvalidIDError(block)
            else:
                yield ident

    def vids(self):
        """Yields virtual IDs"""
        for block in super.__iter__():
            if block.startswith(self.VID_PREFIX):
                block = block[1:]
                yield from self._block_range(block)

    def tids(self):
        """Yields physical identifiers"""
        for block in self.ident_blocks:
            if not block.startswith(self.VID_PREFIX):
                yield from self._block_range(block)


class VirtualIDFilter(ExpressionParser):
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


class TerminalIDFilter(ExpressionParser):
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


class TerminalFilter(ExpressionParser):
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
