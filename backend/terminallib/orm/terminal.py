"""Terminal library ORM models."""

from datetime import datetime

from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import ForeignKeyField

from mdb import Customer
from peeweeplus import EnumField

from terminallib.config import CONFIG
from terminallib.enumerations import OperatingSystem
from terminallib.exceptions import AmbiguousConnections, NoConnection
from terminallib.orm.common import TerminalModel
from terminallib.orm.location import Location


__all__ = ['Terminal']


class Terminal(TerminalModel):
    """A physical terminal out in the field."""

    operating_system = EnumField(OperatingSystem)
    created = DateTimeField(default=datetime.now)
    creator = ForeignKeyField(
        Customer, column_name='creator', on_delete='SET NULL',
        on_update='CASCADE')
    testing = BooleanField(default=False)
    monitor = BooleanField(null=True)
    annotation = CharField(255, null=True)
    serial_number = CharField(255, null=True)
    location = ForeignKeyField(
        Location, column_name='location', null=True, on_delete='SET NULL',
        on_update='CASCADE')

    @property
    def vpn(self):
        """Returns the VPN connection."""
        try:
            vpn, *superfluous = self.vpn_connections
        except ValueError:
            raise NoConnection()

        if superfluous:
            raise AmbiguousConnections()

        return vpn

    @property
    def wireguard(self):
        """Returns the WireGuard connection."""
        try:
            wireguard, *superfluous = self.wg_connections
        except ValueError:
            raise NoConnection()

        if superfluous:
            raise AmbiguousConnections()

        return wireguard

    @property
    def vpn_hostname(self):
        """Returns a host name for the OpenVPN network."""
        return '{}.{}'.format(CONFIG['VPN']['domain'], self.id)

    @property
    def wg_hostname(self):
        """Returns the respective host name."""
        return '{}.{}'.format(CONFIG['WireGuard']['domain'], self.id)

    @property
    def hostname(self):
        """Returns the OpenVPN host name."""
        return self.vpn_hostname

    def to_json(self, cascade=True, **kwargs):
        """Returns a JSON-like dictionary."""
        dictionary = super().to_json(**kwargs)

        if self.vpn is not None:
            dictionary['vpn'] = self.vpn.to_json() if cascade else self.vpn_id

        if self.wireguard is not None:
            if cascade:
                dictionary['wireguard'] = self.wireguard.to_json()
            else:
                dictionary['wireguard'] = self.wireguard_id

        if cascade:
            dictionary['creator'] = self.creator.to_json()
        else:
            dictionary['creator'] = self.creator_id

        if self.location is not None:
            if cascade:
                dictionary['location'] = self.location.to_json()
            else:
                dictionary['location'] = self.location_id

        return dictionary
