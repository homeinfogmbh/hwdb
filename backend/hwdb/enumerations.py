"""Common enumerations."""

from enum import Enum


__all__ = ['from_string', 'Connection', 'Module', 'OperatingSystem', 'Type']


def from_string(enum, value):
    """Returns an enumeration from a text value."""

    try:
        return enum(value)
    except ValueError:
        return enum[value]


class Connection(Enum):
    """Internet connection information."""

    DSL = 'DSL'
    LTE = 'LTE'


class Module(Enum):
    """Available software modules."""

    TENANT_TO_TENANT = 'tenant-to-tenant'
    CLEANING_PROOF = 'cleaning-proof'
    LPT_TIMETABLES = 'lpt-timetables'
    NEWS = 'news'


class OperatingSystem(Enum):
    """Operating systems."""

    ARCH_LINUX = 'Arch Linux'
    WINDOWS_XP = 'Windows XP'
    WINDOWS_XP_EMBEDDED = 'Windows XP Embedded'
    WINDOWS_EMBEDDED_STANDARD = 'Windows Embedded Standard'
    WINDOWS7 = 'Windows 7'
    WINDOWS7_EMBEDDED = 'Windows 7 Embedded'
    WINDOWS8 = 'Windows 8'
    WINDOWS81 = 'Windows 8.1'
    WINDOWS10 = 'Windows 10'


class Type(Enum):
    """Terminal classes."""

    DDB = 'Das Digitale Brett'
    ETV = 'Exposé TV'
    ETV_TOUCH = 'Exposé TV touch'
