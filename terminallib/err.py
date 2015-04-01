"""Library for terminal configuration errors"""

__date__ = "23.03.2015"
__author__ = "Richard Neumann <r.neumann@homeinfo.de>"
__all__ = ['KeygenError', 'UnconfiguredError']


class KeygenError(Exception):
    """Indicates error in key generation"""
    pass


class UnconfiguredError(Exception):
    """Indicates error in key generation"""
    pass
