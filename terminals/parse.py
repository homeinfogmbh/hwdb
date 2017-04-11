"""Terminal selection expression parsing"""

from homeinfo.terminals.orm import Terminal

__all__ = [
    'InvalidCustomerID',
    'InvalidTerminalIDs',
    'InvalidRangeError',
    'InvalidIDError',
    'TerminalSelectionParser']


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
                yield from self._block_range(block[1:], virtual=True)

    @property
    def tids(self):
        """Yields physical identifiers"""
        for block in self._blocks:
            if not block.startswith(self.VID_PREFIX):
                yield from self._block_range(block, virtual=False)

    def _block_range(self, block, virtual=False):
        """Yields elements of a block range or a single ID"""
        try:
            yield int(block)
        except ValueError:
            if block in self.ALL:
                start = None
                end = None
            elif self.RANGE_SEP in block:
                try:
                    start, end = block.split(self.RANGE_SEP)
                except ValueError:
                    raise InvalidRangeError(block) from None
                else:
                    if start == '':
                        start = None
                    else:
                        try:
                            start = int(start)
                        except ValueError:
                            raise InvalidIDError(start) from None

                    if end == '':
                        end = None
                    else:
                        try:
                            end = int(end)
                        except ValueError:
                            raise InvalidIDError(end) from None

                # Disallow leaving out both start
                # and end on range definition using "-"
                if start is None and end is None:
                    raise InvalidRangeError(block) from None
            else:
                raise InvalidRangeError(block) from None

            if start is None:
                if virtual:
                    start = Terminal.min_vid(self.cid)
                else:
                    start = Terminal.min_id(self.cid)

            if end is None:
                if virtual:
                    end = Terminal.max_vid(self.cid)
                else:
                    end = Terminal.max_tid(self.cid)

            yield from range(start, end+1)
