"""Common enumerations."""

from enum import Enum, EnumMeta


__all__ = ['from_string', 'Connection', 'OperatingSystem', 'Type']


def from_string(enum: EnumMeta, value: str) -> Enum:
    """Returns an enumeration from a text value."""

    try:
        return enum[value]
    except KeyError:
        return enum(value)


class Connection(Enum):
    """Internet connection information."""

    DSL = 'DSL'
    LTE = 'LTE'


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
