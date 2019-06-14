"""Nagios configuration generation."""

from logging import getLogger
from subprocess import CalledProcessError

from nagioslib import get_systems
from nagioslib import write_contactgroups
from nagioslib import write_contacts
from nagioslib import write_hostgroups
from nagioslib import write_hosts
from nagioslib import write_services

from terminallib.system import root, systemctl


LOGGER = getLogger('nagios')
NAGIOS_SERVICE = 'nagios4'


@root(LOGGER)
def nagioscfgen():
    """Runs the configuration generation."""

    systems = get_systems()
    LOGGER.info('Writing contacts.')
    write_contacts()
    LOGGER.info('Writing contactgroups.')
    write_contactgroups()
    LOGGER.info('Writing hosts.')
    write_hosts(systems)
    LOGGER.info('Writing hostgroups.')
    write_hostgroups(systems)
    LOGGER.info('Writing services.')
    write_services(systems)
    LOGGER.info('Restarting nagios4 service.')

    try:
        systemctl('restart', NAGIOS_SERVICE)
    except CalledProcessError:
        LOGGER.error('Restarting nagios failed.')
