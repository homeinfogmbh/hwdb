"""Terminal setup configuration"""

from configparserplus import ConfigParserPlus

__all__ = ['config']


class TerminalsConfiguration(ConfigParserPlus):
    """Main terminals configuration class"""

    @property
    def ctrl(self):
        self.load()
        return self['ctrl']

    @property
    def db(self):
        self.load()
        return self['db']

    @property
    def monitoring(self):
        self.load()
        return self['monitoring']

    @property
    def net(self):
        self.load()
        return self['net']

    @property
    def openvpn(self):
        self.load()
        return self['openvpn']

    @property
    def ssh(self):
        self.load()
        return self['ssh']


config = TerminalsConfiguration('/etc/terminals.conf')
