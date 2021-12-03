"""ORM model mixins."""

from hwdb.config import get_config


__all__ = ['DNSMixin']


class DNSMixin:
    """Domain name system mixin."""

    @property
    def domain(self) -> str:
        """Returns the domain."""
        return get_config().get('net', 'domain')

    @property
    def hostname(self) -> str:
        """Returns a host name for the OpenVPN network."""
        return f'{self.id}.{self.domain}'

    @property
    def vpn_hostname(self) -> str:
        """Returns a host name for the OpenVPN network."""
        return f'{self.id}.openvpn.{self.domain}'

    @property
    def wg_hostname(self) -> str:
        """Returns the respective host name."""
        return f'{self.id}.wireguard.{self.domain}'
