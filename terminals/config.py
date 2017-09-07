"""Terminal setup configuration"""

from configparserplus import ConfigParserPlus

__all__ = ['CONFIG']

CONFIG = ConfigParserPlus('/etc/terminals.conf')
