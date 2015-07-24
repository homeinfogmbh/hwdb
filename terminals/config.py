"""Terminal setup configuration"""

from homeinfo.lib.config import Configuration

__all__ = ['terminals_config']


class TerminalsConfiguration(Configuration):
    """Main terminals configuration class"""

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


terminals_config = TerminalsConfiguration('/etc/terminals.conf')
