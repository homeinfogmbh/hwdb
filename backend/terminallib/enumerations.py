"""Common enumerations."""

from enum import Enum


__all__ = ['Connection', 'OperatingSystem', 'Type']


class Connection(Enum):
    """Internet connection information."""

    DSL = 'DSL'
    LTE = 'LTE'


class OperatingSystem(Enum):
    """Operating systems."""

    ARCH_LINUX = 'Arch Linux'
    WINDOWS_XP = 'Windows XP'
    # TODO: implement.


class Type(Enum):
    """Terminal classes."""

    DDB = 'Das Digitale Brett'
    ETV = 'Exposé TV'
    ETV_TOUCH = 'Exposé TV touch'
