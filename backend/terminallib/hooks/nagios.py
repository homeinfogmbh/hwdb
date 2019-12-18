"""Nagios configuration generation."""

from logging import getLogger
from subprocess import CalledProcessError, check_output
from time import sleep

from nagioslib import write_contactgroups
from nagioslib import write_contacts
from nagioslib import write_hostgroups
from nagioslib import write_hosts
from nagioslib import write_services

from terminallib.orm import System
from terminallib.system import root, systemctl


LOGGER = getLogger('nagios')
NAGIOS_SERVICE = 'nagios4'


def pidof(name):
    """Determines whether the respective process is running."""

    try:
        return check_output(('/bin/pidof', name), text=True).split()
    except CalledProcessError as error:
        if error.returncode == 1:
            return []

        raise


def wait_for_nagios_to_die():
    """Wait for all nagios4 processes to vanish."""

    while pidof('nagios4'):
        LOGGER.info('Waiting for nagios process to die.')

        try:
            sleep(1)
        except KeyboardInterrupt:
            return False

    return True


@root(LOGGER)
def nagioscfgen():
    """Runs the configuration generation."""

    systems = System.monitored()
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
        systemctl('stop', NAGIOS_SERVICE)
    except CalledProcessError:
        LOGGER.error('Restarting nagios failed.')
        return False

    return wait_for_nagios_to_die()
