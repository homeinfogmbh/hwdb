"""Terminal setup configuration."""

from configlib import INIParser


__all__ = ['CONFIG']


CONFIG = INIParser('/etc/terminals.conf')
