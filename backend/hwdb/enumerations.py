"""Common enumerations."""

from enum import Enum, EnumMeta


__all__ = [
    'from_string',
    'Connection',
    'DeploymentType',
    'HardwareModel',
    'HardwareType',
    'OperatingSystem'
]


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


class DeploymentType(Enum):
    """Terminal classes."""

    DDB = 'Das Digitale Brett'
    ETV = 'Exposé TV'
    ETV_TOUCH = 'Exposé TV touch'
    KIOSK = 'Kiosk browser'
    SMART_TV = 'Smart TV'


class HardwareModel(Enum):
    """Ordered hardware model."""

    STANDARD24 = 'Standard 24"'
    STANDARD32 = 'Standard 32"'
    PHOENIX = 'Phönix'
    NEPTUN = 'Neptun'
    OTHER = 'other'


class HardwareType(Enum):
    """Generic hardware type."""

    POWER_SUPPLY = 'power supply'


class OperatingSystem(Enum):
    """Operating systems."""

    ARCH_LINUX = 'Arch Linux'
    ARCH_LINUX_ARM = 'Arch Linux ARM'
    WINDOWS_XP = 'Windows XP'
    WINDOWS_XP_EMBEDDED = 'Windows XP Embedded'
    WINDOWS_EMBEDDED_STANDARD = 'Windows Embedded Standard'
    WINDOWS7 = 'Windows 7'
    WINDOWS7_EMBEDDED = 'Windows 7 Embedded'
    WINDOWS8 = 'Windows 8'
    WINDOWS81 = 'Windows 8.1'
    WINDOWS10 = 'Windows 10'
