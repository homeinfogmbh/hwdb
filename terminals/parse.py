"""Terminal selection expression parsing"""

from .orm import Terminal

__all__ = ['InvalidCustomerID', 'InvalidTerminalIDs', 'InvalidRangeError',
           'InvalidIDError', 'NoSuchTerminals', 'TerminalSelectionParser']


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


class TerminalSelectionParser():
    """Parses terminal selection expressions"""

    IDENT_SEP = '.'
    VID_PREFIX = 'v'
    BLOCK_SEP = ','
    RANGE_SEP = '-'
    ALL = ['*']

    def __init__(self, expr):
        """Sets respective expression"""
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
        ident_str = self._ident_str
        if ident_str is not None:
            for block in ident_str.split(self.BLOCK_SEP):
                if block:
                    yield block

    @property
    def vids(self):
        """Yields virtual identifiers"""
        for block in self._blocks:
            if block.startswith(self.VID_PREFIX):
                block = block[1:]
                yield from self._block_range(block, virtual=True)

    @property
    def tids(self):
        """Yields physical identifiers"""
        for block in self._blocks:
            if not block.startswith(self.VID_PREFIX):
                yield from self._block_range(block, virtual=False)

    def _block_range(self, block, virtual=False):
        """Yields elements of a block range or a single ID"""
        if self.RANGE_SEP in block:
            try:
                start, end = block.split(self.RANGE_SEP)
            except ValueError:
                if block in self.ALL:
                    start = None
                    end = None
                else:
                    raise InvalidRangeError(block)
            else:
                # Parse start
                try:
                    start = int(start)
                except ValueError:
                    if start == '':
                        start = None
                    else:
                        raise InvalidIDError(start)
                # Parse end
                try:
                    end = int(end)
                except ValueError:
                    if end == '':
                        end = None
                    else:
                        raise InvalidIDError(end)

                # Disallow leaving out both start
                # and range on range definition
                if start is None and range is None:
                    raise InvalidRangeError(block)

            # Derive ranges
            if start is None:
                if virtual:
                    start = Terminal.min_vid(self.cid)
                else:
                    start = Terminal.min_id(self.cid)
            if end is None:
                if virtual:
                    start = Terminal.max_vid(self.cid)
                else:
                    start = Terminal.max_tid(self.cid)

            yield from range(start, end+1)

        else:
            try:
                ident = int(block)
            except ValueError:
                raise InvalidIDError(block)
            else:
                yield ident
