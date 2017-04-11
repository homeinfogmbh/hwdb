"""Terminal setup configuration"""

from configparserplus import ConfigParserPlus

__all__ = ['config']

config = ConfigParserPlus('/etc/terminals.conf')
