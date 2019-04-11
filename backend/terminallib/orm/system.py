"""Digital signage systems."""

from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField

from mdb import Customer
from peeweeplus import EnumField

from terminallib.config import CONFIG
from terminallib.enumerations import OperatingSystem
from terminallib.orm.common import BaseModel
from terminallib.orm.location import Location
from terminallib.orm.openvpn import OpenVPN
from terminallib.orm.wireguard import WireGuard


__all__ = ['System']


class System(BaseModel):
    """A physical terminal out in the field."""

    location = ForeignKeyField(
        Location, column_name='location', null=True, backref='systems',
        on_delete='SET NULL', on_update='CASCADE')
    openvpn = ForeignKeyField(OpenVPN, column_name='openvpn', null=True)
    wireguard = ForeignKeyField(WireGuard, column_name='wireguard', null=True)
    creator = ForeignKeyField(
        Customer, column_name='creator', on_delete='SET NULL',
        on_update='CASCADE')
    created = DateTimeField(default=datetime.now)
    operating_system = EnumField(OperatingSystem)
    testing = BooleanField(default=False)
    monitor = BooleanField(null=True)
    serial_number = CharField(255, null=True)

    @property
    def vpn_hostname(self):
        """Returns a host name for the OpenVPN network."""
        return '{}.{}'.format(CONFIG['VPN']['domain'], self.id)

    @property
    def wg_hostname(self):
        """Returns the respective host name."""
        return '{}.{}'.format(CONFIG['WireGuard']['domain'], self.id)

    def to_json(self, brief=False, cascade=True, **kwargs):
        """Returns a JSON-like dictionary."""
        dictionary = super().to_json(**kwargs)

        if not brief and self.openvpn is not None:
            if cascade:
                dictionary['vpn'] = self.openvpn.to_json()
            else:
                dictionary['vpn'] = self.openvpn.id

        if not brief and self.wireguard is not None:
            if cascade:
                dictionary['wireguard'] = self.wireguard.to_json()
            else:
                dictionary['wireguard'] = self.wireguard.id

        if not brief:
            if cascade:
                dictionary['creator'] = self.creator.to_json()
            else:
                dictionary['creator'] = self.creator.id

        if self.location is not None:
            if cascade:
                dictionary['location'] = self.location.to_json()
            else:
                dictionary['location'] = self.location.id

        return dictionary
