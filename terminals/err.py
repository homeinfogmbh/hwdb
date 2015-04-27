"""Library for terminal configuration errors"""

__all__ = ['KeygenError', 'UnconfiguredError']


class KeygenError(Exception):
    """Indicates error in key generation"""
    pass


class UnconfiguredError(Exception):
    """Indicates error in key generation"""
    pass
