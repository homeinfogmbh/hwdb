"""ORM model mixins."""

from terminallib.config import CONFIG


__all__ = ['DNSMixin']


class DNSMixin:
    """Domain name system mixin."""

    @property
    def domain(self):
        """Returns the domain."""
        return CONFIG['net']['domain']

    @property
    def hostname(self):
        """Returns a host name for the OpenVPN network."""
        return f'{self.id}.{self.domain}'

    @property
    def vpn_hostname(self):
        """Returns a host name for the OpenVPN network."""
        return f'{self.id}.openvpn.{self.domain}'

    @property
    def wg_hostname(self):
        """Returns the respective host name."""
        return f'{self.id}.wireguard.{self.domain}'
