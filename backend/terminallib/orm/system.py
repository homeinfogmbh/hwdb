"""Digital signage systems."""

from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField

from mdb import Customer
from peeweeplus import EnumField

from terminallib.config import CONFIG, LOGGER
from terminallib.enumerations import OperatingSystem
from terminallib.orm.common import BaseModel
from terminallib.orm.deployment import Deployment
from terminallib.orm.openvpn import OpenVPN
from terminallib.orm.wireguard import WireGuard


__all__ = ['System']


class System(BaseModel):
    """A physical terminal out in the field."""

    deployment = ForeignKeyField(
        Deployment, column_name='deployment', null=True, backref='systems',
        on_delete='SET NULL', on_update='CASCADE')
    openvpn = ForeignKeyField(OpenVPN, column_name='openvpn', null=True)
    wireguard = ForeignKeyField(WireGuard, column_name='wireguard', null=True)
    manufacturer = ForeignKeyField(
        Customer, null=True, column_name='customer', on_delete='CASCADE',
        on_update='CASCADE')
    created = DateTimeField(default=datetime.now)
    operating_system = EnumField(OperatingSystem)
    monitor = BooleanField(null=True)
    serial_number = CharField(255, null=True)
    model = CharField(255, null=True)   # Hardware model.

    @property
    def vpn_hostname(self):
        """Returns a host name for the OpenVPN network."""
        return '{}.{}'.format(CONFIG['VPN']['domain'], self.id)

    @property
    def wg_hostname(self):
        """Returns the respective host name."""
        return '{}.{}'.format(CONFIG['WireGuard']['domain'], self.id)

    def relocate(self, deployment):
        """Locates a system at the respective deployment."""
        if self.deployment == deployment:
            LOGGER.warning('Refusing to deploy to same deployment.')
            return False

        self.deployment, old_deployment = deployment, self.deployment

        if old_deployment is None:
            LOGGER.info('Initially deployed system at "%s".', self.deployment)
        else:
            LOGGER.info('Relocated system from "%s" to "%s".',
                        old_deployment, self.deployment)

        return True

    def to_json(self, brief=False, cascade=False, **kwargs):
        """Returns a JSON-like dictionary."""
        dictionary = super().to_json(**kwargs)

        if cascade:
            if self.deployment is not None:
                dictionary['deployment'] = self.deployment.to_json()

            if not brief and self.openvpn is not None:
                dictionary['openvpn'] = self.openvpn.to_json()

            if not brief and self.wireguard is not None:
                dictionary['wireguard'] = self.wireguard.to_json()

            if not brief and self.manufacturer is not None:
                dictionary['manufacturer'] = self.manufacturer.to_json()

        return dictionary
