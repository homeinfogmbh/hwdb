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
    def net(self):
        self.load()
        return self['net']

    @property
    def ssh(self):
        self.load()
        return self['ssh']


terminals_config = TerminalsConfiguration('/etc/terminals.conf')
