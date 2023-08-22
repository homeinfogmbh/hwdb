"""ORM model mixins."""

from typing import Iterator, Optional, Union

from peewee import Expression, Select

from hwdb.config import LOGGER, get_config
from hwdb.orm.deployment import Deployment
from hwdb.types import DeploymentChange


__all__ = ["DeployingMixin", "DNSMixin", "MonitoringMixin"]


DOMAIN = "homeinfo.intra"


class DeployingMixin:
    """Mixin for deploying systems."""

    @classmethod
    def undeploy_all(
        cls, deployment: Deployment, *, exclude: Optional[Union["System", int]] = None
    ) -> Iterator[DeploymentChange]:
        """Undeploy other systems."""
        condition = cls.deployment == deployment

        if exclude is not None:
            condition &= cls.id != exclude

        for system in cls.select().where(condition):
            system.fitted = False
            system.deployment = None
            system.save()
            yield DeploymentChange(system, system.deployment, None)

    def change_deployment(
        self, deployment: Optional[Deployment]
    ) -> Optional[DeploymentChange]:
        """Changes the current deployment."""
        if deployment == self.deployment:
            return None

        if deployment is not None and deployment.url is not None:
            if self.apply_url(deployment.url).status_code != 200:
                LOGGER.warning("Could not set URL on system.")

        self.deployment, old = deployment, self.deployment
        return DeploymentChange(self, old, deployment)

    def deploy(
        self,
        deployment: Optional[Deployment],
        *,
        exclusive: bool = False,
        fitted: bool = False,
    ) -> Iterator[DeploymentChange]:
        """Locates a system at the respective deployment."""
        if exclusive and deployment is not None:
            yield from type(self).undeploy_all(deployment, exclude=self)

        if (change := self.change_deployment(deployment)) is not None:
            self.fitted = fitted and (deployment is not None)
            self.save()
            yield change


class DNSMixin:
    """Domain name system mixin."""

    @property
    def domain(self) -> str:
        """Returns the domain."""
        return get_config().get("net", "domain")

    @property
    def fqdn(self) -> str:
        """Returns the fully qualified domain name."""
        return f"{self.hostname}.{DOMAIN}"

    @property
    def hostname(self) -> str:
        """Returns a host name for the OpenVPN network."""
        return f"{self.id}.{self.domain}"

    @property
    def vpn_hostname(self) -> str:
        """Returns a host name for the OpenVPN network."""
        return f"{self.id}.openvpn.{self.domain}"

    @property
    def wg_hostname(self) -> str:
        """Returns the respective host name."""
        return f"{self.id}.wireguard.{self.domain}"


class MonitoringMixin:
    """Mixin for monitoring."""

    @classmethod
    def monitoring_cond(cls) -> Expression:
        """Returns the condition for monitored systems."""
        return ((cls.monitor == 1)) | (  # Monitoring is force-enabled.
            (cls.monitor >> None)  # Monitoring is not disabled.
            & (Deployment.testing == 0)  # Not a testing system.
            & (~(cls.deployment >> None))  # System has a deployment.
            & (cls.fitted == 1)  # System is fitted.
        )

    @classmethod
    def monitored(cls) -> Select:
        """Selects monitored systems."""
        return cls.select(cascade=True).where(cls.monitoring_cond())
